#****************Bibliotecas*************************************
import math

import MetaTrader5 as mt5
from datetime import datetime
import time
import pandas as pd
import numpy as np
#****************Modulo sklearn*************************************
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
#****************Setando as colunas das planilhas*************************************
pd.set_option('display.max_columns', 400) # número de colunas mostradas
pd.set_option('display.width', 1500)      # max. largura máxima da tabela exibida
#****************Informacao do Ativo*************************************
ativo = 'WDO$'
symbol = "WDOU22"
symbol_info = mt5.symbol_info(symbol)
#****************Conectar ao sistema Meta Trader 5*************************************
#Passo 1: Conectar ao sistema Meta Trader 5
# conecte-se ao MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
print('******************')
print('*   conectado    *')
print('******************')
#****************funcao criar data frame *************************************
def get_ohlc(ativo, timeframe, n=10):
    ativo = mt5.copy_rates_from_pos(ativo, timeframe, 0, n)
    ativo = pd.DataFrame(ativo)
    ativo['time'] = pd.to_datetime(ativo['time'], unit='s')
    ativo.set_index('time', inplace=True)
    return ativo
wdo_m1 = get_ohlc(ativo, mt5.TIMEFRAME_M1,99999)
#****************Transforma em arquivo CSV***********************************
wdo_m1.to_csv('WDO.CSV')
#****************Data atual**************************************************
hoje = datetime.now()
#****************Pega informacao do tick*************************************
ticks = mt5.copy_ticks_from(ativo, hoje, 8000, mt5.COPY_TICKS_INFO)
ult_Preco = mt5.symbol_info_tick(symbol).last
#****************Dados do ativo**********************************************
#Dados do ativo
tabela = wdo_m1
#print(tabela)
#****************Reset index**********************************************
tabela.reset_index('time', inplace=True)
tabela = tabela.drop(["time"], axis=1)
#****************Tabela manipulaco**********************************************
tabela= tabela.drop(["spread", "real_volume"], axis=1)
tabela.loc[:,'media1'] = (tabela['close'].rolling(2).median())
tabela.loc[:,'media7'] = (tabela['close'].rolling(7).median())
tabela.loc[:,'media21'] = (tabela['close'].rolling(21).median())
tabela.loc[:,'media36'] = (tabela['close'].rolling(36).median())
tabela.loc[:,'media200'] = (tabela['close'].rolling(200).median())
#print(tabela)
#****************Preenche o valor vazio com o valor 0**********************************************
tabela = tabela.fillna(0)  # preenche o valor vazio com o valor 0
#****************Separa dados de X e y*********************************************
X = tabela.drop("close", axis=1)
y = tabela['close'].values
#print(X)
#print(y)
#****************Separa dados de trino e dados de teste*********************************************
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.1, random_state=42)
#****************Seleciono a IA**********************************************
floresta = RandomForestRegressor(bootstrap=True,
                                 n_estimators=100,
                                 min_samples_leaf=5,
                                 max_leaf_nodes=5,
                                 max_depth=30,
                                 random_state=42,
                                 n_jobs=-1)
#floresta = RandomForestRegressor(bootstrap=True, n_estimators=1, min_samples_leaf=5, max_leaf_nodes=5,
#                                 random_state=42, n_jobs=-1)
#****************Treino minha IA**********************************************
floresta.fit(X_treino, y_treino)
#****************Faco minha predicao **********************************************
p = floresta.predict(X_teste)
#print(tabela)
#print(accuracy_score(y_teste, p))
#****************Decisao***********************************************
fl = mean_squared_error(y_teste, p)
#print(f'Floresta------------>>{fl}')
#****************Erro medio quadrado*********************************************
ss = np.sqrt(mean_squared_error(y_teste, p))
#print(f'Erro medio quadrado->>{ss}')
#****************Metrica de precisao**********************************************
r_square = metrics.r2_score(y_teste, p)
#print(f'Metrica------------->>{r_square}')
#****************Acuracia da floresta**********************************************
#acc = accuracy_score(y_teste, p)
'''
#****************funcao simples compra e venda**********************************************
def neg(x):
    if (x >= ult_valor):
        #print("Compra ^")
        buy = mt5.ORDER_TYPE_BUY
        return(buy)
    elif(x <= ult_valor):
       # print('Venda V')
        sell = mt5.ORDER_TYPE_SELL
        return(sell)
flor=(fl)

#****************ultimo valor do tick**********************************************
ult_valor = ult_Preco
#****************Valor da condicao BUY e SELL**********************************************
a = neg(flor)
#****************Negociacao**********************************************
sm = (fl-ult_valor)
sm1 = (fl-ult_valor)/100
print(sm1)
print(sm1, "%")
#****************Operacao de negociacao**********************************************
print('*'*5,'metrica1'*1,'*'*5)
'''
#<<<<<<<<<<Nova IA >>>>>>>>>>>>>>>>>>>
x1 = X_teste
y1 = y_teste
#****************Treino minha IA**********************************************
floresta.fit(x1, y1)
#****************Faco minha predicao **********************************************
p1 = floresta.predict(x1)
#print(tabela)
#print(accuracy_score(y_teste, p))
#****************Decisao***********************************************
fl1 = mean_squared_error(y1, p1)
print(f'Ult-Valor----------->>{ult_Preco}')
print(f'Floresta------------>>{fl1}')

#****************Erro medio quadrado*********************************************
ss1 = np.sqrt(mean_squared_error(y1, p1))
print(f'Erro medio quadrado->>{ss1}')
#****************Metrica de precisao**********************************************
r_square1 = metrics.r2_score(y1, p1)
print(f'Metrica------------->>{r_square1}')
#****************Acuracia da floresta**********************************************
#acc = accuracy_score(y_teste, p)
#****************funcao simples compra e venda**********************************************
def neg(f):
    if (ult_valor<= f):
        print('Compra ^')
        buy = 'mt5.ORDER_TYPE_BUY'
        lot = 1.0
        point = mt5.symbol_info(symbol).point
        price = mt5.symbol_info_tick(symbol).ask
        deviation = 20
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": price - 5000 * point,
            "tp": price + 7000 * point,
            "deviation": deviation,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        # enviamos a solicitação de negociação
        result = mt5.order_send(request)
        return(buy)
    elif(ult_valor >= f):
        print('Venda V')
        sell = 'mt5.ORDER_TYPE_SELL'
        lot = 1.0
        point = mt5.symbol_info(symbol).point
        price = mt5.symbol_info_tick(symbol).bid
        deviation = 2
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": price + 5000 * point,
            "tp": price - 5000 * point,
            "deviation": deviation,
            "magic": 234000,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        # enviamos a solicitação de negociação
        result = mt5.order_send(request)
        return(sell)
flor=(fl)
#****************ultimo valor do tick**********************************************
ult_valor = ult_Preco
#****************Valor da condicao BUY e SELL**********************************************
a1 = neg(flor)
print(a1)
print('*'*15,'metrica'*1,'*'*15)

'''
lot = 1.0
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": typ,
    "price": price,
    "sl": price - 5000 * point,
    "tp": price + 5000 * point,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
    }

# enviamos a solicitação de negociação
result = mt5.order_send(request)
# verificamos o resultado da execução
print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol, lot, price, deviation));
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("2. order_send failed, retcode={}".format(result.retcode))
    # solicitamos o resultado na forma de dicionário e exibimos elemento por elemento
    result_dict = result._asdict()
    for field in result_dict.keys():
        print("   {}={}".format(field, result_dict[field]))
        # se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
        if field == "request":
            traderequest_dict = result_dict[field]._asdict()
            for tradereq_filed in traderequest_dict:
                print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))
    print("shutdown() and quit")

lot = 1.0
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": typ,
    "price": price,
    "sl": price + 5000 * point,
    "tp": price - 5000 * point,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
}

# enviamos a solicitação de negociação
result = mt5.order_send(request)
# verificamos o resultado da execução
print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol, lot, price, deviation));
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("2. order_send failed, retcode={}".format(result.retcode))
    # solicitamos o resultado na forma de dicionário e exibimos elemento por elemento
    result_dict = result._asdict()
    for field in result_dict.keys():
        print("   {}={}".format(field, result_dict[field]))
        # se esta for uma estrutura de uma solicitação de negociação, também a exibiremos elemento a elemento
        if field == "request":
            traderequest_dict = result_dict[field]._asdict()
            for tradereq_filed in traderequest_dict:
                print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))
    print("shutdown() and quit")
'''