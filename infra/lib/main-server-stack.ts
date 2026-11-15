import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecs_patterns from 'aws-cdk-lib/aws-ecs-patterns';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as ssm from 'aws-cdk-lib/aws-ssm';
import * as path from 'path';
import {
  ANALYZER_SCHEDULE_NAME_PREFIX,
  ANALYZER_SCHEDULER_ROLE_NAME,
  SSM_ANALYZER_LAMBDA_ARN,
  SSM_ANALYZER_SCHEDULER_ROLE_ARN,
} from "../constants";
import { IBucketNameProps } from "../interfaces";

export class MainServerStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: IBucketNameProps) {
    super(scope, id, props);

    const cluster = new ecs.Cluster(this, "HRMainServerCluster");

    const loadBalancedFargateService = new ecs_patterns.ApplicationLoadBalancedFargateService(this, 'HrMainServerFargateService', {
      cluster,
      cpu: 256,
      memoryLimitMiB: 512,
      desiredCount: 1,
      publicLoadBalancer: true,
      taskImageOptions: {
        image: ecs.ContainerImage.fromAsset(path.join(__dirname, '../..'), { file: 'server/Dockerfile' }),
        containerPort: 8000,
        logDriver: ecs.LogDrivers.awsLogs({ streamPrefix: 'HrMainServer' }),
      },
    });

    const bucket = s3.Bucket.fromBucketAttributes(this, 'ImportedMediaBucket', {
      bucketName: props.bucketName,
    });

    const taskRole = loadBalancedFargateService.taskDefinition.taskRole;
    bucket.grantReadWrite(taskRole);

    // ARNs published by AnalyzerLambdaStack (deploy it first); the server reads them on startup.
    for (const name of [SSM_ANALYZER_LAMBDA_ARN, SSM_ANALYZER_SCHEDULER_ROLE_ARN]) {
      ssm.StringParameter.fromStringParameterName(this, `Imported${name}`, name).grantRead(taskRole);
    }

    // The server schedules analyzer_lambda runs through EventBridge Scheduler.
    taskRole.addToPrincipalPolicy(new iam.PolicyStatement({
      actions: ['scheduler:CreateSchedule', 'scheduler:UpdateSchedule', 'scheduler:DeleteSchedule'],
      resources: [
        `arn:aws:scheduler:${this.region}:${this.account}:schedule/default/${ANALYZER_SCHEDULE_NAME_PREFIX}*`,
      ],
    }));

    // Creating a schedule hands the scheduler role to the service, which needs PassRole.
    taskRole.addToPrincipalPolicy(new iam.PolicyStatement({
      actions: ['iam:PassRole'],
      resources: [`arn:aws:iam::${this.account}:role/${ANALYZER_SCHEDULER_ROLE_NAME}`],
      conditions: { StringEquals: { 'iam:PassedToService': 'scheduler.amazonaws.com' } },
    }));
  }
}