import pandas as pd

df = pd.read_excel('input/entrada.xlsx', skiprows=[0, 1])
print(df.head())
print(df.shape)


def drop(to_alter, args):
    df = to_alter
    for arg in args:
        df = df.drop(df[df['Etapa atual'] == arg].index)
    return df


drop(df,
     ['CANCELAR',
     'PREENCHER_INFORMACOES_COMPLEMENTARES',
     'CARTILHA_DE_CERTIFICACAO',
     'PREENCHER_DADOS_DA_ORGANIZACAO',
     'PREENCHER_FORMULARIO_DE_REQUERIMENTO'])
print(df.shape)
