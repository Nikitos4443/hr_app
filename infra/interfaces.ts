import * as cdk from 'aws-cdk-lib';

export interface IBucketNameProps extends cdk.StackProps {
    bucketName: string;
}