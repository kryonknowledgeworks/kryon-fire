import os


class BaseConfig(object):
    ...


class DevConfig(BaseConfig):
    DEBUG = True
    MONGO_URI = f"mongodb://{os.getenv('host')}:{os.getenv('port')}/{os.getenv('database')}"
