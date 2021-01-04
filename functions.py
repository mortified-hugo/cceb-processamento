import pandas as pd
import numpy as np


def cneas_parser(input_df, cneas):
    response = []
    for cnpj in input_df['CNPJ:']:
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
            status = situacao.loc[protocolo, 'SITUAÇÃO']
            if type(status) is pd.Series:
                status = status[0]
            if status in ['', np.nan, 0]:
                status = "NÃO ANALISADO"
            response.append(status)
        except KeyError:
            response.append('NÃO ANALISADO')

    return response


def access_parser(df, reference_df):
    base = []
    data = []
    cnpj = []
    nome = []
    tipo = []
    for protocolo in df['PROTOCOLO']:
        base.append(reference_df.loc[protocolo, 'BASE'])
        data.append(reference_df.loc[protocolo, "DT_PROTOCOLO"])
        cnpj.append(reference_df.loc[protocolo, "CNPJ"])
        nome.append(reference_df.loc[protocolo, "ENTIDADE"])
        tipo.append(reference_df.loc[protocolo, "TIPO_PROCESSO"])
    df['#Processo'] = base
    df[' Data da Requisição'] = data
    df['CNPJ:'] = cnpj
    df['Nome da Organização: (como está no CNPJ)'] = nome
    df['Tipo:'] = tipo

