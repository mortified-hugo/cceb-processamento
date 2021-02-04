import pandas as pd

lecom_df = pd.read_excel("OFERTAS LECOM.xlsx")
access_df = pd.read_excel("OFERTAS ACCESS.xlsx")


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

processos = []
etapas = []
atividades = []
usuario = []

for processo in set(lecom_df['#Processo']):
    processos.append(processo)
    etapas.append(single_result_parcer(lecom_df, processo, '#Processo', 'Etapa'))
    atividades.append(create_str_from_list(lecom_df, processo, '#Processo', 'Atividade'))
    usuario.append(create_str_from_list(lecom_df, processo, '#Processo', 'Usuário(s)'))

#Access

cnpjs = []
entidade = []
municipio = []
uf = []
oferta = []
usuario_access = []

for cnpj in set(access_df['CNPJ']):
    cnpjs.append(cnpj)
    entidade.append(single_result_parcer(access_df, cnpj, 'CNPJ', 'ENTIDADE'))
    municipio.append(single_result_parcer(access_df, cnpj, 'CNPJ', 'MUNICIPIO'))
    uf.append(single_result_parcer(access_df, cnpj, 'CNPJ', 'UF'))
    oferta.append(create_str_from_list(access_df, cnpj, 'CNPJ','OFERTA'))
    usuario_access.append(create_str_from_list(access_df, cnpj, 'CNPJ', 'USUARIO'))

#Criando novos Excel

new_lecom_df = pd.DataFrame({
    "#Processo": processos,
    "Etapa": etapas,
    "Atividades": atividades,
    "Usuário(s)": usuario
})

new_access_df = pd.DataFrame({
    "CNPJ": cnpjs,
    "ENTIDADE": entidade,
    "MUNICIPIO": municipio,
    "UF": uf,
    "OFERTA": oferta,
    "USUARIO": usuario_access
})

new_lecom_df.to_excel('ofertas_lecom.xlsx', index=False)
new_access_df.to_excel('ofertas_access.xlsx', index=False)




