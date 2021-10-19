import pandas as pd
import datetime as dt
import json
from lecom_para_quickview.lecom_functions import replace, replace_portaria, drop, adicionar_novas_portarias
from functions.functions import preparar_excel
from ofertas_e_usuarios.oferta_functions import ofertas_e_usuarios_lecom

today = format(dt.datetime.now(), '%d.%m.%Y')

#CARREGAR A PLANILHA LECOM CRUA DO EXCEL

lecom_df = pd.read_excel('input/entrada.xlsx', skiprows=[0, 1])
df = lecom_df.set_index("#Processo")
usuarios_df = pd.read_excel("input/entrada.xlsx", sheet_name='GRID_CONCLU_USU')
print("INPUT CARREGADO")

#DESCARTAR PROCESSOS CANCELADOS OU EM PREENCHIMENTO

df = drop(df,
          ['CANCELAR',
           'PREENCHER_INFORMACOES_COMPLEMENTARES',
           'CARTILHA_DE_CERTIFICACAO',
           'PREENCHER_DADOS_DA_ORGANIZACAO',
           'PREENCHER_FORMULARIO_DE_REQUERIMENTO'],
          'Etapa atual')

df = drop(df,
          ['Cancelado'],
          'Status do Processo')

#LISTA DE FASES "ACCESS: [LECOM]"

alt = {'ANÁLISE TECNICA - CGCEB': ['ANALISE_MACRO',
                                   'DILIGENCIA',
                                   'ELABORAR_SOLICITACAO_DE_MANIFESTACAO',
                                   'ELABORAR_MINUTA_NOTA_TECNICAPARECER_DE_ENCAMINHAMENTO',
                                   'ELABORAR_PARECER_CONCLUSIVO'],
       'ANÁLISE TECNICA - CCEB': ['VALIDACAO_DAS_INFORMACOES_E_DOCUMENTOS'],
       'APROVAÇÃO': ['APROVACAO_CGCEB',
                     'VALIDACAO_PREVIA',
                     'VALIDAR_DECISAO_E_ASSINAR_PORTARIA'],
       'APRECIAÇÃO': ['APRECIAR_DOCUMENTO_DE_ANALISE_CGCEB'],
       'AGUARDANDO ANÁLISE DO RECURSO SNAS - APRECIAÇÃO': ['RECURSO_APRECIAR_DOCUMENTO_DE_ANALISECGCEB'],
       'AGUARDANDO ANÁLISE DO RECURSO SNAS': ['ANALISE_RECURSO','APROVACAO_DE_PARECER_DE_RECURSO'],
       'AGUARDANDO MANIFESTAÇÃO - MEC': ['MEC_ELABORAR_MANIFESTACAO'],
       'AGUARDANDO MANIFESTAÇÃO - MS': ['SAUDE_ELABORAR_MANIFESTACAO'],
       'AGUARDANDO MANIFESTAÇÃO EM FASE RECURSAL - MS': ['SAUDE_MANIFESTACAO_RECURSO'],
       'AGUARDANDO MANIFESTAÇÃO EM FASE RECURSAL - MEC': ['MEC_MANIFESTACAO_RECURSO'],
       'EM DILIGÊNCIA': ['VALIDACAO_DE_DOCUMENTOS', 'RESPONDER_DILIGENCIA'],
       'TRIAGEM': ['TRIAGEM']}

replace(alt, df, 'Etapa atual')

#LINHAS DE CÓDIGO PARA DEFENIR SE O PROCESSO CONCLUÍDO ESTÁ INDEFERIDO OU DEFERIDO
#APÓS DEFINIÇÃO A INFORMAÇÃO É SALVA NA COLUNA "ETAPA ATUAL"

df['Etapa atual'] = df['Etapa atual'].replace('COMUNICAR_RESULTADO_FINAL', 'INDEFERIDO')
df.loc[(df['Decisão Final'] == 'Deferido') & (df['Etapa atual'] == 'INDEFERIDO'), 'Etapa atual'] = 'DEFERIDO'
cond = (df['Decisão:.2'] == 'RECONSIDERAÇÃO DA DECISÃO DE INDEFERIMENTO') & (df['Etapa atual'] == 'INDEFERIDO')
df.loc[cond, 'Etapa atual'] = 'DEFERIDO'

print("ETAPA ATUAL ATUALIZADA")

#DEFINIÇÃO DE PORTARIAS - REMOVER ULTIMA PARTE DO NOME DO ARQUIVO (ex.: '.pdf12345566778899000')

df['Portaria Assinada'] = df['Portaria Assinada'].map(lambda x: x.split('.pdf')[0], na_action='ignore')
df['Portaria Assinada - Fase Recursal'] = df['Portaria Assinada - Fase Recursal'].map(
    lambda x: x.split('.pdf')[0], na_action='ignore')

#DETERMINA E NOMEIA AS PORTARIAS DE ACORDO COM O SISTEMA NÚMERO/ANO

assinadas = set(df['Portaria Assinada'])
recursal = set(df['Portaria Assinada - Fase Recursal'])

#SE FOR A PRIMEIRA VEZ QUE O CÓDIGO LÊ UMA PORTARIA, ELE SALVA NO JSON

with open('portarias.json', mode='r') as file:
    portaria_assinada = json.load(file)

check_dump = len(portaria_assinada)
adicionar_novas_portarias(assinadas, portaria_assinada)
adicionar_novas_portarias(recursal, portaria_assinada)

if len(portaria_assinada) != check_dump:
    with open('portarias.json', mode='w') as file:
        json.dump(portaria_assinada, file)
        print("NOVAS PORTARIAS SALVAS, CHECAR JSON")

#USANDO O DICIONÁRIO DE SUBSTITUIÇÃO SALVO NO JSON, O SCRIPT SUBSTITUI OS NOMES DAS PORTARIAS NA PLANILHA

replace_portaria(portaria_assinada, df, 'Portaria Assinada')
replace_portaria(portaria_assinada, df, 'Portaria Assinada - Fase Recursal')
df['Portaria Publicada'] = df['Portaria Assinada']
df['Portaria Publicada - Fase Recursal'] = df['Portaria Assinada - Fase Recursal']


#CASOS AD HOC DE PORTARIA ERRADO

for processo_a_corrigir in [6005, 6787, 6969, 8107, 8241, 8327, 9062, 9645, 10078, 11049, 10828,
                            16725, 16882, 17092, 17604, 17648, 18108, 19203, 19253, 19855, 20560,
                            15552, 20902, 20090]:
    try:
        df.loc[processo_a_corrigir, 'Portaria Assinada'] = '163/2020'
        df.loc[processo_a_corrigir, 'Portaria Publicada'] = '163/2020'
    except IndexError:
        print(f'Processo número {processo_a_corrigir} não encontrado')
print("PORTARIAS SUBSTITUÍDAS")
print(f"TOTAL DE {len(portaria_assinada)} PORTARIAS RECONHECIDAS")

#SALVAR A PLANILHA EM EXCEL COMPATÍVEL COM SCRIPT DE QLICKVIEW PARA JUNÇÃO COM DADOS DO ACCESS.

df.to_excel(f'output/processos_lecom_{today}.xlsx', index=True, sheet_name='Principal')
print("TABELA SALVA")

#OFERTAS E USUÁRIOS

new_lecom_df = ofertas_e_usuarios_lecom(usuarios_df, lecom_df)
new_lecom_df.to_excel('output/ofertas_e_usuarios_lecom.xlsx', index=False)
preparar_excel('output/ofertas_e_usuarios_lecom.xlsx')
print("TABELA DE OFERTAS E USUÁRIOS SALVA")