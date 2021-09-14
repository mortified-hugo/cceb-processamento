import pandas as pd
from glob import glob
from datetime import datetime
from diligencia.__main__ import preparar_diligencia
from functions.functions import preparar_excel


hoje = format(datetime.now(), '%d.%m.%Y')
filenames = glob('input/*.xlsx')
analistas = [file.replace('.xlsx', '').replace('input\\', '') for file in filenames]

for analista in analistas:
    file = f'input/{analista}.xlsx'
    preparar_diligencia(analista, file)

df_base = pd.read_excel(glob('output/*.xlsx')[0])
general_df = pd.DataFrame(columns=df_base.columns)
for analista in analistas:
    df = pd.read_excel(f'output/{analista}_{hoje}.xlsx')
    df['Atribuído a:'] = [analista.upper() for row in df['#Processo']]
    general_df = general_df.append(df)
path = f'output/geral.xlsx'
general_df.to_excel(path, index=False)
preparar_excel(path)
