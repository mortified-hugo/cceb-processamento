import pandas as pd
from functions.text_function import text_to_id


def load_main_sheet(file):
    df = pd.read_excel(file, sheet_name=0, engine='xlrd', skiprows=[0, 1],
                       usecols=['#Processo',
                                ' Data da Requisição',
                                'Análise Macro Analisada por:',
                                'PROTOCOLO',
                                'CNPJ:',
                                'Município:',
                                'Nome da Organização: (como está no CNPJ)',
                                'Tipo:',
                                'Etapa atual'
                                ],
                       )
    df[' Data da Requisição'] = pd.to_datetime(df[' Data da Requisição'], dayfirst=True)
    df['Município:'] = df['Município:'].map(text_to_id)
    return df


def load_cneas(file):
    df = pd.read_excel(file, engine='xlrd', skiprows=range(0, 12),
                       usecols="B,J", index_col="CNPJ da\nEntidade")
    return df


def load_cneas_direct(file):
    df = pd. read_excel(file, engine='xlrd')
    df['Município'] = df['Município'].map(text_to_id)

    return df


def load_old_sheet(file):
    df = pd.read_excel(file, engine='xlrd', index_col='PROTOCOLO')
    return df


def load_processos(file):
    df = pd.read_excel(file,
                       usecols=['BASE',
                                'ENTIDADE',
                                'CNPJ',
                                'DT_PROTOCOLO',
                                'TIPO_PROCESSO',
                                'PROTOCOLO_SEI',
                                'MUNICIPIO',
                                'FASE_PROCESSO']
                       )
    df['MUNICIPIO'] = df['MUNICIPIO'].map(text_to_id)

    return df

