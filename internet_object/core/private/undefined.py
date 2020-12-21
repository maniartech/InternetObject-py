from utils.singletons import Singleton

class Undefined(Singleton):

    def __str__(self):
        return 'undefined'

    def __repr__(self):
        return 'undefined'

undefined = Undefined()
