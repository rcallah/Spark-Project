import pandas as pd
import operator
import urllib
import matplotlib as plt
from wordcloud import WordCloud as wc
import numpy as np

data = pd.read_csv("federal_sample_20170408.csv")
params = ['txt_link', 'alleged_pros_misconduct', 'misconduct_determination']
new = data[params]
data = pd.DataFrame(data)
data['misconduct_determination'] = data[data.misconduct_determination.str.strip() != 'no misconduct']


data = data[pd.notnull(data['misconduct_determination'])]
print(data.head())
data = data.reset_index()
print(data['misconduct_determination'])
