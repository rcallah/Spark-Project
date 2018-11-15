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

print(data.keys())

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


""" USING TFID VECTORIZATION """
"""
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


X_train = tfid3[0:275]
y_train = df['outcome'].values.tolist()[0:275]
X_test = tfid3[275:]
y_test = df['outcome'].values.tolist()[275:]
"""
"""    	END TFID VECTORIZATION				"""


""" 	USING COUNT VECTORIZATION """

from sklearn.feature_extraction.text import CountVectorizer
vec = CountVectorizer()


count = vec.fit_transform(df['aleg_terms'].values)
count = pd.DataFrame(count.toarray(), columns=vec.get_feature_names())
cvec = count.values.tolist()

count2 = vec.fit_transform(df['deter_terms'].values)
count2 = pd.DataFrame(count2.toarray(), columns=vec.get_feature_names())
cvec2 = count2.values.tolist()

count3 = vec.fit_transform(df['comb'].values)
count3 = pd.DataFrame(count3.toarray(), columns=vec.get_feature_names())
cvec3 = count3.values.tolist()


X_train = cvec3[0:275]
y_train = df['outcome'].values.tolist()[0:275]
X_test = cvec3[275:]
y_test = df['outcome'].values.tolist()[275:]


"""			END COUNT VECTORIZATION					"""



""" 	USING MULTI DIMENSIONAL SCALING		"""
from sklearn.manifold import MDS

"""
embedding = MDS(n_components=1)

#X_trans = embedding.fit_transform(X_train)
#X_test_trans = embedding.fit_transform(X_test)
x_aleg = embedding.fit_transform(cvec)
x_deter = embedding.fit_transform(cvec2)
x_mds_comb = [np.append(a, b) for a,b in list(zip(x_aleg, x_deter))]
X_train = x_mds_comb[0:275]
X_test = x_mds_comb[275:]
"""

"""			END MULTI DIMENSIONAL SCALING 		"""





"""		USING SUPPORT VECTOR MACHINE	"""
#embedding = MDS(n_components=50)
#X_train = embedding.fit_transform(X_train)
#X_test = embedding.fit_transform(X_test)
"""
from sklearn.svm import SVC
clf = SVC(gamma='auto')
clf.fit(X_train, y_train)
#clf.fit(X_trans, y_train) #MDS set
SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
    decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
    max_iter=-1, probability=False, random_state=None, shrinking=True,
    tol=0.001, verbose=False)
print(clf.predict(X_test))
#pred = clf.predict(X_test_trans) #mds
score2 = clf.score(X_test, y_test)
#score2 = clf.score(X_test_trans, y_test) #mds
print(score2)
"""

"""			END SUPPORT VECTOR MACHINE			"""



"""		USING LOGISTIC REGRESSION 		"""

from sklearn.linear_model import LogisticRegressionCV
clf = LogisticRegressionCV(random_state=0, solver='lbfgs', multi_class='multinomial').fit(X_train, y_train)
preds = clf.predict(X_test)
probs = clf.predict_proba(X_test)
score = clf.score(X_test, y_test)
print(score)


"""		END LOGISTIC REGRESSION			"""




""" 	USING RAINFOREST CLASSIFIER 	"""
#cvec = aleg
#cvec2 = deter
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
clf = RandomForestClassifier(n_estimators=100, max_depth=2,
                              random_state=0)
clf.fit(X_train, y_train)
RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=2, max_features='auto', max_leaf_nodes=None,
            min_impurity_decrease=0.0, min_impurity_split=None,
            min_samples_leaf=1, min_samples_split=2,
            min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=None,
            oob_score=False, random_state=0, verbose=0, warm_start=False)
print(clf.feature_importances_)
print(clf.predict(X_test))
print(clf.score(X_test, y_test))
"""
"""			END RAINFOREST CLASSIFIER			"""






import matplotlib.pyplot as plt

score = clf.score(X_test, y_test)
print(score)
yes = score
no = 1-score
chart = [yes, no]
labels = [r'Correct - ' + str(round(yes, 3)), r'Incorrect - ' + str(round(no, 3))]
patches, texts = plt.pie(chart)
plt.legend(patches, labels, loc="best")
#plt.pie(chart)
plt.show()



"""
Results:
tfid aleg = 80.2%
tfid deter = 80.2%
tfid comb = 80.2%
count aleg = 80.2%
count deter = 80.2%
count comb = 83.5%
rainforest w/ MDS = 80.2%
rainforest w/out MDS = 80.2%
SVM - count - MDS 1 = 76%
SVM - comb - count - MDS 5 = 80.2%
SVM - aleg - count - MDS 1 = 80.2%
"""

#TRY USING MDS TO REDUCE ALEG AND DETER INDIVIDUALLY