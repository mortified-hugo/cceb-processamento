import pandas as pd
from datetime import datetime
from glob import glob


hoje = format(datetime.now(), "%d.%m.%Y")
file = glob('input/*.xlsx')[-1]
df = pd.read_excel(file, sheet_name=0, skiprows=[0, 1],
                   usecols=['#Processo',
                            'Análise Macro Analisada por:',
                            ' Data da Requisição',
                            'PROTOCOLO',
                            'CNPJ:',
                            'Nome da Organização: (como está no CNPJ)',
                            'Tipo:'])

df.to_excel(f'output/diligência_{hoje}.xlsx', index=False)
