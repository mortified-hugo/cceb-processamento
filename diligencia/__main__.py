import pandas as pd
from datetime import datetime
from glob import glob
from functions.functions import preparar_excel


file = glob('input/*.xlsx')[-1]


def preparar_diligencia(diligencia, file):
    hoje = format(datetime.now(), "%d.%m.%Y")

    df = pd.read_excel(file, sheet_name=0, skiprows=[0, 1],
                       usecols=['#Processo',
                                'Etapa atual',
                                'Análise Macro Analisada por:',
                                ' Data da Requisição',
                                'PROTOCOLO',
                                'CNPJ:',
                                'Nome da Organização: (como está no CNPJ)',
                                'Tipo:'])

    df.to_excel(f'output/{diligencia}_{hoje}.xlsx', index=False)
    preparar_excel(f'output/{diligencia}_{hoje}.xlsx')
    

preparar_diligencia("diligencia", file)
