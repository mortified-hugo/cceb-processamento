import pandas as pd
from oferta_functions import ofertas_lecom
from functions.functions import preparar_excel

try:
    lecom_df = pd.read_excel("input/entrada.xlsx", sheet_name='GRID_OFERTAS')
    print(lecom_df.head())
    new_lecom_df = ofertas_lecom(lecom_df)
    new_lecom_df.to_excel('output/ofertas_lecom.xlsx', index=False)
    preparar_excel('output/ofertas_lecom.xlsx')
except FileNotFoundError:
    print('LECOM não encontrada')