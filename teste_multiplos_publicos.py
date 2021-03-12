import pandas as pd

def create_str_from_list(df, ftr, column_a, column_b):
    try:
        todos_os_usuarios = ';'.join(list(set(df[df[column_a] == ftr][column_b])))
        return ', '.join(set(todos_os_usuarios.split(';')))
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
    atividades = []
    usuario = []

    for processo in set(df['#Processo']):
        processos.append(processo)
        etapas.append(single_result_parcer(df, processo, '#Processo', 'Etapa'))
        atividades.append(create_str_from_list(df, processo, '#Processo', 'Atividade'))
        usuario.append(create_str_from_list(df, processo, '#Processo', 'Usuário(s)'))

    new_df = pd.DataFrame({
        "#Processo": processos,
        "Etapa": etapas,
        "Atividades": atividades,
        "Usuário(s)": usuario
    })
    return new_df


#Access
def ofertas_access(df):
    cnpjs = []
    entidade = []
    municipio = []
    uf = []
    oferta = []
    usuario_access = []

    for cnpj in set(df['CNPJ']):
        cnpjs.append(cnpj)
        entidade.append(single_result_parcer(df, cnpj, 'CNPJ', 'ENTIDADE'))
        municipio.append(single_result_parcer(df, cnpj, 'CNPJ', 'MUNICIPIO'))
        uf.append(single_result_parcer(df, cnpj, 'CNPJ', 'UF'))
        oferta.append(create_str_from_list(df, cnpj, 'CNPJ','OFERTA'))
        usuario_access.append(create_str_from_list(df, cnpj, 'CNPJ', 'USUARIO'))

    new_df = pd.DataFrame({
        "CNPJ": cnpjs,
        "ENTIDADE": entidade,
        "MUNICIPIO": municipio,
        "UF": uf,
        "OFERTA": oferta,
        "USUARIO": usuario_access
    })

    return new_df


try:
    lecom_df = pd.read_excel("input/ofertas_lecom.xlsx")
    new_lecom_df = ofertas_lecom(lecom_df)
    new_lecom_df.to_excel('output/ofertas_lecom.xlsx', index=False)
except FileNotFoundError:
    print('LECOM não encontrada')

try:
    access_df = pd.read_excel("input/ofertas_access.xlsx")
    new_access_df = ofertas_access(access_df)
    new_access_df.to_excel('output/ofertas_access.xlsx', index=False)
except FileNotFoundError:
    print('ACCESS não encontrada')






