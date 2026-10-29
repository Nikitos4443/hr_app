import * as path from 'path';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications';
import {SqsEventSource} from "aws-cdk-lib/aws-lambda-event-sources";
import {Duration} from "aws-cdk-lib";
import { BUCKET_CV_PREFIX } from '../constants'
import {IBucketNameProps} from "../interfaces";
import * as dotenv from 'dotenv';
dotenv.config({ path: path.join(__dirname, '../../.env') });

export class CVPipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: IBucketNameProps) {
    super(scope, id, props);

    const lambdaTimeout = Duration.minutes(15);

    const bucketName = props.bucketName;

    const bucket = s3.Bucket.fromBucketAttributes(this, 'ImportedMediaBucket', {
      bucketName,
    });

    const queue = new sqs.Queue(this, 'CVPipelineQueue', {
      visibilityTimeout: Duration.seconds(lambdaTimeout.toSeconds() * 2),
    });

    const fn = new lambda.Function(this, 'CVPipelineLambda', {
      runtime: lambda.Runtime.PYTHON_3_14,
      handler: 'app.index',
      timeout: lambdaTimeout,
      code: lambda.Code.fromAsset( path.join (__dirname, "../../resume_process_lambda"),
        {bundling: {
          image: lambda.Runtime.PYTHON_3_14.bundlingImage,
          command: ['bash', '-c', 'pip install -r requirements.txt -t /asset-output && cp -au . /asset-output']
        }
      }),
      environment: {
        MONGO_URI: process.env.MONGO_URI!,
        MONGO_DB_NAME: process.env.MONGO_DB_NAME!,
        GOOGLE_API_KEY: process.env.GOOGLE_API_KEY!

      }
    });

    bucket.grantRead(fn);
    bucket.addEventNotification(
        s3.EventType.OBJECT_CREATED,
        new s3n.SqsDestination(queue),
        { prefix: BUCKET_CV_PREFIX }
    );
    const eventSource = new SqsEventSource(queue);
    fn.addEventSource(eventSource);
  }
}
