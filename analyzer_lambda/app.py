def index(event, context):
    print("Received Event:", event)
    return {'statusCode': 200}