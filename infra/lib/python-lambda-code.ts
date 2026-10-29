import * as path from 'path';
import { DockerImage, IgnoreMode } from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';

export const REPO_ROOT = path.join(__dirname, '../..');

const UV_BUNDLING_IMAGE = DockerImage.fromRegistry('ghcr.io/astral-sh/uv:0.13.6-python3.14-trixie-slim');

// Packages a uv workspace member as Lambda code. The asset is the repo root (restricted to the
// workspace manifests, uv.lock and the member's own folder) so dependencies resolve from uv.lock.
export function pythonLambdaCode(memberDir: string, packageName: string): lambda.Code {
  return lambda.Code.fromAsset(REPO_ROOT, {
    ignoreMode: IgnoreMode.DOCKER,
    exclude: [
      '*',
      '!pyproject.toml',
      '!uv.lock',
      '!*/pyproject.toml',
      `!${memberDir}`,
      '**/__pycache__',
      '**/.venv',
      '**/.ruff_cache',
    ],
    bundling: {
      image: UV_BUNDLING_IMAGE,
      environment: { UV_CACHE_DIR: '/tmp/uv-cache' },
      command: ['bash', '-c', [
        `uv export --frozen --no-dev --no-emit-workspace --package ${packageName} -o /tmp/requirements.txt`,
        'uv pip install --target /asset-output --python-platform x86_64-manylinux_2_28 --python-version 3.14 -r /tmp/requirements.txt',
        `cp -au ${memberDir}/. /asset-output`,
        'rm -f /asset-output/pyproject.toml',
      ].join(' && ')],
    },
  });
}
