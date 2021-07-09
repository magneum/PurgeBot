from ᴋᴀᴛᴇ import *
class Config(object):
    FEEDBACK=True
    API_ID=6372795
    API_HASH ="4b7731b0a6d8e15bef82863887feb293"
    TOKEN="1861790845:AAFmfVGvgoEadA_JGwotw5XpmSH6BEpiE6Y"
    LOAD=[]
    WORKERS=8  

    # API_ID=os.environ.get('API_ID')
    # API_HASH =os.environ.get('API_HASH')
    # TOKEN=os.environ.get('TOKEN')
    # WORKERS=8  


class Development(Config):
    FEEDBACK = True