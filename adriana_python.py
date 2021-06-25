# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 21:57:51 2021

@author: Adhmir Renan Voltolini Gomes
"""

import pandas as pd
import numpy as np 

df = pd.read_excel('C:/PHD/Disciplinas/06 - Analise Decisoria/Adriana_df.xlsx')

criterios = df.drop("Alternativas", axis=1)

        
def normalizar(x):
    df_norm = (x-x.min())/(x.max()-x.min())
    return df_norm

df_normalizado = criterios.copy()
df_normalizado = normalizar(df_normalizado)

  
def aquisicao(x):
    for i in range(len(x.columns)):
        x[x.columns[i:i+1]] = x[x.columns[i:i+1]]-x[x.columns[i:i+1]].mean()
    return x           

df_aquisicao = df_normalizado.copy()
df_aquisicao = aquisicao(df_aquisicao)


def naquisicao(x):
    for i in range(len(x.columns)):
        def_norm = x.copy()
        for j in range(len(x)):
            xij = x.iloc[j,i:i+1].values
            soma_coluna = def_norm[def_norm.columns[i:i+1]].sum()
            grau_liberdade = len(def_norm)-1

            primeiro_valor = xij-((soma_coluna-xij)/(grau_liberdade))
            x.iloc[j,i:i+1] = primeiro_valor
         
    return x

df_naquisicao = df_normalizado.copy()
df_naquisicao = naquisicao(df_naquisicao)


def ai_tij(x):
    pesos = 1/len(x.columns)
    x = x.mul(pesos).sum(1)
    return x

serie_ai = ai_tij(df_aquisicao)
serie_ai.rename("Valores_ai", inplace = True)
serie_tij = ai_tij(df_naquisicao)
    
def vth(x,y, vlamba = 0.5):
    Vth = (x*vlamba)+(y*(1-vlamba))
    return Vth
    
Valor_Thales = vth(serie_ai,serie_tij)

def f_utilidade(x):
    phi = (1+np.sqrt(5))/2
    if x > 0:
        utl = x/phi*np.sqrt(x)
       
    else:
        utl = -phi*np.sqrt(np.abs(x))
    return utl
         
pontos_utilidade = Valor_Thales.apply(f_utilidade)


df1 = pd.read_excel('C:/PHD/Disciplinas/06 - Analise Decisoria/Adriana_df.xlsx')


def adriana(x):
    
    x_norm = normalizar(x.copy())
    x_norm.rename(lambda x: x+str("_normalizado"), axis=1, inplace=True)
    x_aquisicao = aquisicao(x_norm.copy())
    x_aquisicao.rename(lambda x: x+str("_aquisicao"), axis=1, inplace=True)
    x_naquisicao = naquisicao(x_norm.copy())
    x_naquisicao.rename(lambda x: x+str("_nao_aquisicao"), axis=1, inplace=True)
    
    serie_ai =  ai_tij(x_aquisicao.copy())
    serie_ai.rename('Valor_ai', inplace = True)
    serie_tij =  ai_tij(x_naquisicao.copy())
    serie_tij.rename('Valor_Tij', inplace = True)    
    Valor_thales =  vth(serie_ai, serie_tij)
    Valor_thales.rename('Valor_de_Thales', inplace = True)
    funcao_utlidade = Valor_thales.apply(f_utilidade)
    funcao_utlidade.rename("Funcao_util", inplace = True)
    
    x = pd.concat([x, x_norm,
                   x_aquisicao, x_naquisicao, 
                   serie_ai, serie_tij, Valor_thales, funcao_utlidade ], axis=1)
    
    return x

teste = adriana(criterios)

import matplotlib.pyplot as plt

plt.scatter(pontos_utilidade,Valor_Thales, c="blue", alpha=0.5, 
            label="Utilidade")
plt.xlabel("pontos_utilidade")
plt.ylabel("Valor_Thales")
plt.legend(loc='upper left')
plt.show() 


