import * as path from 'path';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';
import {Duration} from "aws-cdk-lib";
import {IBucketNameProps} from "../interfaces";

export class AnalyzerLambdaStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: IBucketNameProps) {
    super(scope, id, props);

    const lambdaTimeout = Duration.minutes(15);

    const fn = new lambda.Function(this, 'AnalyzerLambda', {
      runtime: lambda.Runtime.PYTHON_3_14,
      handler: 'app.index',
      timeout: lambdaTimeout,
      code: lambda.Code.fromAsset(path.join(__dirname, "../../analyzer_lambda"), {
          bundling: {
              image: lambda.Runtime.PYTHON_3_14.bundlingImage,
              command: ['bash', '-c', 'pip install -r requirements.txt -t /asset-output && cp -au . /asset-output']
          }
      }),
    });

    const schedulerRole = new iam.Role(this, 'EventBridgeSchedulerRole', {
      assumedBy: new iam.ServicePrincipal('scheduler.amazonaws.com'),
    });

    fn.grantInvoke(schedulerRole);
  }
}
