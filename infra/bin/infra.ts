#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib/core';
import { VideoPipelineStack } from '../lib/video-pipeline-stack';
import { CVPipelineStack } from '../lib/cv-stack';
import { AnalyzerLambdaStack } from '../lib/analyzer-lambda-stack';
import {S3StorageStack} from "../lib/s3-storage-stack";
import {BUCKET_RAW_NAME} from "../constants";
import * as dotenv from 'dotenv';
import {MainServerStack} from "../lib/main-server-stack";
dotenv.config();

const app = new cdk.App();

const env = {
  account: process.env.AWS_ACCOUNT_ID,
  region: process.env.AWS_REGION,
};

const fullBucketName = BUCKET_RAW_NAME + `-${env.account}-${env.region}`

new S3StorageStack(app, 'S3StorageStack', {env});

new MainServerStack(app, 'MainServerStack', {
  bucketName: fullBucketName,
  env,
});

new VideoPipelineStack(app, 'VideoPipelineStack', {
  bucketName: fullBucketName,
  env,
});

new CVPipelineStack(app, 'CVPipelineStack', {
  bucketName: fullBucketName,
  env
})

new AnalyzerLambdaStack(app, 'AnalyzerLambdaStack', {
  bucketName: fullBucketName,
  env
})
