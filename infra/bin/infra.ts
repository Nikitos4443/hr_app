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

const stacks: Record<string, () => cdk.Stack> = {
  S3StorageStack: () => new S3StorageStack(app, 'S3StorageStack', {env}),

  MainServerStack: () => new MainServerStack(app, 'MainServerStack', {
    bucketName: fullBucketName,
    env,
  }),

  VideoPipelineStack: () => new VideoPipelineStack(app, 'VideoPipelineStack', {
    bucketName: fullBucketName,
    env,
  }),

  CVPipelineStack: () => new CVPipelineStack(app, 'CVPipelineStack', {
    bucketName: fullBucketName,
    env
  }),

  AnalyzerLambdaStack: () => new AnalyzerLambdaStack(app, 'AnalyzerLambdaStack', {
    bucketName: fullBucketName,
    env
  }),
};

// DEPLOY_STACKS is a comma-separated list of stack keys to instantiate (e.g. "VideoPipelineStack").
// When unset, every stack is created.
const requested = process.env.DEPLOY_STACKS
  ?.split(',')
  .map((key) => key.trim())
  .filter(Boolean);

const selected = requested?.length ? requested : Object.keys(stacks);

for (const key of selected) {
  const createStack = stacks[key];
  if (!createStack) {
    throw new Error(`Unknown stack "${key}" in DEPLOY_STACKS. Available: ${Object.keys(stacks).join(', ')}`);
  }
  createStack();
}
