import pandas as pd

file = 'excelteste/teste.xlsx'

raw_df = pd.read_excel(file, sheet_name=0, engine='xlrd', skiprows=[0, 1])
print(raw_df.head())
print(raw_df.shape)
clean_df = raw_df[['#Processo',
                  ' Data da Requisição',
                  'PROTOCOLO',
                  'CNPJ:',
                  'Nome da Organização: (como está no CNPJ)',
                  'Tipo:']]
clean_df['CNEAS:'] = pd.Series(dtype='str')
clean_df['SITUAÇÃO:'] = pd.Series(dtype='str')
print(clean_df.head())
print(clean_df.shape)
clean_df.to_excel('excelteste/retorno.xlsx', index=False)
