import pandas as pd
from glob import glob
from datetime import datetime

from functions.functions import access_parser, situacao_parser, cneas_parser, preparar_excel, cneas_parser_direct
from functions.load_functions import load_cneas, load_processos, load_main_sheet, load_old_sheet, load_cneas_direct

# Carregar planilhas de informação

hoje = format(datetime.now(), '%d.%m.%Y')
cneas_df = load_cneas('input/cneas.xlsx')
df_processos_geral = load_processos('input/processos.xlsx')

filenames = glob('input/new/*.xlsx')
analistas = [file.replace('.xlsx', '').replace('input/new\\', '') for file in filenames]
print(analistas)

for analista in analistas:

# PLANILHA INICIAL
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


    excel = f'output/{analista}-{hoje}.xlsx'
    sorted_df.to_excel(excel, index=False)
    preparar_excel(excel)

    print(f"Planilha de {analista} finalizada, com {len(final_df.index)} processos atribuídos")

general_df = pd.DataFrame(columns=sorted_df.columns)
for analista in analistas:
    df = pd.read_excel(f'output/{analista}-{hoje}.xlsx')
    df['Analista'] = [analista.capitalize() for row in df['#Processo']]
    general_df = general_df.append(df)
path = f'output/geral.xlsx'
general_df.to_excel(path, index=False)
preparar_excel(path)

print('Planilhas Processadas')

