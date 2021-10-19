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
def ofertas_e_usuarios_lecom(df_usuarios, lecom_df):

    processos = []
    protocolo = []
    cnpj = []
    #ofertas = []
    n_de_ofertas = []
    usuarios = []
    atividades = []

    for processo in set.union(set(df_usuarios['#Processo']), set(df_usuarios["#Processo"])):
        processos.append(processo)
        cnpj.append(single_result_parcer(lecom_df, processo, "#Processo", "CNPJ:"))
        protocolo.append(single_result_parcer(lecom_df, processo, "#Processo", "PROTOCOLO"))
        #ofertas.append(create_str_from_list(df_ofertas, processo, '#Processo', 'Ofertas'))
        usuario = create_str_from_list(df_usuarios, processo, "#Processo", "Usuário(s)")
        usuarios.append(usuario)
        ofertas_cebas = create_str_from_list(df_usuarios, processo, '#Processo', "Atividade")
        n_de_ofertas.append(len(ofertas_cebas.split("; ")))
        atividades.append(ofertas_cebas)

    new_df = pd.DataFrame({
        "#Processo": processos,
        "Protocolo": protocolo,
        "CNPJ": cnpj,
        #"Ofertas CNEAS": ofertas,
        "Número de Ofertas": n_de_ofertas,
        "Ofertas CEBAS": atividades,
        "Usuários": usuarios
    })
    return new_df


def ofertas_access_column(df):
    access = []
    protocolos = []
    cnpj = []
    ofertas = []
    usuarios = []
    n_de_ofertas = []

    for protocolo, row in df.iterrows():
        access.append("Access")
        protocolos.append(protocolo)

        # OFERTAS
        lista_de_ofertas = []
        for column in ["OFERTA_I", "OFERTA_II", "OFERTA_III",
                       "OFERTA_IV", "OFERTA_V", "OFERTA_VI",
                       "OFERTA_VII"]:
            oferta = df.loc[protocolo, column]
            if oferta is not np.NaN:
                lista_de_ofertas.append(oferta)
        ofertas.append("; ".join(lista_de_ofertas))
        n_de_ofertas.append(len(lista_de_ofertas))

        #USUARIOS
        lista_de_usuarios = []
        for column in ["USUARIO_I", "USUARIO_II", "USUARIO_III",
                       "USUARIO_IV", "USUARIO_V", "USUARIO_VI",
                       "USUARIO_VII"]:
            usuario = df.loc[protocolo, column]
            if usuario is not np.NaN:
                lista_de_usuarios.append(usuario)
        usuarios.append("; ".join(lista_de_usuarios))

        cnpj.append(df.loc[protocolo, 'CNPJ'])

    new_df = pd.DataFrame({
        "#Processo": access,
        "Protocolo": protocolos,
        "CNPJ": cnpj,
        "Número de Ofertas": n_de_ofertas,
        "Ofertas CEBAS": ofertas,
        "Usuários": usuarios
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