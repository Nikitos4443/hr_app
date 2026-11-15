import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';
import {Duration} from "aws-cdk-lib";
import {IBucketNameProps} from "../interfaces";
import { pythonLambdaCode } from "./python-lambda-code";
import * as ssm from 'aws-cdk-lib/aws-ssm';

export class AnalyzerLambdaStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: IBucketNameProps) {
    super(scope, id, props);

    const lambdaTimeout = Duration.minutes(15);

    const fn = new lambda.Function(this, 'AnalyzerLambda', {
      runtime: lambda.Runtime.PYTHON_3_14,
      handler: 'app.index',
      timeout: lambdaTimeout,
      code: pythonLambdaCode('analyzer_lambda', 'analyzer-lambda'),
    });

    const databaseUrlParameter = ssm.StringParameter.fromSecureStringParameterAttributes(this, 'DatabaseUrl', {
      parameterName: 'DATABASE_URL',
    });

    const geminiKeyParameter = ssm.StringParameter.fromSecureStringParameterAttributes(this, 'GeminiKey', {
      parameterName: 'GOOGLE_API_KEY',
    });

    databaseUrlParameter.grantRead(fn);
    geminiKeyParameter.grantRead(fn);

    const schedulerRole = new iam.Role(this, 'EventBridgeSchedulerRole', {
      assumedBy: new iam.ServicePrincipal('scheduler.amazonaws.com'),
    });

    fn.grantInvoke(schedulerRole);
  }
}
