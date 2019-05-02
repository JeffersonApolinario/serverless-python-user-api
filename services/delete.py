import os
import json

from bson import ObjectId
from utils.user_dao import UserDAO
from utils.responses import success, not_found, error

def handler(event, context):
    
    id = event['pathParameters']['id']

    try:
        dao = UserDAO()
        match_params = { '_id' : ObjectId(id) }
        response_deleted = dao.deleted(match_params)

        if (response_deleted.matched_count == 0):
            message = 'User id: {} not found'.format(id)
            return not_found({ 'message': message })

        response = { 'message': 'successfully' }
        
        return success(response)
    except Exception as e:
        return error({ 'message': str(e) })