import pandas as pd
from glob import glob
from datetime import datetime
from functions import *
from load_functions import *

#Carregar planilhas de informação
hoje = format(datetime.now(), '%d.%m.%Y')
cneas_df = load_cneas('input/cneas.xlsx')
df_processos_geral = load_processos('input/processos.xls')

filenames = glob('input/new/*.xlsx')
analistas = [file.rstrip('.xlsx').lstrip('input/new\\') for file in filenames]
print(analistas)

for analista in analistas:
# PLANIULHA INICIAL
    main_file = f'input/new/{analista}.xlsx'
    old_file = f'input/old/{analista}.xlsx'
    df = load_main_sheet(main_file)
    old_df = load_old_sheet(old_file)

# DADOS DO ACCESS

    df_access = pd.DataFrame()
    df_access['PROTOCOLO'] = [str(p) for p in pd.read_excel(f'input/sei/{analista}.xlsx', usecols='B')['PROTOCOLO']]
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
    sorted_df.to_excel(f'output/{analista}-{hoje}.xlsx', index=False)
    print(f"Planilha de {analista} finalizada")

print('Planilhas Processadas')
