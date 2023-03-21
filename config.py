import tempfile



class Config(object):
    DEBUG = False
    TESTING = False
    

    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = tempfile.mkdtemp()
    SESSION_PERMANENT = False
    SESSION_COOKIE_SECURE = True
    SECRET_KEY = b'\x8el>E\xa2_@F\xbaM?\xaal\x99\xe5\x02+\xae\xc3\xac+\xb4a\xef'
    
    ALLOWED_EXTENSIONS = ["CSV"]
    FILES_UPLOAD = r"C:\Users\Mohamed Mosad\Desktop\myproject\static\files"



class ProductionConfig(Config):
    pass



class DevelopmentConfig(Config):
    DEBUG = True

    SESSION_COOKIE_SECURE = False



class TestingConfig(Config):
    TESTING = True


    SESSION_COOKIE_SECURE = False