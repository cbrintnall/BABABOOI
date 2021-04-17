class BaseConfig:
    pass

class DevConfig(BaseConfig):
    MODEL_URL = "http://quickdraw:6000"

class ProdConfig(BaseConfig):
    MODEL_URL = ""