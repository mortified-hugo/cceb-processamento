import numpy as np
import pandas as pd


def create_str_from_list(df, ftr, column_a, column_b):
    try:
        todos_os_usuarios = ';'.join(list(set(df[df[column_a] == ftr][column_b])))
        return '; '.join(set(todos_os_usuarios.split(';')))
    except TypeError:
        return ''


def single_result_parcer(df, ftr, column_a, columb_b):
    n = df.loc[df[column_a] == ftr, columb_b]
    if type(n) is str:
        return n
    else:
        return list(n)[0]


#Lecom
def ofertas_lecom(df):

    processos = []
    etapas = []
    ofertas = []
    n_de_ofertas = []

    for processo in set(df['#Processo']):
        processos.append(processo)
        etapas.append(single_result_parcer(df, processo, '#Processo', 'Etapa'))
        oferta = create_str_from_list(df, processo, '#Processo', 'Ofertas')
        ofertas.append(oferta)
        n_de_ofertas.append(len(oferta.split("; ")))

    new_df = pd.DataFrame({
        "#Processo": processos,
        "Etapa": etapas,
        "Ofertas": ofertas,
        "Número de Ofertas": n_de_ofertas,
    })
    return new_df

def ofertas_access_column(df):
    protocolos = []
    entidades = []
    ofertas = []
    n_de_ofertas = []
    print(df.head())

    for protocolo, row in df.iterrows():
        protocolos.append(protocolo)
        lista_de_ofertas = []
        for column in ["OFERTA_I", "OFERTA_II", "OFERTA_III",
                       "OFERTA_IV", "OFERTA_V", "OFERTA_VI",
                       "OFERTA_VII"]:
            oferta = df.loc[protocolo, column]
            if oferta is not np.NaN:
                lista_de_ofertas.append(oferta)
        entidades.append(df.loc[protocolo, 'ENTIDADE'])
        ofertas.append("; ".join(lista_de_ofertas))
        n_de_ofertas.append(len(lista_de_ofertas))

    new_df = pd.DataFrame({
        "PROTOCOLO": protocolos,
        "ENTIDADE": entidades,
        "OFERTAS": ofertas,
        "NÚMERO DE OFERTAS": n_de_ofertas
    })

    return new_df


#Access
def ofertas_access(df):
    cnpjs = []
    cebas = []
    entidade = []
    municipio = []
    uf = []
    oferta = []
    n_de_ofertas = []
    usuario_access = []

    for cnpj in set(df['CNPJ']):
        cnpjs.append(cnpj)
        entidade.append(single_result_parcer(df, cnpj, 'CNPJ', 'ENTIDADE'))
        cebas.append(single_result_parcer(df, cnpj, 'CNPJ', 'CEBAS'))
        municipio.append(single_result_parcer(df, cnpj, 'CNPJ', 'MUNICIPIO'))
        uf.append(single_result_parcer(df, cnpj, 'CNPJ', 'UF'))
        lista_de_ofertas = create_str_from_list(df, cnpj, 'CNPJ','OFERTA')
        n_de_ofertas.append(len(lista_de_ofertas.split("; ")))
        oferta.append(lista_de_ofertas)
        usuario_access.append(create_str_from_list(df, cnpj, 'CNPJ', 'USUARIO'))

    new_df = pd.DataFrame({
        "CNPJ": cnpjs,
        "ENTIDADE": entidade,
        "CEBAS": cebas,
        "MUNICIPIO": municipio,
        "UF": uf,
        "OFERTA": oferta,
        "NÚMERO DE OFERTAS": n_de_ofertas,
        "USUARIO": usuario_access
    })

    return new_df