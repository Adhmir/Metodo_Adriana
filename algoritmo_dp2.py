# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 14:17:29 2021

@author: Adhmir Renan Voltolini Gomes

Algoritmo para cálculo do DP2

"""
"""
A distância DP2 é um indicador sintético elaborado por Trapero (1977) que tem
por finalidade a comparação interespacial e/ou intertemporal de variáveis. Há
duas vantagens inerentes ao método: o primeiro é a atribuição de pontuação a
cada elemento envolvido na análise, formando um ranking dos elementos
envolvidos frente o que a realidade permite, ou seja, o método trabalha com
pontos de referência hierarquicamente construídos. A segunda vantagem é a
possibilidade da mensuração de disparidades entre os envolvidos


Em linhas gerais pode-se formular o algoritmo para o cálculo do DP2 como segue:
    
1º Estabelecimento da matriz de valores das componentes das m empresas envolvidas. 
2º Verificar os critérios das n variáveis envolvidas quanto a sua conduta, 
  ou seja, classificar as variáveis quanto a seu objetivo: “quanto maior, melhor” 
  ou “quanto menor, melhor”;
3º Eleição da base de referência em cada variável, determinando seu ideal teórico;


Todavia, esses passos não serão abordados aqui. Embora seja possível direcionar o segundo passo,
neste algoritmo espera-se que o conjunto de dados já tenha sido construído.

Problemas de la medición del bienestar y conceptos afines: una aplicación al caso español. Madrid: Presidencia del Gobierno, Instituto Nacional de Estadística,

"""
## Leitura do conjunto de dados========================================================================

import pandas as pd
import numpy as np


#df = pd.read_excel('C:/PHD/Disciplinas/06 - Analise Decisoria/Artigo fama multicriterio/Python DP2/df_dp2.xlsx')


### Remover a coluna das empresas para manter apenas os vetores numéricos

#df = df.drop(["Empresa"], axis =1)
#df = pd.read_excel('C:/PHD/Disciplinas/06 - Analise Decisoria/Adriana_df.xlsx') 
## 4º Calcular as distâncias de Frechet ===============================================================

## (|xij-maximo|)/std,    exemplo: (|1,5-1,2|)/0.383406

def frechet(df):
    x = df.copy()
    for i in range(len(x.columns)):
        df_refer = x.copy()
        for j in range(len(x)):
            xij = x.iloc[j,i:i+1].values
            maximo = df_refer[df_refer.columns[i:i+1]].max()
            std = df_refer[df_refer.columns[i:i+1]].std()         
            valor = (np.abs(xij - maximo))/std
            x.iloc[j,i:i+1] = valor
         
    return x



## 5º Ordenação das componentes de maior para menor à hierarquização do modelo=========================


# ordenar e criar uma lista com todos os modelos
def ordemfrechet(x):
    ordem_frechet =  x[x.columns].sum().sort_values(ascending=False).rename("Distancia")
    ordem_frechet = pd.DataFrame(ordem_frechet).reset_index()

    return ordem_frechet


def modelos(x):
    ordem_frechet = ordemfrechet(x)
        
    modelos = []
    for i in range(len(x.columns)):
        
        ordem_modelos = ordem_frechet.loc[0:i,['index']].values
        
        if i > 0:
            modelos.append(ordem_modelos)
            
    return modelos
 

## 6º Obtenção do R2 segundo a hierarquia definida em (5º);
#========================================================================================================

def rquadrado(x):
    df_frechet = frechet(x)
    lista_modelos = modelos(df_frechet)
    v1_r2 = [1.000]
    constante =  np.ones((len(x),1))
    for i in range(len(x.columns)-1):
            #Listas com os nomes dos modelos
            dependente = pd.Series(np.reshape(lista_modelos[i][-1],-1)) 
            independentes = pd.Series(np.reshape(lista_modelos[i][0:len(lista_modelos[i])-1], -1)) 
            Vetores_y = x[dependente]
            
            Vetores_X_const = pd.DataFrame(constante)
            Vetores_X = x[independentes]
            Vetores_X = pd.concat([Vetores_X_const, Vetores_X], ignore_index=True, axis =1)
               
            regression = np.dot(np.linalg.inv(np.dot(Vetores_X.T,Vetores_X)),np.dot(Vetores_X.T,Vetores_y))
            
            yhat = np.sum(regression.T * Vetores_X, axis=1)
            ybar = np.sum(Vetores_y)/len(Vetores_y)      
            error_total = (yhat-ybar.values)**2
            soma_quadrado_total = np.sum(error_total)
            error_res = np.array(Vetores_y) - np.array(yhat).reshape(-1,1)
            soma_residuo_total = np.sum(error_res**2)
            r2_modelos = (1-(soma_residuo_total/(soma_residuo_total+soma_quadrado_total)))
            fator_1r = 1-r2_modelos
            v1_r2.append(fator_1r)         
           
    return v1_r2

## 7º Ponderação dos pesos de acordo com os R2 ======================================================

"""
df = pd.read_excel('C:/PHD/Disciplinas/06 - Analise Decisoria/Adriana_df.xlsx') 

df_frechet = frechet(df)
ordem_de_frechet = ordemfrechet(df_frechet)
ordem_modelos = pd.Series(np.reshape(ordem_de_frechet.loc[:,['index']].values,-1))
ordem_modelos = ordem_modelos.to_list()



Vetores = df_frechet[ordem_modelos]
Vetores = Vetores.add_suffix('_frechet')

lista_r2 = np.array(rquadrado(df_frechet)).reshape(1,-1)

valor_dp2 = np.sum(Vetores*lista_r2, axis=1)

dp2 = pd.concat([df, Vetores, valor_dp2 ], axis=1)
 
x1 = dp2.columns.to_list()
x1[len(x1)-1] = "DP2"

dp2.columns = x1

dp2['Ranking'] = dp2['DP2'].rank(ascending=False)
"""

def calculo_DP2(x):
     
    df_frechet = frechet(x)
    ordem_de_frechet = ordemfrechet(df_frechet)
    ordem_modelos = pd.Series(np.reshape(ordem_de_frechet.loc[:,['index']].values,-1))
    ordem_modelos = ordem_modelos.to_list()
    
    Vetores = df_frechet[ordem_modelos]
    Vetores = Vetores.add_suffix('_frechet')
    
    lista_1_r2 = np.array(rquadrado(df_frechet)).reshape(1,-1)
    
    valor_dp2 = np.sum(Vetores*lista_1_r2, axis=1)
    
    dp2 = pd.concat([x.copy(), Vetores, valor_dp2 ], axis=1)
    
 
    x1 = dp2.columns.to_list() 
    x1[len(x1)-1] = "DP2"
    dp2.columns = x1
    
    dp2['Ranking'] = dp2['DP2'].rank(ascending=False)
    
    #dp2['Empresas'] = df["Empresa"]
    #dp2 = dp2.sort_values(by=['Ranking'])
   
    return dp2

#df = pd.read_excel('C:/PHD/Disciplinas/06 - Analise Decisoria/Adriana_df.xlsx') 

#x = calculo_DP2(df.copy())



