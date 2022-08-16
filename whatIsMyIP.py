# -*- coding: utf-8 -*-

import urllib.request as urllib

def whatIsMyIP():

    url1 = None
    url2 = None
    servidor1 = 'http://www.soporteweb.com'
    servidor2 = 'http://www.ifconfig.me/ip'

    consulta1 = urllib.build_opener()
    consulta1.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')] 
    consulta2=consulta1

    respuesta = -1

    try:
        url1 = consulta1.open(servidor1, timeout=17)
        respuesta1 = url1.read()
        try:
            respuesta = respuesta1.decode('UTF-8')
        except UnicodeDecodeError:
            respuesta = respuesta1.decode('ISO-8859-1')

        url1.close()
    except:
        # print('Falló la consulta ip a '+servidor1)
        try:
            url2 = consulta2.open(servidor2, timeout=17)
            respuesta2 = url2.read()
            try:
                respuesta = respuesta2.decode('UTF-8')
            except UnicodeDecodeError:
                respuesta = respuesta2.decode('ISO-8859-1')
            url2.close()
        except:
            raise Exception('Falló la consulta ip')
    return respuesta
    