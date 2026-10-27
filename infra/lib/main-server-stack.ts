import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecs_patterns from 'aws-cdk-lib/aws-ecs-patterns';
import * as path from 'path';
import { IBucketNameProps } from "../interfaces";

export class MainServerStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: IBucketNameProps) {
    super(scope, id, props);

    const cluster = new ecs.Cluster(this, "HRMainServerCluster");

    const loadBalancedFargateService = new ecs_patterns.ApplicationLoadBalancedFargateService(this, 'HrMainServerFargateService', {
      cluster,
      cpu: 256,
      memoryLimitMiB: 512,
      desiredCount: 0,
      publicLoadBalancer: true,
      taskImageOptions: {
        image: ecs.ContainerImage.fromAsset(path.join(__dirname, '../../server')),
        containerPort: 8000,
        logDriver: ecs.LogDrivers.awsLogs({ streamPrefix: 'HrMainServer' }),
      },
    });

    const bucket = s3.Bucket.fromBucketAttributes(this, 'ImportedMediaBucket', {
      bucketName: props.bucketName,
    });

    bucket.grantReadWrite(loadBalancedFargateService.taskDefinition.taskRole);
  }
}