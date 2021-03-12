import pandas as pd
from datetime import datetime as dt


def validade(df):

    result = []
    hoje = dt.now()

    list_of_etapas_access = ['ANÁLISE TÉCNICA',
                             'ANÁLISE TECNICA - CGCEB',
                             'ANÁLISE TECNICA - CCEB'
                             'EM DILIGÊNCIA',
                             'AGUARDANDO ANÁLISE',
                             'AGUARDANDO MANIFESTAÇÃO',
                             'APRECIAÇÃO',
                             'APROVAÇÃO']
    list_of_etapas_json = ["ANALISE_MACRO",
                           'VALIDACAO_DE_DOCUMENTOS',
                           'APROVACAO_CGCEB',
                           'RESPONDER_DILIGENCIA',
                           'DILIGENCIA',
                           'APRECIAR_DOCUMENTO_DE_ANALISE_CGCEB',
                           'VALIDACAO_PREVIA',
                           'VALIDAR_DECISAO_E_ASSINAR_PORTARIA',
                           'ELABORAR_PARECER_CONCLUSIVO',
                           'ELABORAR_SOLICITACAO_DE_MANIFESTACAO',
                           'MEC_ELABORAR_MANIFESTACAO',
                           'ELABORAR_MINUTA_NOTA_TECNICAPARECER_DE_ENCAMINHAMENTO',
                           'SAUDE_ELABORAR_MANIFESTACAO']
    for row in df.iterrows():
        row = row[1]
        if row['DT_FIM_CERTIFICACAO_ATUAL'] >= hoje:
            result.append("Vigente")
        else:
            if row['TIPO_PROCESSO'] == 'Renovação':
                if row['FASE_PROCESSO'] in list_of_etapas_json:
                    result.append("Válida")
                elif row['FASE_PROCESSO'] in list_of_etapas_access:
                    result.append("Válida")
                else:
                    result.append("Sem Cebas")
            else:
                result.append("Sem Cebas")

    return result


def ultimo_processo(info, coluna):
    return list(info[coluna])[0]


def listagem_de_entidades(df):
    rows = []
    print(f"{len(df['CNPJ'])} processos detectados")
    print(f"{len(set(df['CNPJ']))} CNPJs únicos detectados")
    for cnpj in set(df['CNPJ']):
        info_cnpj = df[df['CNPJ'] == cnpj].sort_values(by='DT_PROTOCOLO', ascending=False)

        protocolo = ultimo_processo(info_cnpj, 'PROTOCOLO')
        data = ultimo_processo(info_cnpj, 'DT_PROTOCOLO')
        tipo = ultimo_processo(info_cnpj, 'TIPO_PROCESSO')
        etapa = ultimo_processo(info_cnpj, 'FASE_PROCESSO')
        nome = ultimo_processo(info_cnpj, 'ENTIDADE')

        dates = info_cnpj['DT_FIM_CERTIFICACAO_ATUAL']
        try:
            data_fim = max(d for d in dates if isinstance(d, pd.Timestamp))
        except ValueError:
            data_fim = ''

        rows.append({
            "CNPJ": cnpj,
            "ENTIDADE": nome,
            "PROTOCOLO_PROCESSO_MAIS_RECENTE": protocolo,
            "DT_PROTOCOLO": data,
            "TIPO_PROCESSO": tipo,
            "FASE_PROCESSO": etapa,
            "DT_FIM_CERTIFICACAO_ATUAL": data_fim
        })

    print(f'{len(rows)} entidadas cadastradas detectadas')
    return_df = pd.DataFrame(rows)
    return return_df


df = pd.read_excel('input/processos_cebas.xlsx')
sorted_df = df.sort_values(by=['CNPJ', 'DT_FIM_CERTIFICACAO_ATUAL'])


cnpj_df = listagem_de_entidades(sorted_df)
cnpj_df['STATUS_CEBAS'] = validade(cnpj_df)
cnpj_df.to_excel('output/status_cebas.xlsx', index=False)
