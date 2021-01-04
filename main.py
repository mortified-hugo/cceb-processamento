import pandas as pd
from glob import glob
from datetime import datetime
from functions import *

analista = "lucas"
main_file = f'input/new/{analista}.xlsx'
old_file = f'input/old/{analista}.xlsx'
cneas_file = 'input/cneas.xlsx'
processos_geral_file = 'input/processos-geral.xlsx'
today = format(datetime.now(), '%d.%m.%Y')


# PLANIULHA INICIAL
def load_main_sheet(file):
    df = pd.read_excel(file, sheet_name=0, engine='xlrd', skiprows=[0, 1],
                       usecols=['#Processo',
                                ' Data da Requisição',
                                'PROTOCOLO',
                                'CNPJ:',
                                'Nome da Organização: (como está no CNPJ)',
                                'Tipo:'],
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


df = load_main_sheet(main_file)
cneas_df = load_cneas(cneas_file)
old_df = load_old_sheet(old_file)

# DADOS DO ACCESS
df_processos_geral = load_processos(processos_geral_file)
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
sorted_df.to_excel('output/retorno.xlsx', index=False)
print('Planilha finalizada')
