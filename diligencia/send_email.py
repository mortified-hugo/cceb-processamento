import json
import pandas as pd
import pathlib
from datetime import datetime
from functions.functions import preparar_excel, comprimento

from diligencia.email_function import send_email


hoje = format(datetime.now(), "%d.%m.%Y")
comp = comprimento()

with open("emails/analistas.json", mode='r') as file:
    analistas = json.load(file)
    analistas["Karine Gonçalves de Souza"] = analistas['Karine GonÃ§alves de Souza']

try:
    df = pd.read_excel(f'output/diligencia_{hoje}.xlsx')

    for analista in set(df["Análise Macro Analisada por:"]):
        diligencias = f'output/for_emails/diligencia_{analistas[analista]["nome"]}_{hoje}.xlsx'
        df[df["Análise Macro Analisada por:"] == analista].to_excel(
            diligencias,
            index=False)
        preparar_excel(diligencias)
        send_email(analistas[analista]["email"],
                   f"Tramitação de Processos LECOM - Resposta de Diligência - {hoje}",
                   f"{comp} {analistas[analista]['nome']},\n\n"
                   f"Segue em anexo tramitação de processos com resposta de diligência:\n\n"
                   f"Att,\n"
                   f"Hugo",
                   str(pathlib.Path(diligencias).resolve()))

    print("Emails enviados")

except FileNotFoundError:
    print("DILIGÊNCIAS NÃO ENCONTRADAS")









