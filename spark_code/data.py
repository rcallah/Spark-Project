import pandas as pd
import operator
import urllib
from wordcloud import WordCloud as wc
import numpy as np
import sklearn

data = pd.read_csv("federal_sample_20170408.csv")
params = ['txt_link', 'alleged_pros_misconduct', 'misconduct_determination']
new = data[params]
data = pd.DataFrame(data)
#print(data['misconduct_determination'].iloc[:50])
#data['misconduct_determination'] = data[data.misconduct_determination.str.strip() != 'no misconduct']
#print(data.keys())
#print(data['misconduct_determination'].iloc[:10])

#conduct_cases = data[pd.notnull(data['misconduct_determination'])]
#print(np.unique(conduct_cases['misconduct_determination']))

misconduct_terms = [' no misconduct', 'REVIEW', 'harmless error/no misconduct',
 'harmless error/no misconduct?', 'harmless error/no misconduct??','motion denied' ,
 'no misconduct', 'no misconduct(see notes)', 'no misconduct/harmless error',
 'no misconduct/harmless error??', 'no misconduct/harmless error???','prejudicial', 'prejudicial ',
 'prejudicial error', 'prejudicial misconduct', 'procedurally barred','procedurally barred // no misconduct','remand for evidentiary hearing']

remove_terms = ['no determinatation','no determination', 'na','no ruling', 'no ruling???', 'not determined','procedurally defaulted', 'time-barred (did not determine)']


data['new_outs'] = 0
drop = []
for index, x in data.iterrows():
	if x['misconduct_determination'] in misconduct_terms:
		data['new_outs'].iloc[index] = 0
	elif x['misconduct_determination'] in remove_terms:
		drop.append(index)
	else:
		data['new_outs'].iloc[index] = 1


nulls = pd.isna(data['misconduct_determination'])
to_drop = []
for x in range(len(nulls)):
	if nulls[x] == True:
		to_drop.append(x)


data = data.drop(drop)
data = data.drop(to_drop)
data = data.reset_index()

"""
conduct_cases = [i[0] for i in conduct_cases]
#data = data.reset_index()
data['outcome'] = 0
for index, x in data.iterrows():
	if x['orig_pdf'] in conduct_cases:
		data['outcome'].loc[index] = 1
"""
data['outcome'] = data['new_outs']
#print(data['new_outs'])

#miscons = data[data['outcome'] == 1]
#print(len(miscons))

#print(data.keys())
df = data[['orig_pdf', 'outcome']]
df['aleg_terms'] = data[['allegation_term_1', 'allegation_term_2', 'allegation_term_3', 'allegation_term_4', 'allegation_term_5', 'allegation_term_6']].values.tolist()
df['deter_terms'] = data[['misconduct_determination_term1', 'misconduct_determination_term2', 'misconduct_determination_term3', 'misconduct_determination_term4', 'misconduct_determination_term5', 'misconduct_determination_term6']].values.tolist()
df['comb'] = ([a + b for a, b in zip(df['aleg_terms'].values.tolist(), df['deter_terms'].values.tolist())])


#print(df['deter_terms'])
#print(df['aleg_terms'])
from sklearn.feature_extraction.text import TfidfVectorizer
vec = TfidfVectorizer()
df['aleg_terms'] = [[str(val) for val in sublist] for sublist in df['aleg_terms'].values]
df['aleg_terms'] = [' '.join(val) for val in df['aleg_terms'].values]

df['deter_terms'] = [[str(val) for val in sublist] for sublist in df['deter_terms'].values]
df['deter_terms'] = [' '.join(val) for val in df['deter_terms'].values]

df['comb'] = [[str(val) for val in sublist] for sublist in df['comb'].values]
df['comb'] = [' '.join(val) for val in df['comb'].values]


#print(df['deter_terms'])
#print(df['aleg_terms'])


out = vec.fit_transform(df['aleg_terms'].values)
ret = pd.DataFrame(out.toarray(), columns=vec.get_feature_names())

out2 = vec.fit_transform(df['deter_terms'].values)
ret2 = pd.DataFrame(out2.toarray(), columns=vec.get_feature_names())

out3 = vec.fit_transform(df['comb'].values)
ret3 = pd.DataFrame(out3.toarray(), columns=vec.get_feature_names())

df['deter_terms'] = ret2.values.tolist()
tfid2 = ret2.values.tolist()

df['comb'] = ret3.values.tolist()
tfid3 = ret3.values.tolist()

df['aleg_terms'] = ret.values.tolist()
tfid = ret.values.tolist()

#print(np.shape(tfid))
#print(np.shape(tfid2))
#print(np.shape(tfid3))

X_train = tfid[0:275]
y_train = df['outcome'].values.tolist()[0:275]
X_test = tfid[275:]
y_test = df['outcome'].values.tolist()[275:]

from sklearn.linear_model import LogisticRegressionCV
clf = LogisticRegressionCV(random_state=0, solver='lbfgs', multi_class='multinomial').fit(X_train, y_train)
preds = clf.predict(X_test)
probs = clf.predict_proba(X_test)


import matplotlib.pyplot as plt

score = clf.score(X_test, y_test)
print(score)
yes = score
no = 1-score
chart = [yes, no]
labels = [r'Correct - 80.2%', r'Incorrect - 19.8%']
patches, texts = plt.pie(chart)
plt.legend(patches, labels, loc="best")
#plt.pie(chart)
plt.show()
