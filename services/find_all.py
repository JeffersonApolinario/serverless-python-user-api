import os

from pymongo import MongoClient
from utils.user_dao import UserDAO
from utils.responses import success, error
from utils.methods import tratament_any

def handler(event, context):
    try:
        
        params = event['queryStringParameters'] or {}
    
        dao = UserDAO()
        response_find = dao.find_all(params)
        cursor = response_find['data']
        users = tratament_any(cursor)
        
        response_find['data'] = users
        response_find['metadata']['totalListed'] = len(users)

        response = { 
            'metadata': response_find['metadata'],
            'data' : response_find['data']
        }

        return success(response)

    except Exception as e:
        print(e)
        response = { 'message': str(e) }
        return error(response)
    
