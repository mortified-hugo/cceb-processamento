import pandas as pd
import numpy as np
import win32com.client as win32
import pathlib
from datetime import datetime


def cneas_parser(input_df, cneas, access=False):
    if access:
        column = 'CNPJ'
    else:
        column = 'CNPJ:'
    response = []
    for cnpj in input_df[column]:
        try:
            status = cneas.loc[cnpj, 'Status do\nCNEAS']
            if type(status) is pd.Series:
                status = status[0]
            response.append(status)
        except KeyError:
            response.append('Não Cadastrado')

    return response


def situacao_parser(input_df, situacao):
    response = []
    for protocolo in input_df['PROTOCOLO']:
        try:
            status = situacao.loc[protocolo, 'SITUAÇÃO:']
            if type(status) is pd.Series:
                status = "Dependente do Município: verificar consulta pública"
            if status in ['', np.nan, 0]:
                status = "SEM ANÁLISE"
            response.append(status)
        except KeyError:
            response.append('SEM ANÁLISE')

    return response


def access_parser(df, reference_df):
    base = []
    data = []
    cnpj = []
    nome = []
    tipo = []
    fase = []
    for protocolo in df['PROTOCOLO']:
        base.append(reference_df.loc[protocolo, 'BASE'])
        data.append(reference_df.loc[protocolo, "DT_PROTOCOLO"])
        cnpj.append(reference_df.loc[protocolo, "CNPJ"])
        nome.append(reference_df.loc[protocolo, "ENTIDADE"])
        tipo.append(reference_df.loc[protocolo, "TIPO_PROCESSO"])
        fase.append(reference_df.loc[protocolo, 'FASE_PROCESSO'])
    df['#Processo'] = base
    df[' Data da Requisição'] = data
    df['CNPJ:'] = cnpj
    df['Nome da Organização: (como está no CNPJ)'] = nome
    df['Tipo:'] = tipo
    df['Etapa atual'] = fase

def preparar_excel(input):
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(str(pathlib.Path(input).resolve()))
    ws = wb.Worksheets("Sheet1")
    ws.Columns.AutoFit()
    wb.Save()
    excel.Application.Quit()

def comprimento():
    current_hour = datetime.now().hour
    if current_hour < 12:
        return 'Bom dia'
    elif 12 <= current_hour < 18:
        return 'Boa tarde'
    else:
        return 'Boa noite'


