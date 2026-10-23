import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications';
import {SqsEventSource} from "aws-cdk-lib/aws-lambda-event-sources";
import {Duration} from "aws-cdk-lib";
import { BUCKET_RAW_VIDEOS_PREFIX } from '../constants'
import {IBucketNameProps} from "../interfaces";

export class VideoPipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: IBucketNameProps) {
    super(scope, id, props);

    const lambdaTimeout = Duration.minutes(15);

    const bucketName = props.bucketName;

    const bucket = s3.Bucket.fromBucketAttributes(this, 'ImportedMediaBucket', {
      bucketName,
    });

    const queue = new sqs.Queue(this, 'VideoPipelineQueue', {
      visibilityTimeout: Duration.seconds(lambdaTimeout.toSeconds() * 2),
    });

    const ffmpegLayer = new lambda.LayerVersion(this, 'FFmpegLayer', {
      code: lambda.Code.fromAsset('layers/ffmpeg/ffmpeg.zip'),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_14],
      description: 'Custom FFmpeg layer',
    });

    const fn = new lambda.Function(this, 'VideoPipelineLambda', {
      runtime: lambda.Runtime.PYTHON_3_14,
      handler: 'index.index',
      timeout: lambdaTimeout,
      code: lambda.Code.fromInline(`
def index(event, context):
    print("Received EventBridge Event:", event)
    return {'statusCode': 200}
      `),
      layers: [ffmpegLayer]
    });

    bucket.grantRead(fn);
    bucket.addEventNotification(
        s3.EventType.OBJECT_CREATED,
        new s3n.SqsDestination(queue),
        { prefix: BUCKET_RAW_VIDEOS_PREFIX }
    );
    const eventSource = new SqsEventSource(queue);
    fn.addEventSource(eventSource);
  }
}
