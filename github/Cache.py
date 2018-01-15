import sys

atLeastPython26 = sys.hexversion >= 0x02060000
atLeastPython3 = sys.hexversion >= 0x03000000

if atLeastPython26:
    import json
else:  # pragma no cover (Covered by all tests with Python 2.5)
    import simplejson as json  # pragma no cover (Covered by all tests with Python 2.5)


def cache(function):
    def wrapper(self, verb, url, parameters=None, headers=None, input=None, cnx=None):
        hashing = str(verb) + str(url) + str(parameters) + str(headers) + str(input) + str(cnx)
        try:
            with open("arquivo.dat", "r") as file:
                texto = json.load(file)
                retorno = texto[hashing]
                return retorno
        except FileNotFoundError:
            texto = {}
        except KeyError:
            pass
        retorno = function(self, verb, url, parameters, headers, input, cnx)
        with open("arquivo.dat", "w") as file:
            texto[hashing] = retorno
            json.dump(texto, file)
        return retorno

    return wrapper
