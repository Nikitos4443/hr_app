import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class S3StorageStack extends cdk.Stack {

  public readonly mediaBucket: s3.IBucket;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Candidates upload resumes and videos straight from the browser with presigned POSTs, and
    // HR opens resume PDFs through presigned GETs, so the frontend origin must be allowed.
    // No production frontend yet: only the local Vite dev server. Once prod exists, add its
    // origin here (e.g. from the FRONTEND_URL SSM parameter).
    const allowedOrigins = ['http://localhost:5173'];

    this.mediaBucket = new s3.Bucket(this, 'SharedMediaBucket', {
      bucketName: `hr-app-media-${this.account}-${this.region}`,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
      cors: [{
        allowedMethods: [s3.HttpMethods.POST, s3.HttpMethods.GET, s3.HttpMethods.PUT],
        allowedOrigins,
        allowedHeaders: ['*'],
        exposedHeaders: ['ETag'],
        maxAge: 3000,
      }],
    });
  }
}
