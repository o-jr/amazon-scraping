# Vamos importar o que precisamos
import pandas as pd
import sqlite3
from datetime import datetime
import os
import json


#basePath = os.path.dirname(os.path.abspath(__file__))
#df = pd.read_json(basePath + '../data/data.json', lines=True, orient = 'records')
# Definir o caminho para o arquivo JSONL
df = pd.read_json('../data/data.json', lines=True)

print(df)