import json

from datetime import datetime
from bson import ObjectId
from utils.user_dao import UserDAO
from utils.responses import create, error, success

def handler(event, context):
    
    body = json.loads(event['body'])

    try:
       
        dao = UserDAO()

        user = tratament_user(body)
        id = dao.create(user)
        response = { 'data': { '_id' : id } }
        return create(response)

    except Exception as e:
        print(e)
        return error({ 'message': str(e) })

def tratament_user(body):
    user = {}
    user['createdAt'] = datetime.now()
    user['updatedAt'] = datetime.now()
    user['firstName'] = body['firstName']
    user['lastName'] = body['lastName']
    user['email'] = body['email']
    user['status'] = 'ready'
    return user