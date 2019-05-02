import json
from bson import ObjectId
from utils.user_dao import UserDAO
from utils.responses import success, error, not_found

def handler(event, context):
    
    id = event['pathParameters']['id']
    body = json.loads(event['body'])

    fields = generate_fields(body)

    try:
        dao = UserDAO()
        match_params = { '_id' : ObjectId(id) }
        update_params = { '$set': fields }

        response_update = dao.update_one(match_params, update_params)

        if (response_update.matched_count == 0):
            message = 'User id: {} not found'.format(id)
            return not_found({ 'message': message })

        response = { 'message': 'successfully' }
        
        return success(response)
    except Exception as e:
        return error({ 'message': str(e) })
    
def generate_fields(body):
    items_to_update = {}

    for key, value in body.items():
        items_to_update[key] = value
    
    return items_to_update
