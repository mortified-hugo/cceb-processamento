import re
import pandas as pd
from datetime import datetime as dt


def drop(to_alter, args, column):
    df = to_alter
    for arg in args:
        df = df.drop(df[df[column] == arg].index)
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








