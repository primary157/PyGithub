import sys

atLeastPython26 = sys.hexversion >= 0x02060000
atLeastPython3 = sys.hexversion >= 0x03000000

if atLeastPython26:
    import json
else:  # pragma no cover (Covered by all tests with Python 2.5)
    import simplejson as json  # pragma no cover (Covered by all tests with Python 2.5)
'''
a Singleton class for holding the cache values and states
'''


class Cache():
    instance = None

    def __init__(self):
        self.texto = {}

    def setUp(self):
        with open("arquivo.dat", "r") as file:
            self.texto = json.load(file)

    def save(self):
        with open("arquivo.dat", "w") as file:  # TODO: lazy writing
            json.dump(self.texto, file)

    def __call__(self, function, verb, url, parameters=None, headers=None, input=None, cnx=None):
        hashing = str(verb) + str(url) + str(parameters) + str(headers) + str(input) + str(cnx)
        try:
            if self.texto != {}:
                self.setUp()
            return self.texto[hashing]
        except FileNotFoundError:
            pass
        except KeyError:
            pass
        retorno = function(self, verb, url, parameters, headers, input, cnx)
        self.texto[hashing] = retorno
        self.save()
        return retorno

    @classmethod
    def uniqueInstance(cls):
        if cls.instance is None:
            cls.instance = Cache()
        return cls.instance


# Decorator definition
def cache(function):
    def wrapper(self, verb, url, parameters=None, headers=None, input=None, cnx=None):
        cache = Cache.uniqueInstance()
        return cache(function, verb, url, parameters, headers, input, cnx)

    return wrapper
