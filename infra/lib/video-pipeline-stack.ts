import * as path from 'path';
import { execSync } from 'child_process';
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

const FFMPEG_URL = 'https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz';

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

    // FFmpeg is downloaded during bundling, which CDK runs only for stacks being deployed,
    // so synthesizing other stacks (e.g. in their own CI) doesn't need the binary.
    const ffmpegLayer = new lambda.LayerVersion(this, 'FFmpegLayer', {
      code: lambda.Code.fromAsset(path.join(__dirname, '../layers/ffmpeg'), {
        exclude: ['bin', '*.zip'],
        assetHashType: cdk.AssetHashType.SOURCE,
        bundling: {
          image: cdk.DockerImage.fromRegistry('alpine'),
          local: {
            tryBundle(outputDir: string) {
              execSync(
                `mkdir -p ${outputDir}/bin && wget -qO- ${FFMPEG_URL} | tar -xJ --strip-components=1 -C ${outputDir}/bin`,
                { stdio: 'inherit' },
              );
              return true;
            },
          },
        },
      }),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_14],
      description: 'Custom FFmpeg layer',
    });

    const fn = new lambda.Function(this, 'VideoPipelineLambda', {
      runtime: lambda.Runtime.PYTHON_3_14,
      handler: 'app.index',
      timeout: lambdaTimeout,
      code: lambda.Code.fromAsset(path.join(__dirname, '../../video_process_lambda')),
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
