import pandas as pd
from oferta_functions import ofertas_e_usuarios_lecom
from functions.functions import preparar_excel

try:
    ofertas_df = pd.read_excel("input/entrada.xlsx", sheet_name='GRID_OFERTAS')
    usuarios_df = pd.read_excel("input/entrada.xlsx", sheet_name='GRID_CONCLU_USU')
    new_lecom_df = ofertas_e_usuarios_lecom(ofertas_df, usuarios_df)
    new_lecom_df.to_excel('output/ofertas_lecom.xlsx', index=False)
    preparar_excel('output/ofertas_lecom.xlsx')
except FileNotFoundError:
    print('LECOM não encontrada')