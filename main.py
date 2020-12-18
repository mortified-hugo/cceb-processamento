import pandas as pd
import numpy as np
import datetime as dt


analista = "lucas"
file = f'excelteste/{analista}.xlsx'
old_file = f'excelteste/old-{analista}.xlsx'


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


# PLANIULHA INICIAL
df = pd.read_excel(file, sheet_name=0, engine='xlrd', skiprows=[0, 1],
                   usecols=['#Processo',
                            ' Data da Requisição',
                            'PROTOCOLO',
                            'CNPJ:',
                            'Nome da Organização: (como está no CNPJ)',
                            'Tipo:'],
                   )
df[' Data da Requisição'] = pd.to_datetime(df[' Data da Requisição'], dayfirst=True)
cneas_df = pd.read_excel('excelteste/cneas.xlsx', engine='xlrd', skiprows=range(0, 12),
                         usecols="B,J", index_col="CNPJ da\nEntidade")
old_df = pd.read_excel(old_file, engine='xlrd', index_col='PROTOCOLO')

# DADOS DO ACCESS
df_processos_geral = pd.read_excel('excelteste/processos-geral.xlsx',
                                   usecols=['BASE',
                                            'ENTIDADE',
                                            'CNPJ',
                                            'DT_PROTOCOLO',
                                            'TIPO_PROCESSO',
                                            'PROTOCOLO_SEI']
                                   )
df_access = pd.DataFrame()
df_access['PROTOCOLO'] = [str(p) for p in pd.read_excel(f'excelteste/access-{analista}.xlsx', usecols='B')['PROTOCOLO']]
filtro_processos = df_processos_geral[df_processos_geral['PROTOCOLO_SEI'].isin(df_access['PROTOCOLO'])]
by_protocol = filtro_processos.set_index("PROTOCOLO_SEI")
access_parser(df_access, by_protocol)


# FUSÃO
final_df = df.append(df_access)


# CNEAS E SITUAÇÃO
final_df['CNEAS:'] = cneas_parser(final_df, cneas_df)
final_df['SITUAÇÃO:'] = situacao_parser(final_df, old_df)
sorted_df = final_df.sort_values(' Data da Requisição')
sorted_df[' Data da Requisição'] = sorted_df[' Data da Requisição'].dt.strftime('%d/%m/%Y')
sorted_df.to_excel('excelteste/retorno.xlsx', index=False)
print('Planilha finalizada')
