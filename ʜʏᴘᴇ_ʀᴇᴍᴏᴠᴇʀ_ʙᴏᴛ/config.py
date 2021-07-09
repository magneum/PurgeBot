import os
class Config(object):
    FEEDBACK=True
    LOAD=[]
    WORKERS=8  
    API_ID=os.environ.get('API_ID')
    API_HASH =os.environ.get('API_HASH')
    TOKEN = os.environ.get("TOKEN")
class Development(Config):
    FEEDBACK = True