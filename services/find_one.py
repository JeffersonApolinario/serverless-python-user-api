import datetime

from json import dumps
from pymongo import MongoClient
from utils.user_dao import UserDAO
from utils.responses import success, error, not_found
from utils.methods import tratament_one

def handler(event, context):
    
    id = event['pathParameters']['id']
 
    try:
        dao = UserDAO()
        user = dao.find_one(id)

        if (user is None):
            message = 'User id: {} not found'.format(id)
            return not_found({ 'message': message })
        
        user_tratated = tratament_one(user)
        return success({ 'data': user_tratated })
    except Exception as e:
        return error({ 'message': str(e) })
