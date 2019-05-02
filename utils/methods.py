import datetime
import math
from pymongo import ASCENDING, DESCENDING

def tratament_any(cursor):
    users = []

    for user in cursor:
        print(user)
        user['_id'] = str(user['_id'])

        for key, value in user.items():
            if isinstance(value, datetime.datetime):
                user[key] = value.isoformat()
        users.append(user)
    
    return users

def tratament_one (user):
    user['_id'] = str(user['_id'])
    for key, value in user.items():
        if isinstance(value, datetime.datetime):
            user[key] = value.isoformat()
    return user

def generate_pagination(params):
        
    sort_key = '-createdAt'
    sort_order = DESCENDING
    limit_value = 10
    page = 1
    total_pages = 1
    skip = 0
    count = 0
    
    if (params != None):
        page = int(params.get('page', page)) 
        sort_key = params.get('sort', sort_key)
        limit_value = int(params.get('limit', limit_value))
        count = params['count']
        skip = page * limit_value - limit_value

        if (sort_key[0] != '-'):
            sort_order = ASCENDING
        else:
            sort_order = DESCENDING
            sort_key = sort_key[1:]

    if (count > limit_value):
        total_pages = count / limit_value
        total_pages = math.ceil(total_pages)

    if (page > total_pages):
        raise Exception('page not found')

    del params['count']

    if params.get('page') != None:
        del params['page']
    
    mount = ''
    
    for key, value in params.items():
        mount = mount + '{}={}&'.format(key, value)
    
    mount = mount[:-1]
    
    next_request = None
    previous_request = None

    if (total_pages == 1):
        next_request = None
        previous_request = None
    elif (page == 1):
        next_request = '/?page={}&{}'.format(page + 1, mount)
        previous_request: None
    elif (page == total_pages):
        next_request = None
        previous_request = '/?page={}&{}'.format(page - 1, mount)
    else:
        next_request = '/?page={}&{}'.format(page + 1, mount)
        previous_request = '/?page={}&{}'.format(page - 1, mount)
        
    return {
        'page': page,
        'sort_key': sort_key,
        'sort_order': sort_order,
        'total_pages': total_pages,
        'skip': skip,
        'limit': limit_value,
        'next_page': next_request,
        'previous_page': previous_request
    }

def generate_filter_and_projection(params):
    filter_value = { 'status' : 'ready' }
    projection_value = None
    
    if (params.get('status') != None):
        filter_value['status'] = params['status']

    if (params.get('select') != None):
        projection_value = { '_id' : True }
        fields_select = params['select'].split()

        for field in fields_select:
            projection_value[field] = True
    
    return {
        'filter_value': filter_value,
        'projection_value': projection_value
    }