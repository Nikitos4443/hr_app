import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as ssm from 'aws-cdk-lib/aws-ssm';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications';
import { Platform } from 'aws-cdk-lib/aws-ecr-assets';
import {SqsEventSource} from "aws-cdk-lib/aws-lambda-event-sources";
import {Duration} from "aws-cdk-lib";
import { BUCKET_RAW_VIDEOS_PREFIX } from '../constants'
import {IBucketNameProps} from "../interfaces";
import { REPO_ROOT } from "./python-lambda-code";

export class VideoPipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: IBucketNameProps) {
    super(scope, id, props);

    const lambdaTimeout = Duration.minutes(15);

    const bucketName = props.bucketName;

    const bucket = s3.Bucket.fromBucketAttributes(this, 'ImportedMediaBucket', {
      bucketName,
    });

    // Neon connection string, read by video_process_lambda/config.py at cold start
    const databaseUrlParameter = ssm.StringParameter.fromSecureStringParameterAttributes(this, 'DatabaseUrl', {
      parameterName: 'DATABASE_URL',
    });

    const queue = new sqs.Queue(this, 'VideoPipelineQueue', {
      visibilityTimeout: Duration.seconds(lambdaTimeout.toSeconds() * 2),
    });

    // Container image instead of a zip: faster-whisper + PyAV + the baked model are ~500 MB,
    // over the 250 MB zip limit. Build context is the repo root so the image gets the shared
    // hr_core package (see video_process_lambda/Dockerfile and the root .dockerignore).
    // PyAV ships its own ffmpeg libs, so the FFmpeg layer is not needed (images can't use layers).
    const fn = new lambda.DockerImageFunction(this, 'VideoPipelineLambda', {
      code: lambda.DockerImageCode.fromImageAsset(REPO_ROOT, {
        file: 'video_process_lambda/Dockerfile',
        platform: Platform.LINUX_AMD64,
      }),
      architecture: lambda.Architecture.X86_64,
      timeout: lambdaTimeout,
      memorySize: 3008,
    });

    bucket.grantRead(fn);
    databaseUrlParameter.grantRead(fn);
    bucket.addEventNotification(
        s3.EventType.OBJECT_CREATED,
        new s3n.SqsDestination(queue),
        { prefix: BUCKET_RAW_VIDEOS_PREFIX }
    );
    const eventSource = new SqsEventSource(queue, { batchSize: 1 });
    fn.addEventSource(eventSource);
  }
}
