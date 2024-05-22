import pandas as pd
import re

log_file_path = 'C:\\Users\eroshevich_d\PycharmProject\pythonProject\logs.json'
data = []

with open(log_file_path, 'r', encoding='UTF-8') as log_file:
    lines = log_file.readlines()

for line in lines:
    try:
        new_line = re.sub(r'on \d+: ', '', line)
        row_dict = eval(new_line.strip())
        data.append(row_dict)
    except NameError:
        pass

df = pd.DataFrame(data)

df.to_excel('C:\\Users\eroshevich_d\PycharmProject\pythonProject\logs\logs.xlsx', index=False)
