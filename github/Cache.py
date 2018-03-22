import sys
import types
from functools import wraps

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

    def __init__(self, func):
        self.texto = None
        wraps(func)(self)

    def __del__(self):
        self.save()

    def load(self):
        with open("arquivo.dat", "r") as file:
            self.texto = json.load(file)

    def save(self):
        with open("arquivo.dat", "w") as file:
            json.dump(self.texto, file)

    def __call__(self, verb, url, parameters=None, headers=None, input=None, cnx=None):
        hashing = str(verb) + str(url) + str(parameters) + str(headers) + str(input) + str(cnx)
        try:
            if self.texto is None:
                self.load()
            return self.texto[hashing]
        except FileNotFoundError:
            self.texto = {}
        except KeyError:
            pass
        retorno = self.__wrapped__(self, verb, url, parameters, headers, input, cnx)  # Self realmente necessário?
        self.texto[hashing] = retorno
        # lazy writing?
        return retorno

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)
