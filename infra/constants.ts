export const BUCKET_RAW_NAME = 'hr-app-media'

export const BUCKET_RAW_PREFIX = 'raw/'

export const BUCKET_RAW_VIDEOS_PREFIX = BUCKET_RAW_PREFIX + 'videos/'

export const BUCKET_CV_PREFIX = 'CV/'

export const BUCKET_FFMPEG_LAYER_KEY = 'ffmpeg/ffmpeg.zip'

export const MAIN_SERVER_APP_DIR = '/opt/hrapp'

// SecureString parameter holding the contents of server/.env
export const MAIN_SERVER_ENV_PARAMETER = '/hr-app/main-server/env'

export const CADDY_VERSION = '2.10.0'

// Fixed name so other stacks (e.g. the server) can build the role ARN for iam:PassRole
// without a cross-stack reference.
export const ANALYZER_SCHEDULER_ROLE_NAME = 'hr-analyzer-scheduler-role'

// Must match SCHEDULE_NAME_PREFIX in shared/src/hr_core/event_bridge/scheduler.py
export const ANALYZER_SCHEDULE_NAME_PREFIX = 'analyze-vacancy-'

// SSM parameters the analyzer stack publishes and the server reads (see server/config.py).
export const SSM_ANALYZER_LAMBDA_ARN = 'ANALYZER_LAMBDA_ARN'
export const SSM_ANALYZER_SCHEDULER_ROLE_ARN = 'ANALYZER_SCHEDULER_ROLE_ARN'
