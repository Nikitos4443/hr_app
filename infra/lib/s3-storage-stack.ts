import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class S3StorageStack extends cdk.Stack {

  public readonly mediaBucket: s3.IBucket;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    this.mediaBucket = new s3.Bucket(this, 'SharedMediaBucket', {
      bucketName: `hr-app-media-${this.account}-${this.region}`,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });
  }
}
