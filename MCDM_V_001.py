# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 20:03:35 2021
 pyinstaller.exe --onefile -w --icon=yourIcon.ico 
@author: Adhmir Renan Voltolini Gomes
"""

# Youtube Link: https://www.youtube.com/watch?v=PgLjwl6Br0k

import tkinter as tk
from tkinter import filedialog, ttk, PhotoImage


import pandas as pd
import numpy as np 


# initalise the tkinter GUI
root = tk.Tk()
root.title("Análise Decisória Multicritério")


root.state('zoomed')
#root.geometry("500x500") # set the root dimensions
#root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
#root.resizable(0, 0) # makes the root window fixed in size.

p1 = PhotoImage(file = 'C:/PHD/Disciplinas/06 - Analise Decisoria/PPGCC.png')
 
# Setting icon of master window
root.iconphoto(False, p1)

# Frame for open file dialog
file_frame = tk.LabelFrame(root, text="Menu principal")
file_frame.place(height=100, width=1200, rely=0.65, relx=0)


# Buttons
button1 = tk.Button(file_frame, text="Buscar", command=lambda: File_dialog())
button1.place(rely=0.65, relx=0.10)

button2 = tk.Button(file_frame, text="Carregar", command=lambda: Load_excel_data())
button2.place(rely=0.65, relx=0.20)

button3 = tk.Button(file_frame, text="Limpar", command=lambda: clear_data())
button3.place(rely=0.65, relx=0.30)

button4 = tk.Button(file_frame, text="ADRIANA", command=lambda: calcular())
button4.place(rely=0.65, relx=0.40)

button5 = tk.Button(file_frame, text="Salvar", command=lambda: salvar())
button5.place(rely=0.65, relx=0.50)


# The file/file path text
label_file = ttk.Label(file_frame, text="Nenhum arquivo selecionado, clique em buscar")
label_file.place(rely=0, relx=0)

# Frame for TreeView
frame1 = tk.LabelFrame(root, text="Conjunto de dados")
frame1.place(height=400, width=1200)


## Treeview Widget
tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget



def File_dialog():
    """This Function will open the file explorer and assign the chosen file path to label_file"""
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))
    label_file["text"] = filename
    return None


def Load_excel_data():
    """If the file selected is valid this will load the file into the Treeview"""
    file_path = label_file["text"]
    try:
        excel_filename = r"{}".format(file_path)
        if excel_filename[-4:] == ".csv":
            df = pd.read_csv(excel_filename)
        else:
            df = pd.read_excel(excel_filename)

    except ValueError:
        tk.messagebox.showerror("Information", "Arquivo escolhido inválido")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"{file_path}")
        return None

    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    return None

def pegar_dados():
    file_path = label_file["text"]
    excel_filename = r"{}".format(file_path)
    if excel_filename[-4:] == ".csv":
        df = pd.read_csv(excel_filename)
    else:
        df = pd.read_excel(excel_filename)
        return df
    

def clear_data():
    tv1.delete(*tv1.get_children())
    tv1["column"] = []
   
    return None


"""
Cálculo do método adriana

"""



        
def normalizar(x):
    df_norm = (x-x.min())/(x.max()-x.min())
    return df_norm
  
def aquisicao(x):
    for i in range(len(x.columns)):
        x[x.columns[i:i+1]] = x[x.columns[i:i+1]]-x[x.columns[i:i+1]].mean()
    return x           


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


def ai_tij(x):
    pesos = 1/len(x.columns)
    x = x.mul(pesos).sum(1)
    return x

    
def vth(x,y, vlamba = 0.5):
    Vth = (x*vlamba)+(y*(1-vlamba))
    return Vth
    

def f_utilidade(x):
    phi = (1+np.sqrt(5))/2
    if x > 0:
        utl = x/phi*np.sqrt(x)
       
    else:
        utl = -phi*np.sqrt(np.abs(x))
    return utl
   
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
    funcao_utlidade.rename("Funcao_utilidade", inplace = True)
    
    x = pd.concat([x, x_norm,
                   x_aquisicao, x_naquisicao, 
                   serie_ai, serie_tij, Valor_thales, funcao_utlidade ], axis=1)
    
    return x


def calcular():
   
    x = pegar_dados()
    
    x = adriana(x)
    
    
    clear_data()
    tv1["column"] = list(x.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = x.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    return None

    
def salvar():
    local = label_file["text"]
    dados = pegar_dados()
    dados = adriana(dados)
    writer = pd.ExcelWriter(local, engine='xlsxwriter')
    dados.to_excel(writer, sheet_name='ADRIANA')
    writer.save()
    writer.close()
    
    

"""
import matplotlib.pyplot as plt

plt.scatter(pontos_utilidade,Valor_Thales, c="blue", alpha=0.5, 
            label="Utilidade")
plt.xlabel("pontos_utilidade")
plt.ylabel("Valor_Thales")
plt.legend(loc='upper left')
plt.show() 
    
"""  


root.mainloop()