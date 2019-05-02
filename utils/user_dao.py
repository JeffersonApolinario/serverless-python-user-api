from utils.mongo_connection import MongoConnection
from utils.methods import generate_pagination, generate_filter_and_projection
from bson import ObjectId

import pymongo
import math

class UserDAO():
    user_collection: None
    
    def __init__(self):
        connection = MongoConnection()
        self.user_collection = connection.getCollection('users')

    def create(self, user):
        id = self.user_collection.insert_one(user).inserted_id
        return str(id)

    def find_all(self, params):
        
    

        params_filter_and_paginate = generate_filter_and_projection(params)
        print(params_filter_and_paginate)

        count = self.user_collection.find(
            filter=params_filter_and_paginate['filter_value'],
            projection=params_filter_and_paginate['projection_value']
        ).count()
        

        print(count)
        params['count'] = count

        params_paginate = generate_pagination(params)

        cursor = self.user_collection.find(
            filter=params_filter_and_paginate['filter_value'],
            projection=params_filter_and_paginate['projection_value'],
            sort=[(params_paginate['sort_key'], params_paginate['sort_order'])],
            limit=params_paginate['limit'],
            skip=params_paginate['skip']
        )

        response = {
            'metadata': {
                'page': params_paginate['page'],
                'pages': params_paginate['total_pages'],
                'limit': params_paginate['limit'],
                'totalCount': count,
                'nextPage': params_paginate['next_page'],
                'previousPage': params_paginate['previous_page']
            },
            'data': cursor
        }
        
        return response

    def find_one(self, id):
        user = self.user_collection.find_one({ '_id': ObjectId(id) })
        return user
        
    def update_one(self, match, update_body):
        response = self.user_collection.update_one(match, update_body)
        return response

    def count(self):
        count = self.user_collection.find().count()
        return count

    def deleted(self, match):
        response = self.user_collection.update_one(match, { '$set': { 'status': 'deleted' } })
        return response