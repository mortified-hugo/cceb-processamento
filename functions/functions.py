import pandas as pd
import numpy as np
import win32com.client as win32
import pathlib
from datetime import datetime


def cneas_parser(input_df, cneas, access=False):
    """
    Pareia os CNPJs das entidades com as informações do CNEAS obtidas na consulta pública.
    Infelizmente, essa função não leva em conta diferentes cneas por municípios, então se usada, é aconceselhável que
    os analistas confirmem a informação ou no próprio cneas ou no Painel CEBAS.
    :param input_df: Planilha do analista (em DataFrame)
    :param cneas: Planilha CNEAS Consulta Pública (em DataFrame)
    :param access: Se verdadeiro, a função é capaz de extrair a informação de uma planilha com as colunas do ACCESS.
    Default é Falso.

    :return: Coluna "SITUAÇÃO CNEAS" adicionado ao DataFrame de input.
    """
    if access:
        column = 'CNPJ'
    else:
        column = 'CNPJ:'
    response = []
    for cnpj in input_df[column]:
        try:
            status = cneas.loc[cnpj, 'Status do\nCNEAS']
            if type(status) is pd.Series:
                status = status[0]
            response.append(status)
        except KeyError:
            response.append('Não Cadastrado')

    return response


def cneas_parser_direct(input_df, cneas, access=False):
    if access:
        column = 'CNPJ'
    else:
        column = 'CNPJ:'
    response = []
    input_df_indexed = input_df.set_index(column)

    for cnpj in input_df[column]:
        try:
            municipio = input_df_indexed.loc[cnpj, 'Município:']

            result = cneas[(cneas['CNPJ'] == cnpj) & (cneas['Município'] == municipio)]
            print(f'{result["Situação CNEAS"]} em {result["Ano de Conclusão"]}')
            nulls = result['Ano Conclusão'].isnull().sum()
            total = len(result['Ano Conclusão'])

            if nulls != total:
                result = result.sort_values(by='Ano Conclusão', ascending=False)
                data = result['Ano Conclusão'][0]
                status = f"Concluído em {data}"
                print(status)
            else:
                status = result['Situação CNEAS'][0]

            if type(status) is pd.Series:
                status = status[0]
            if status == 'Concluído ':
                data = result.loc[municipio, 'Ano Conclusão']
                if type(data) is pd.Series:
                    data = data[0]
                status = f"Concluído em {data}"
            response.append(status)
        except KeyError:
            response.append('Não Cadastrado')

    return response


def situacao_parser(input_df, situacao):
    """
    Transporta a coluna de situação das planilhas antigas dos analistas para a nova planilha.

    :param input_df: DataFrame da planilha do analista
    :param situacao: DataFrame da planilha antiga do analista

    :return: Coluna "Situação:" na planilha finalizada.
    """
    response = []
    for protocolo in input_df['PROTOCOLO']:
        try:
            status = situacao.loc[protocolo, 'SITUAÇÃO:']
            if type(status) is pd.Series:
                status = "Dependente do Município: verificar consulta pública"
            if status in ['', np.nan, 0]:
                status = "SEM ANÁLISE"
            response.append(status)
        except KeyError:
            response.append('SEM ANÁLISE')

    return response


def access_parser(df, reference_df):
    """
    Retira informações da planilha geral de processos de processos contidos em blocos do SEI.
    :param df: Planilha do SEI, com a lista de protocolos na coluna B (Em DataFrame)
    :param reference_df: Planilha de processos geral (Em Data Frame)

    :return: Lista de processos com informações similares àquelas contidas na planilha em produção para serem somadas.
    """
    base = []
    data = []
    cnpj = []
    nome = []
    tipo = []
    fase = []
    municipio = []
    for protocolo in df['PROTOCOLO']:
        base.append(reference_df.loc[protocolo, 'BASE'])
        data.append(reference_df.loc[protocolo, "DT_PROTOCOLO"])
        cnpj.append(reference_df.loc[protocolo, "CNPJ"])
        nome.append(reference_df.loc[protocolo, "ENTIDADE"])
        tipo.append(reference_df.loc[protocolo, "TIPO_PROCESSO"])
        #municipio.append(reference_df.loc[protocolo, "MUNICIPIO"])
        fase.append(reference_df.loc[protocolo, 'FASE_PROCESSO'])
    df['#Processo'] = base
    df[' Data da Requisição'] = data
    df['CNPJ:'] = cnpj
    df['Nome da Organização: (como está no CNPJ)'] = nome
    #df['Município:'] = municipio
    df['Tipo:'] = tipo
    df['Etapa atual'] = fase

def preparar_excel(input):
    """
    Abre as colunas em uma planilha do Excel para facilicar a leitura.
    :param input: string da localização do Excel no computador
    """
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(str(pathlib.Path(input).resolve()))
    ws = wb.Worksheets("Sheet1")
    ws.Columns.AutoFit()
    wb.Save()
    excel.Application.Quit()

def comprimento():
    """
    Define o comprimento do dia mais adequado (para uso em e-mails)
    :return: Comprimento adequado para o horário do dia
    """
    current_hour = datetime.now().hour
    if current_hour < 12:
        return 'Bom dia'
    elif 12 <= current_hour < 18:
        return 'Boa tarde'
    else:
        return 'Boa noite'


