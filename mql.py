#****************Bibliotecas*************************************
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.metrics import mean_squared_error
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
print(tabela)
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
#print(tabela)
#****************Separa dados de X e y*********************************************
X = tabela.drop("close", axis=1)
y = tabela['close']
#print(X)
#print(y)
#****************Separa dados de trino e dados de teste*********************************************
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)
#****************Seleciono a IA**********************************************
floresta = RandomForestRegressor(bootstrap=True,
                                 n_estimators=13,
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
#****************Decisao***********************************************
fl = mean_squared_error(y_teste, p)
print(f'Floresta------------>>{fl}')
#****************Erro medio quadrado*********************************************
ss = np.sqrt(mean_squared_error(y_teste, p))
print(f'Erro medio quadrado->>{ss}')
#****************Metrica de precisao**********************************************
r_square = metrics.r2_score(y_teste, p)
print(f'Metrica------------->>{r_square}')

#****************funcao simples compra e venda**********************************************
def neg(x):
    if (x >= ult_valor):
        print("Compra ^")
        buy = mt5.ORDER_TYPE_BUY
        return(buy)
    elif(x <= ult_valor):
        print('Venda V')
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
print(sm)
print(sm1, "%")