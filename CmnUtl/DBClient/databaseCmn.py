import json
import pymongo
import DBClient.declaration as declaration

#DB_URL = f'mysql+pymysql://{declaration.USERNAME_DB}:{declaration.PASSWORD_DB}@{declaration.HOST_DB}:{declaration.PORT_DB}/{declaration.NAME_DB}'
if declaration.MONGO_PORT == None or declaration.MONGO_PORT == "":
    conn = pymongo.MongoClient(host=f"mongodb://{declaration.MONGO_HOST}/{declaration.MONGO_NAME}")
else:
    conn = pymongo.MongoClient(host=declaration.MONGO_HOST,port=int(declaration.MONGO_PORT))
#
# class engineConn:
#
#     def __init__(self):
#         self.engine = create_engine(DB_URL, pool_recycle = 500)
#
#     def sessionmaker(self):
#         Session = sessionmaker(bind=self.engine)
#         session = Session()
#         return session
#
#     def connection(self):
#         conn = self.engine.connect()
#         return conn
#
#
# class MyEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj.__class__, DeclarativeMeta):
#             # If obj is an instance of a SQLAlchemy model class, remove the _sa_instance_state attribute
#             data = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
#             data.pop('_sa_instance_state', None)
#             return data
#         if hasattr(obj, '__dict__'):
#             return obj.__dict__
#         else:
#             return json.JSONEncoder.default(self, obj)

# if __name__ == "__main__":
#     ec = engineConn()

