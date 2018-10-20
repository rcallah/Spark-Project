import pandas as pd
import operator
import urllib
import matplotlib as plt
from wordcloud import WordCloud as wc
import numpy as np
import sklearn

data = pd.read_csv("federal_sample_20170408.csv")
params = ['txt_link', 'alleged_pros_misconduct', 'misconduct_determination']
new = data[params]
data = pd.DataFrame(data)
data['misconduct_determination'] = data[data.misconduct_determination.str.strip() != 'no misconduct']



conduct_cases = data[pd.notnull(data['misconduct_determination'])].values
conduct_cases = [i[0] for i in conduct_cases]
#data = data.reset_index()

data['outcome'] = 0
for index, x in data.iterrows():
	if x['orig_pdf'] in conduct_cases:
		data['outcome'].loc[index] = 1


#print(data.keys())
#print(data.loc[1])

df = data[['orig_pdf', 'outcome']]
df['aleg_terms'] = data[['allegation_term_1', 'allegation_term_2', 'allegation_term_3', 'allegation_term_4', 'allegation_term_5', 'allegation_term_6']].values.tolist()
#print(df['aleg_terms'])
from sklearn.feature_extraction.text import TfidfVectorizer
vec = TfidfVectorizer()
df['aleg_terms'] = [[str(val) for val in sublist] for sublist in df['aleg_terms'].values]
df['aleg_terms'] = [' '.join(val) for val in df['aleg_terms'].values]

out = vec.fit_transform(df['aleg_terms'].values)
ret = pd.DataFrame(out.toarray(), columns=vec.get_feature_names())

df['aleg_terms'] = ret.values.tolist()
tfid = ret.values.tolist()


X_train = tfid[0:400]
y_train = df['outcome'].values.tolist()[0:400]
X_test = tfid[400:]
y_test = df['outcome'].values.tolist()[400:]

from sklearn.linear_model import LogisticRegressionCV
clf = LogisticRegressionCV(random_state=0, solver='lbfgs', multi_class='multinomial').fit(X_train, y_train)
preds = clf.predict(X_test)
probs = clf.predict_proba(X_test) 
score = clf.score(X_test, y_test)
print(score)

