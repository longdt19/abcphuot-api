from flask_mongoengine import MongoEngine
from flask_restful import Api
from flask_cors import CORS
from flask_redis import FlaskRedis


cors = CORS()
db = MongoEngine()
api = Api()
redis_store = FlaskRedis()
