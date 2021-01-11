import pandas as pd
import datetime as dt
import re
import json

today = format(dt.datetime.now(), '%d.%m.%Y')

df = pd.read_excel('input/entrada.xlsx', skiprows=[0, 1])
print(df.head())
print(df.shape)


def drop(to_alter, args):
    df = to_alter
    for arg in args:
        df = df.drop(df[df['Etapa atual'] == arg].index)
    return df


def replace(to_replace, df, column):
    for key in to_replace:
        df[column] = df[column].replace(to_replace[key], key)


def replace_portaria(to_replace, df, column):
    for key in to_replace:
        df[column] = df[column].replace(key, to_replace[key])


def adicionar_novas_portarias(list, dict):
    for portaria in list:
        if type(portaria) is str and portaria not in dict:
            info = re.findall(r'\d+', portaria)
            if len(info) == 2:
                dict[portaria] = f'{info[0]}/{info[1]}'
            else:
                dict[portaria] = f'{info[0]}/?'


df = drop(df,
          ['CANCELAR',
           'PREENCHER_INFORMACOES_COMPLEMENTARES',
           'CARTILHA_DE_CERTIFICACAO',
           'PREENCHER_DADOS_DA_ORGANIZACAO',
           'PREENCHER_FORMULARIO_DE_REQUERIMENTO'])


alt = {'ANÁLISE TECNICA - CGCEB' : ['ANALISE_MACRO',
                                    'DILIGENCIA',
                                    'ELABORAR_SOLICITACAO_DE_MANIFESTACAO',
                                    'ELABORAR_MINUTA_NOTA_TECNICAPARECER_DE_ENCAMINHAMENTO',
                                    'ELABORAR_PARECER_CONCLUSIVO'],
       'ANÁLISE TECNICA - CCEB' : ['VALIDACAO_DAS_INFORMACOES_E_DOCUMENTOS'],
       'APROVAÇÃO' : ['APROVACAO_CGCEB',
                      'VALIDACAO_PREVIA',
                      'VALIDAR_DECISAO_E_ASSINAR_PORTARIA'],
       'APRECIAÇÃO' : ['APRECIAR_DOCUMENTO_DE_ANALISE_CGCEB'],
       'AGUARDANDO ANÁLISE DO RECURSO SNAS - APRECIAÇÃO' : ['RECURSO_APRECIAR_DOCUMENTO_DE_ANALISECGCEB'],
       'AGUARDANDO ANÁLISE DO RECURSO SNAS' : ['ANALISE_RECURSO'],
       'AGUARDANDO MANIFESTAÇÃO - MEC' : ['MEC_ELABORAR_MANIFESTACAO'],
       'AGUARDANDO MANIFESTAÇÃO - MS' : ['SAUDE_ELABORAR_MANIFESTACAO'],
       'AGUARDANDO MANIFESTAÇÃO EM FASE RECURSAL - MS' : ['SAUDE_MANIFESTACAO_RECURSO'],
       'AGUARDANDO MANIFESTAÇÃO EM FASE RECURSAL - MEC' : ['MEC_MANIFESTACAO_RECURSO'],
       'EM DILIGÊNCIA' :  ['VALIDACAO_DE_DOCUMENTOS', 'RESPONDER_DILIGENCIA']}

replace(alt, df, 'Etapa atual')

df['Etapa atual'] = df['Etapa atual'].replace('COMUNICAR_RESULTADO_FINAL', 'INDEFERIDO')
df.loc[df['Decisão Final'] == 'Deferido', 'Etapa atual'] = 'DEFERIDO'
df.loc[df['Decisão:'] == 'RECONSIDERAÇÃO DA DECISÃO DE INDEFERIMENTO'] = 'DEFERIDO'

print(df.shape)
print(df['Etapa atual'].head())

df['Portaria Assinada'] = df['Portaria Assinada'].map(lambda x: x.split('.pdf')[0], na_action='ignore')
df['Portaria Assinada - Fase Recursal'] = df['Portaria Assinada - Fase Recursal'].map(
    lambda x: x.split('.pdf')[0], na_action='ignore')

assinadas = set(df['Portaria Assinada'])
recursal = set(df['Portaria Assinada - Fase Recursal'])

with open('portarias.json', mode='r') as file:
    portaria_assinada = json.load(file)

check_dump = len(portaria_assinada)
adicionar_novas_portarias(assinadas, portaria_assinada)
adicionar_novas_portarias(recursal, portaria_assinada)

with open('portarias.json', mode='w') as file:
    if len(portaria_assinada) != check_dump:
        json.dump(portaria_assinada, file)

replace_portaria(portaria_assinada, df, 'Portaria Assinada')
replace_portaria(portaria_assinada, df, 'Portaria Assinada - Fase Recursal')
print(portaria_assinada)
print(len(portaria_assinada))



df.to_excel(f'output/processos_lecom_{today}.xlsx', index = False)
