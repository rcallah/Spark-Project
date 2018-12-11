import pandas as pd
import string
import textract
import requests
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.stem import PorterStemmer

data = pd.read_csv('federal_sample_20170408 - federal_sample_20170408.csv')

data = data[data['new_misconduct_determination'].notnull()]
data['new_misconduct_determination'] = data['new_misconduct_determination'].str.strip()
data['new_misconduct_determination'] = data['new_misconduct_determination'].str.lower()
data = data.replace('na', 'no')

if len(set(data['new_misconduct_determination'])) == 2:
    
    data = data[['txt_link', 'new_misconduct_determination']]
    data = data.replace('yes', 1)
    data = data.replace('no', 0)
    
    nltk_stopwords = stopwords.words('english')
    custom_stopwords = set(w.rstrip() for w in open('stopwords.txt'))
    stopwords = custom_stopwords.union(nltk_stopwords)
    
    data_to_export = pd.DataFrame(columns=['case_text', 'misconduct'])
    
    def preprocessing(text):
        
        text2 = ' '.join(''.join([' ' if ch in string.punctuation else ch for ch in text]).split())
        tokens = [word for sent in nltk.sent_tokenize(text2) for word in nltk.word_tokenize(sent)]
        tokens = [word.lower() for word in tokens]
        tokens = [token for token in tokens if token not in stopwords]
        tokens = [word for word in tokens if len(word) >= 3]
        
        # stemmer = PorterStemmer()
        # tokens = [stemmer.stem(word) for word in tokens]
        
        tokens = [t for t in tokens if not any(c.isdigit() for c in t)]
        tagged_corpus = pos_tag(tokens)
        
        Noun_tags = ['NN','NNP','NNPS','NNS']
        Verb_tags = ['VB','VBD','VBG','VBN','VBP','VBZ']
        
        lemmatizer = WordNetLemmatizer()
        
        def prat_lemmatize(token,tag):
            if tag in Noun_tags: return lemmatizer.lemmatize(token, 'n')
            elif tag in Verb_tags: return lemmatizer.lemmatize(token, 'v')
            else: return lemmatizer.lemmatize(token,'n')
            
        pre_proc_text = ' '.join([prat_lemmatize(token,tag) for token,tag in tagged_corpus])
        
        return pre_proc_text

    for i, row in data.iterrows():
        url = row['txt_link']
        if "https://drive.google.com" in url:
            file_id = url[41: -18]
            url = 'https://drive.google.com/a/bu.edu/uc?id=' + file_id +'&export=download'
            res = requests.get(url)
            open(file_id + '.rtf', 'wb').write(res.content)
            text = textract.process(file_id + '.rtf')
            # call to preprocessing function can be deleted to have original text
            data_to_export = data_to_export.append({'case_text': preprocessing(text.decode()), 'misconduct': row['new_misconduct_determination']}, ignore_index=True)
        else:
            res = requests.get(url)
            data_to_export = data_to_export.append({'case_text': preprocessing(res.text), 'misconduct': row['new_misconduct_determination']}, ignore_index=True)

    data_to_export.to_csv('preprocessed_data.csv', index=False)