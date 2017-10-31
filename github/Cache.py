import sys

atLeastPython26 = sys.hexversion >= 0x02060000
atLeastPython3 = sys.hexversion >= 0x03000000

if atLeastPython26:
    import json
else:  # pragma no cover (Covered by all tests with Python 2.5)
    import simplejson as json  # pragma no cover (Covered by all tests with Python 2.5)


def cache(function):
    def wrapper(self, *args, **kwargs):
        try:
            parameters = kwargs["parameters"]
        except KeyError:
            parameters = None
        try:
            headers = kwargs["headers"]
        except KeyError:
            headers = None
        try:
            input = kwargs["input"]
        except KeyError:
            input = None
        try:
            cnx = kwargs["cnx"]
        except KeyError:
            cnx = None
        hashing = str(
            {"verb": args[0], "url": args[1], "parameters": parameters, "headers": headers, "input": input, "cnx": cnx})
        """
        try:
            with open("arquivo.dat", "r") as file:
                texto = json.loads(file.readline())
                try:
                    retorno = texto[hashing]
                    existe = True
                except KeyError:
                    existe = False
        except FileNotFoundError:
            texto = {}
            existe = False
        """
        texto = {}
        existe = False
        if not existe:
            retorno = function(self, args[0], args[1], parameters, headers, input, cnx)
            if len(retorno[1]) > 0:
                with open("arquivo.dat", "w") as file:
                    texto[hashing] = retorno
                    file.write(json.dumps(texto))
                    print("ok")
        return retorno

    return wrapper
