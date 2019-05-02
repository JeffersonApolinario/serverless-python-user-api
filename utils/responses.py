from json import dumps

def success(params):
    return {
        'statusCode': 200,
        'body': dumps(params)
    }

def create(params):
    return {
        'statusCode': 201,
        'body': dumps(params)
    }

def error(params):
    params['statusCode'] = 500

    return {
        'statusCode': 500,
        'body': dumps(params)
    }

def not_found(params):
    params['statusCode'] = 404
    return {
        'statusCode': 404,
        'body': dumps(params)
    }