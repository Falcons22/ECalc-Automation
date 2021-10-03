import numpy
import pandas as pd

file = pd.read_excel('prop.xlsx')
data = pd.DataFrame(file)

for row in data:
    print(row[0], row[1])