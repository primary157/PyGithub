def cache(function):
    def wrapper(self, verb, url, parameters=None, headers=None, input=None, cnx=None):
        retorno = function(self, verb, url, parameters, headers, input, cnx)
        if len(retorno[1]) > 0:
            print({"verb": verb, "url": url, "parameters": parameters, "headers": headers, "input": input, "cnx": cnx})
            print(retorno[1])
        return retorno

    return wrapper
