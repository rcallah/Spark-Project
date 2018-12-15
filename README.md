# Nationwide Investigation of Federal Prosecutors

This is a Natural Language Processing (NLP) & Supervised Machine Learning (ML) problem to determine if there is a prosecutor misconduct involved in a federal prosecutor case. We have a dataset of 624 labeled cases (467 are "no misconduct" & 157 "misconduct" cases) of which we use 80% to train the model and 20% to validate the model respectfully. We use StratifiedKFold cross-validator to ensure an equal distribution of both "misconduct" and "no misonduct" cases in the training & testing process. We have tried Logistic Regression, Random Forest, Support Vector Machine (SVM), Recurrent Neural Network (RNN) and Convolutional Neural Network (CNN) to solve this problem. As the result of comparing, Logistic Regression model could achieve 80% accuracy which is the highest.

# Implementations
- [Logistic Regression, Random Forest, Support Vector Machine (SVM)](./final_code/README.md)
- [Recurrent Neural Network (RNN)](./spark_code/neural_net/rnn.ipynb)
- [Convolutional Neural Network (CNN)](./spark_code/neural_net/cnn.ipynb)
- [Preprocessing](./spark_code/neural_net/preprocessing)

# Tools
- [Keras](https://keras.io)
- [scikit-learn](https://scikit-learn.org)
- [Natural Language Toolkit](https://www.nltk.org)
- [GloVe](https://nlp.stanford.edu/projects/glove)
- [textract](https://textract.readthedocs.io)
- [Google Colaboratory](https://colab.research.google.com)

# Requirements
 - pandas >= 0.23.4
 - numpy >= 1.14.5
 - wordcloud >= 1.5.0
 - matplotlib >= 3.0.0
 - scikit_learn >= 0.20.1
 - download [glove.6B.zip](http://nlp.stanford.edu/data/glove.6B.zip)
 - install [textract](https://textract.readthedocs.io/en/stable/installation.html)