operaciones_prueba = [] 
operacion = ''
operaciones_dict = {}

operacion = input('Ticker, tipo, nº, precio, fecha: ')

while operacion != 'x':
    
    operaciones_prueba.append(operacion.split())
 
    # añadir datos al diccionario: AAPL V 1000 12 21/10/2019
    if operacion.split()[4] in operaciones_dict.keys():
        operaciones_dict[operacion.split()[4]].append([operacion.split()[0],
                                                                     operacion.split()[1],
                                                                     operacion.split()[2],
                                                                     operacion.split()[3]])
    else:
        operaciones_dict[operacion.split()[4]] = [operacion.split()[0],
                                                   operacion.split()[1],
                                                   operacion.split()[2],
                                                   operacion.split()[3]]
    
    operacion = input('Ticker, tipo, nº, precio, fecha: ')
