import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as fs from 'fs';
import * as path from 'path';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { IBucketNameProps } from '../interfaces';
import {
  MAIN_SERVER_APP_DIR,
  MAIN_SERVER_ENV_PARAMETER,
  CADDY_VERSION,
} from '../constants';

/**
 * Single EC2 instance hosting the FastAPI backend (systemd) and the built Vue client (Caddy).
 * Caddy config lives in deploy/Caddyfile. Code is deployed by CI: release tarball to S3,
 * then deploy/deploy-main-server.sh runs on the instance through SSM.
 */
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
      actions: ['ssm:GetParameter'],
      resources: [
        cdk.Stack.of(this).formatArn({
          service: 'ssm',
          resource: 'parameter',
          resourceName: MAIN_SERVER_ENV_PARAMETER.replace(/^\//, ''),
        }),
      ],
    }));
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
