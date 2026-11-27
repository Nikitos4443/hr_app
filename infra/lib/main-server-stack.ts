import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as fs from 'fs';
import * as path from 'path';
import { IBucketNameProps } from '../interfaces';
import {
  ANALYZER_SCHEDULE_NAME_PREFIX,
  ANALYZER_SCHEDULER_ROLE_NAME,
  CADDY_VERSION,
  MAIN_SERVER_APP_DIR,
  SSM_ANALYZER_LAMBDA_ARN,
  SSM_ANALYZER_SCHEDULER_ROLE_ARN,
} from '../constants';

export class MainServerStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: IBucketNameProps) {
    super(scope, id, props);

    const vpc = ec2.Vpc.fromLookup(this, 'DefaultVpc', { isDefault: true });

    const securityGroup = new ec2.SecurityGroup(this, 'MainServerSg', {
      vpc,
      description: 'HR app main server: public HTTP/HTTPS, no SSH (use SSM Session Manager)',
      allowAllOutbound: true,
    });
    securityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80), 'HTTP');
    securityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(443), 'HTTPS');

    const role = new iam.Role(this, 'MainServerRole', {
      assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com'),
      managedPolicies: [iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSSMManagedInstanceCore')],
    });

    const bucket = s3.Bucket.fromBucketName(this, 'ImportedMediaBucket', props.bucketName);
    bucket.grantReadWrite(role);

    role.addToPolicy(new iam.PolicyStatement({
      actions: ['kms:Decrypt'],
      resources: ['*'],
      conditions: { StringEquals: { 'kms:ViaService': `ssm.${this.region}.amazonaws.com` } },
    }));

    const userData = ec2.UserData.forLinux();
    userData.addCommands(
      `export APP_DIR=${MAIN_SERVER_APP_DIR} CADDY_VERSION=${CADDY_VERSION}`,
      fs.readFileSync(path.join(__dirname, '../userdata/main-server.sh'), 'utf-8'),
    );

    // Parameters the server loads on startup (PARAMETER_NAMES in server/config.py) when they are not
    // set in the environment. The two analyzer ARNs are published by AnalyzerLambdaStack (deploy it first).
    const serverParameterNames = [
      'SECRET_KEY',
      'DATABASE_URL',
      'GOOGLE_API_KEY',
      'SMTP_USER',
      'SMTP_PASSWORD',
      'BUCKET_NAME',
      'FRONTEND_URL',
      'LLM_MODEL',
      SSM_ANALYZER_LAMBDA_ARN,
      SSM_ANALYZER_SCHEDULER_ROLE_ARN,
    ];
    role.addToPolicy(new iam.PolicyStatement({
      actions: ['ssm:GetParameters', 'ssm:GetParameter'],
      resources: serverParameterNames.map((name) => this.formatArn({
        service: 'ssm',
        resource: 'parameter',
        resourceName: name,
      })),
    }));

    // The server schedules analyzer_lambda runs through EventBridge Scheduler.
    role.addToPolicy(new iam.PolicyStatement({
      actions: ['scheduler:CreateSchedule', 'scheduler:UpdateSchedule', 'scheduler:DeleteSchedule'],
      resources: [
        `arn:aws:scheduler:${this.region}:${this.account}:schedule/default/${ANALYZER_SCHEDULE_NAME_PREFIX}*`,
      ],
    }));

    // Creating a schedule hands the scheduler role to the service, which needs PassRole.
    role.addToPolicy(new iam.PolicyStatement({
      actions: ['iam:PassRole'],
      resources: [`arn:aws:iam::${this.account}:role/${ANALYZER_SCHEDULER_ROLE_NAME}`],
      conditions: { StringEquals: { 'iam:PassedToService': 'scheduler.amazonaws.com' } },
    }));

    const instance = new ec2.Instance(this, 'MainServerInstance', {
      vpc,
      vpcSubnets: { subnetType: ec2.SubnetType.PUBLIC },
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.SMALL),
      machineImage: ec2.MachineImage.latestAmazonLinux2023(),
      securityGroup,
      role,
      userData,
      userDataCausesReplacement: false,
      requireImdsv2: true,
      associatePublicIpAddress: true,
      blockDevices: [{
        deviceName: '/dev/xvda',
        volume: ec2.BlockDeviceVolume.ebs(20, { volumeType: ec2.EbsDeviceVolumeType.GP3, encrypted: true }),
      }],
    });

    const eip = new ec2.CfnEIP(this, 'MainServerEip', { instanceId: instance.instanceId });

    new cdk.CfnOutput(this, 'MainServerInstanceId', { value: instance.instanceId });
    new cdk.CfnOutput(this, 'MainServerPublicIp', { value: eip.attrPublicIp });
    const dashedIp = cdk.Fn.join('-', cdk.Fn.split('.', eip.attrPublicIp));
    new cdk.CfnOutput(this, 'MainServerUrl', {
      value: `https://ec2-${dashedIp}.${this.region}.compute.amazonaws.com`,
    });
  }
}
