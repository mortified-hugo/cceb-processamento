import json
import pandas as pd
import pathlib
from datetime import datetime

from diligência.email_function import send_email


hoje = format(datetime.now(), "%d.%m.%Y")

with open("emails/analistas.json", mode='r') as file:
    analistas = json.load(file)
    analistas["Karine Gonçalves de Souza"] = analistas['Karine GonÃ§alves de Souza']

print(analistas)
df = pd.read_excel(f'output/diligência_{hoje}.xlsx')
for analista in set(df["Análise Macro Analisada por:"]):
    diligencias = f'output/for_emails/diligência_{analistas[analista]["nome"]}_{hoje}.xlsx'
    df[df["Análise Macro Analisada por:"] == analista].to_excel(
        diligencias)
    send_email('hugo.figueira@cidadania.gov.br',
               f"Tramitação de Processos LECOM - Resposta de Diligência - {hoje}",
               f"Bom dia {analistas[analista]['nome']},\n\n"
               f"Segue em anexo tramitação de processos com resposta de diligência:\n\n"
               f"Att,\n"
               f"Hugo",
               str(pathlib.Path(diligencias).resolve()))
    print(str(pathlib.Path(diligencias).resolve()))

print("Emails enviados")




