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
import { pythonLambdaCode } from "./python-lambda-code";
import * as dotenv from 'dotenv';
import * as ssm from 'aws-cdk-lib/aws-ssm'

dotenv.config({ path: path.join(__dirname, '../../.env') });

export class CVPipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: IBucketNameProps) {
    super(scope, id, props);

    const lambdaTimeout = Duration.minutes(15);

    const bucketName = props.bucketName;

    const bucket = s3.Bucket.fromBucketAttributes(this, 'ImportedMediaBucket', {
      bucketName,
    });

    const databaseUrlParameter = ssm.StringParameter.fromSecureStringParameterAttributes(this, 'DatabaseUrl', {
      parameterName: 'DATABASE_URL',
    })

    const  geminiKeyParameter = ssm.StringParameter.fromSecureStringParameterAttributes(this, 'MySecretLLMAPI', {
      parameterName: 'GOOGLE_API_KEY',
      version: 1
    })

    const gmailUserParameter = ssm.StringParameter.fromSecureStringParameterAttributes(this, 'GmailUser', {
      parameterName: 'SMTP_USER',
    })

    const gmailAppPasswordParameter = ssm.StringParameter.fromSecureStringParameterAttributes(this, 'GmailAppPassword', {
      parameterName: 'SMTP_PASSWORD',
    })

    const frontendUrlParameter = ssm.StringParameter.fromStringParameterAttributes(this, 'FrontendUrl', {
      parameterName: 'FRONTEND_URL',
    })

    const deadLetterQueue = new sqs.Queue(this, 'CVPipelineDLQ', {
      retentionPeriod: Duration.days(14),
    });

    const queue = new sqs.Queue(this, 'CVPipelineQueue', {
      visibilityTimeout: Duration.seconds(lambdaTimeout.toSeconds() * 2),
      deadLetterQueue: { queue: deadLetterQueue, maxReceiveCount: 3 },
    });

    const fn = new lambda.Function(this, 'CVPipelineLambda', {
      runtime: lambda.Runtime.PYTHON_3_14,
      handler: 'app.index',
      timeout: lambdaTimeout,
      // The default 128 MB runs out of memory while importing LangChain/Gemini and parsing the PDF.
      memorySize: 1024,
      code: pythonLambdaCode('resume_process_lambda', 'resume-process-lambda'),
      environment: { BUCKET_NAME: bucketName },
    });

    bucket.grantRead(fn);
    bucket.grantDelete(fn);
    bucket.addEventNotification(
        s3.EventType.OBJECT_CREATED,
        new s3n.SqsDestination(queue),
        { prefix: BUCKET_CV_PREFIX }
    );
    databaseUrlParameter.grantRead(fn);
    geminiKeyParameter.grantRead(fn);
    gmailUserParameter.grantRead(fn);
    gmailAppPasswordParameter.grantRead(fn);
    frontendUrlParameter.grantRead(fn);

    const eventSource = new SqsEventSource(queue);
    fn.addEventSource(eventSource);
  }
}
