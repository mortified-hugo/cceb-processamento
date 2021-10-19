import pandas as pd
from oferta_functions import ofertas_access_column
from lecom_para_quickview.lecom_functions import drop
from functions.functions import preparar_excel


ofertas_lecom = pd.read_excel("input/ofertas_e_usuarios_lecom.xlsx")
ofertas_df = pd.read_excel("input/access.xlsx", index_col="PROTOCOLO")
ofertas_df_clean = drop(ofertas_df,["Supervisão Extraordinária",
                                    "Representação",
                                    "Importação",
                                    "Recurso de Revisão",
                                    "Recurso MPS",
                                    "Reconsideração",
                                    "Revisão",
                                    "Supervisão",
                                    "Supervisão Ordinária"],
                        "TIPO_PROCESSO")


new_ofertas_df = ofertas_access_column(ofertas_df_clean)
final_ofertas_df = ofertas_lecom.append(new_ofertas_df)
final_ofertas_df = drop(final_ofertas_df,[0],"Número de Ofertas")

final_ofertas_df.to_excel('output/ofertas_e_usuarios.xlsx', index=False)
preparar_excel('output/ofertas_e_usuarios.xlsx')
