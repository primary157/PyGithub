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


# Decorador como classes: Pagina 384 (python cookbook)
class Countdown:
    def __init__(self, cache):
        self.reset()
        self.cache = cache

    def reset(self):
        self.time = 10

    def __call__(self, *args, **kwargs):
        import time
        while self.time:
            time.sleep(1)
            self.time -= 1
        self.cache.save()


class Cache:
    def __init__(self, func):
        from threading import Thread
        self.countdown = Countdown(self)
        self.thread = Thread(target=self.countdown, daemon=True)
        self.text = None
        wraps(func)(self)

    def __del__(self):
        self.save()

    def load(self):
        with open("arquivo.dat", "r") as file:
            self.text = json.load(file)

    def save(self):
        with open("arquivo.dat", "w") as file:
            json.dump(self.text, file)

    def __call__(self, verb, url, parameters=None, headers=None, input=None, cnx=None):
        hashing = str(verb) + str(url) + str(parameters) + str(headers) + str(input) + str(cnx)
        try:
            if self.text is None:
                self.load()
            return self.text[hashing]
        except FileNotFoundError:
            self.text = {}
        except KeyError:
            pass
        retorno = self.__wrapped__(self, verb, url, parameters, headers, input, cnx)
        self.text[hashing] = retorno
        self.countdown.reset()
        if not self.thread.is_alive():
            self.thread.start()
        return retorno

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)
