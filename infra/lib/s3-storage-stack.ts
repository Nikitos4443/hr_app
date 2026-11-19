import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as ssm from 'aws-cdk-lib/aws-ssm';

export class S3StorageStack extends cdk.Stack {

  public readonly mediaBucket: s3.IBucket;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Candidates upload resumes and videos straight from the browser with presigned POSTs, and
    // HR opens resume PDFs through presigned GETs, so the frontend origin must be allowed.
    const frontendUrl = ssm.StringParameter.valueForStringParameter(this, 'FRONTEND_URL');

    this.mediaBucket = new s3.Bucket(this, 'SharedMediaBucket', {
      bucketName: `hr-app-media-${this.account}-${this.region}`,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
      cors: [{
        allowedMethods: [s3.HttpMethods.POST, s3.HttpMethods.GET, s3.HttpMethods.PUT],
        allowedOrigins: [frontendUrl],
        allowedHeaders: ['*'],
        exposedHeaders: ['ETag'],
        maxAge: 3000,
      }],
    });
  }
}
