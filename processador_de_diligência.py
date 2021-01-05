import pandas as pd
from datetime import datetime


file = 'input/new/diligencia.xlsx'
df = pd.read_excel(file, sheet_name=0, skiprows=[0, 1],
                   usecols=['#Processo',
                            'Análise Macro Analisada por:',
                            ' Data da Requisição',
                            'PROTOCOLO',
                            'CNPJ:',
                            'Nome da Organização: (como está no CNPJ)',
                            'Tipo:'])

hoje = str(datetime.today())
df.to_excel(f'output/diligência_{hoje[:11]}.xlsx', index=False)
