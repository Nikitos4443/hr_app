def index(event, context):
    print("Received EventBridge Event:", event)
    return {'statusCode': 200}