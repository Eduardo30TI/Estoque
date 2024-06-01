import gspread as gc
from decouple import config
import streamlit as st
import pandas as pd

CODE='1iToXLcP1P_alrTvhuQTHIwWPSRbp4BV4xhParNlTbYE'
worksheet=gc.service_account(filename='cred.json')
sheet=worksheet.open_by_key(CODE)

@st.cache_data
def inventario():

    df=dict()

    for c in ['STK','Estoque','Confronto STK','Produto']:

        sh=sheet.worksheet(c)

        df[c]=pd.DataFrame(columns=sh.row_values(1),data=sh.get_all_values()[1:])

        pass

    for c in ['STK','Confronto STK']:

        colunas=[l for l in df[c].columns.tolist() if str(l).find('Data')>=0]
        for d in colunas:

            df[c][d]=pd.to_datetime(df[c][d])

            pass

        pass

    return df

    pass

def usuario():

    sh=sheet.worksheet('Usuario')

    df=pd.DataFrame(columns=sh.row_values(1),data=sh.get_all_values()[1:])

    return df

    pass

@st.cache_data
def expedicao():

    df=dict()

    for c in ['Romaneio','Fila','Produto','Picking']:

        sh=sheet.worksheet(c)

        df[c]=pd.DataFrame(columns=sh.row_values(1),data=sh.get_all_values()[1:])

        pass

    for c in ['Romaneio','Fila','Produto','Picking']:

        colunas=[l for l in df[c].columns.tolist() if str(l).find('Data')>=0]
        for d in colunas:

            try:

                df[c][d]=pd.to_datetime(df[c][d])

                pass

            except:


                continue

            pass

        pass

    return df

    pass

def separador():

    sh=sheet.worksheet('Separador')

    df=pd.DataFrame(columns=sh.row_values(1),data=sh.get_all_values()[1:])

    return df

    pass

def insert(df,tabela):

    sh=sheet.worksheet(tabela)

    sh.update([df.columns.values.tolist()]+df.values.tolist())

    pass


