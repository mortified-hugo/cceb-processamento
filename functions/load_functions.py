import pandas as pd


def load_main_sheet(file):
    df = pd.read_excel(file, sheet_name=0, engine='xlrd', skiprows=[0, 1],
                       usecols=['#Processo',
                                ' Data da Requisição',
                                'PROTOCOLO',
                                'CNPJ:',
                                'Nome da Organização: (como está no CNPJ)',
                                'Tipo:'
                                ],
                       )
    df[' Data da Requisição'] = pd.to_datetime(df[' Data da Requisição'], dayfirst=True)
    return df


def load_cneas(file):
    df = pd.read_excel(file, engine='xlrd', skiprows=range(0, 12),
                       usecols="B,J", index_col="CNPJ da\nEntidade")
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
                                'PROTOCOLO_SEI']
                       )
    return df

