def neg(f):
    if (ult_valor<= f):
        print('Compra ^')
        buy = 'mt5.ORDER_TYPE_BUY'
        return(buy)
    elif(ult_valor >= f):
        print('Venda V')
        sell = 'mt5.ORDER_TYPE_SELL'
        return(sell)
fl =25
ult_Preco = 10
flor=(fl)
#****************ultimo valor do tick**********************************************
ult_valor = ult_Preco
#****************Valor da condicao BUY e SELL**********************************************
a1 = neg(flor)
print(a1)