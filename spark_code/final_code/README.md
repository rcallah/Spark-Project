# About

This algorithm uses logistic regression on our dataset to try and predict if there is prosecutor misconduct in a federal prosecutor case. We have a dataset of ~500 labeled cases of which we split 75%-25% into training and test respectfully. With this said, the algorithm achieves an accuracy of 80%.

# How to run
1. Open spark_code -> final_code folder
2. Run data.py script
   ```
   cd spark_code
   cd final_code
   python data.py
   ```

# Understanding the source code
The script contains Machine Learning algorithms such as Support Vector Machine, Logistic Regression and Rainforest Classifier. They are commented in the script. So, in order to try them separately, please comment them out. There are also 2 types of vectorization is used such as TFID VECTORIZATION and COUNT VECTORIZATION. Please, comment them out in order to use.

## Requirements
 - pandas >= 0.23.4
 - numpy >= 1.14.5
 - wordcloud >= 1.5.0
 - matplotlib >= 3.0.0
 - scikit_learn >= 0.20.1