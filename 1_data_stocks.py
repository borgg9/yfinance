# Import the yfinance
import yfinance as yf

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from datetime import *

import scipy.stats as stats

# 0_new_trades.py
operaciones_prueba = [] 
operacion = ''
operaciones_dict = {}

operacion = input('Ticker, tipo, nº, precio, fecha: ')

while operacion != 'x':
    
    operaciones_prueba.append(operacion.split())
 
    # añadir datos al diccionario: AAPL V 1000 12 2020-08-12
    if operacion.split()[4] in operaciones_dict.keys():
        operaciones_dict[operacion.split()[4]].append([operacion.split()[0],
                                                                     operacion.split()[1],
                                                                     operacion.split()[2],
                                                                     operacion.split()[3]])
    else:
        operaciones_dict[operacion.split()[4]] = ([[operacion.split()[0],
                                                   operacion.split()[1],
                                                   operacion.split()[2],
                                                   operacion.split()[3]]])
    
    operacion = input('Ticker, tipo, nº, precio, fecha: ')
      
  #1_data_stocks  
  # LISTA TICKERS
tickers_list = []
tipo_operacion = []
acciones = []
precio_operacion = []

for dias in operaciones_dict.values():
    for operacion in dias:
        if operacion[0] not in tickers_list:
            tickers_list.append(operacion[0])
            tipo_operacion.append(operacion[1])  
            acciones.append(operacion[2])    
            precio_operacion.append(operacion[3]) 
              
tickers_list = sorted(tickers_list)
acciones = sorted(acciones)
precio_operacion = sorted(precio_operacion)
tipo_operacion = sorted(tipo_operacion)

#lista con operaciones, acciones y fechas
formato_fecha = "%Y-%m-%d"
fecha_inicial = datetime.strptime("2020-08-01", formato_fecha)
fecha_final = datetime.strptime(str(date.today()), formato_fecha)
diferencia = fecha_final - fecha_inicial

fechas = []

#lista valor del fondo en el dia
valor_precio_compra = [] 
valor_mercado = []

# lista de [] para cada ticker (numeoro diario de acciones)
num_acciones = []
for ticker in tickers_list:
    num_acciones.append([])

# lista de [] para cada ticker (valor de las acciones a precio de compra)
valor_precio_compra = []
for ticker in tickers_list:
    valor_precio_compra.append([])    
    
# LISTA DE FECHAS
# Añadir un dia anterior a la fecha inicial con 0 acciones
fechas.append(fecha_inicial + timedelta(days =- 1))
for accion in range(len(num_acciones)):
    (num_acciones[accion]).append(0) 
    (valor_precio_compra[accion]).append(0) 

for dia in range(diferencia.days):

    # SOLO AÑADE DIAS DE ENTRESEMANA
    if (fecha_inicial + timedelta(days =+ dia)).weekday() < 5:
        fechas.append(fecha_inicial + timedelta(days =+ dia))
      
        # lista de info de las operaciones
        tickers_dia = []
        acciones_dia = []
        precios_dia = []
        tipo_dia = []        
      
        for accion in range(len(num_acciones)):
            # añade 1 a cada dia y posicion
            (num_acciones[accion]).append(1) 
            (valor_precio_compra[accion]).append(1) 

            # cambia el dia recien añadido por 2
            (num_acciones[accion][-1]) = (num_acciones[accion][-2])
            (valor_precio_compra[accion][-1]) = (valor_precio_compra[accion][-2])               
           
        # analiza si en el dia hay operaciones
        if (fecha_inicial + timedelta(days =+ dia)).strftime('%Y-%m-%d') in operaciones_dict.keys():   
            lista_operaciones = operaciones_dict[(fecha_inicial + timedelta(days =+ dia)).strftime('%Y-%m-%d')]
            #lista_operaciones = [['AAPL', 'C', '1000', '12'], ['AAPL', 'C', '1000', '12'], ['JPM', 'C', '1000', '12']]
            
            # datos de la operacion
            for dato in range(len(operaciones_dict[(fecha_inicial + timedelta(days =+ dia)).strftime('%Y-%m-%d')])):              
                ticker_operacion = operaciones_dict[(fecha_inicial + timedelta(days =+ dia)).strftime('%Y-%m-%d')][dato][0]
                tickers_dia.append(ticker_operacion)     
                acciones_operacion = operaciones_dict[(fecha_inicial + timedelta(days =+ dia)).strftime('%Y-%m-%d')][dato][2]
                acciones_dia.append(int(acciones_operacion))                 
                precios_operacion = operaciones_dict[(fecha_inicial + timedelta(days =+ dia)).strftime('%Y-%m-%d')][dato][3]
                precios_dia.append(int(precios_operacion))                 
                tipo_operacion = operaciones_dict[(fecha_inicial + timedelta(days =+ dia)).strftime('%Y-%m-%d')][dato][1]
                tipo_dia.append(tipo_operacion)
                
           # AÑADIR Nº ACCIONES (Compra / Venta)     
            for accion in range(len(num_acciones)):
                if tickers_list[accion] in tickers_dia:
                    #posicion de la accion en la lista de operaciones del dia
                    posicion_dia = tickers_dia.index(tickers_list[accion])
                    
                    #compra / venta & nº acciones
                    if tipo_dia[posicion_dia] == 'C':
                        num_acciones[accion][-1] = (num_acciones[accion][-2]) + acciones_dia[posicion_dia] 
                    if tipo_dia[posicion_dia] == 'V': 
                        num_acciones[accion][-1] = (num_acciones[accion][-2]) - acciones_dia[posicion_dia]                     
                        
                    #valor cartera con precio compra
                    if tipo_dia[posicion_dia] == 'C':
                        valor_precio_compra[accion][-1] = (num_acciones[accion][-2]) + (acciones_dia[posicion_dia] * precios_dia[posicion_dia])
                    if tipo_dia[posicion_dia] == 'V': 
                        valor_precio_compra[accion][-1] = (num_acciones[accion][-2]) - (acciones_dia[posicion_dia] * precios_dia[posicion_dia])                      
   
# TRASPONER LISTA Nº ACCIONES y VALOR COMPRA
traspo_valor_precio_compra = np.array(valor_precio_compra).T
traspo_num_acciones = np.array(num_acciones).T

df_valor_compra = pd.DataFrame(traspo_valor_precio_compra, columns=(list(tickers_list)), index=(list(fechas)))
df_valor_compra.index.name = 'Fechas'

df_num_acciones = pd.DataFrame(traspo_num_acciones, columns=(list(tickers_list)), index=(list(fechas)))
df_num_acciones.index.name = 'Fechas'

precios_last = []
sectores = []
country = []
currency = []

for ticker in tickers_list:
    try:
        precios_last.append(yf.Ticker(ticker).history(period="1d")['Close'][0])
    except IndexError:
        precios_last.append(0)
        
    try:
        sectores.append(yf.Ticker(ticker).info['sector'])
    except IndexError:
        sectores.append(0)

    try:
        country.append(yf.Ticker(ticker).info['country'])
    except IndexError:
        country.append(0)
        
    try:
        currency.append(yf.Ticker(ticker).info['currency'])
    except IndexError:
        currency.append(0) 
          
cantidad_acciones = [] # nº de acciones
valor = [] # valor posición
valor_tot = 0 #valor total de las posiciones
porcentaje = [] # % accion
p_l_porc = [] # Ganancia / perdida PORCENTAJE %
p_l_cash = [] # Ganancia / perdida CASH €$

for x in range(len(num_acciones)):
    cantidad_acciones.append(num_acciones[x][-1])
    valor.append(int(acciones[x]) * precios_last[x])
    p_l_porc.append(((int(precios_last[x]) - int(precio_operacion[x])) / int(precio_operacion[x])) * 100)
    p_l_cash.append((int(precios_last[x]) - int(precio_operacion[x])) * int(acciones[x]))
    
for posicion in valor:
    valor_tot += int(posicion)    
    
for x in range(len(num_acciones)):
    porcentaje.append((valor[x] / valor_tot) * 100)
    
data = pd.DataFrame({'Country':country, 'Currency':currency, 'nº':cantidad_acciones, 
                     '% Posición':porcentaje, 'Valor':valor, 'Sector':sectores, 'Precio Compra':precio_operacion,
                     'Precio':precios_last, '+/- %':p_l_porc, '+/- €':p_l_cash}, index=(list(tickers_list)))
data.index.name = 'Ticker'
data
