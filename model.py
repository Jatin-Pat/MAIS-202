# imports
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix
import spacy
from spacy import displacy
import re

# read in the data as pandas dataframe and initialize spacy language
data = pd.read_csv('https://raw.githubusercontent.com/Jatin-Pat/MAIS-202/main/data.csv', names = ['classification', 'text'], encoding ='latin1')
nlp = spacy.load('en_core_web_sm')


def dataset_balancing(df):
  """ 
  dataset (pandas DataFrame) -> balanced dataset (pandas DataFrame)

  Performs undersampling on dataset and returns the balanced dataset
  """
  balanced_dataset = []
  neutral_classification_count = 0
  positive_classification_count = 0

  for i, classification in enumerate(data['classification']):
    if classification == 'neutral':
      neutral_classification_count += 1
      if neutral_classification_count < df['classification'].value_counts().min():
        balanced_dataset.append(data.iloc[i])

    elif classification == 'positive':
      positive_classification_count += 1
      if positive_classification_count < df['classification'].value_counts().min():
        balanced_dataset.append(data.iloc[i])
    
    else:
      balanced_dataset.append(data.iloc[i])
    
  balanced_dataset = ((pd.DataFrame(balanced_dataset)).sample(frac = 1)).reset_index()
  del balanced_dataset['index']

  return balanced_dataset


balanced_data = dataset_balancing(data)
print(balanced_data['classification'].value_counts())

def preprocess_classification_data(df):
  """
  dataset (pandas DataFrame) -> dataset (pandas DataFrame)

  Returns dataset with quantified labels
  """
  labels = {
      'negative': 0,
      'neutral': 1,
      'positive': 2
      }
  return df['classification'].replace(labels)

def preprocess_text_data(df):
  """
  dataset (pandas DataFrame) -> dataset (pandas DataFrame)

  Returns dataset with punctuation and capitalization removed

  """
  for i in range(len(df.index)):
    text = re.sub(r"[,.;@#?!&$]+\ *", " ", df[i])
    df[i] = text.lower()
  return df

# initializing train and test split
vectorizer = TfidfVectorizer(min_df=.001)
features = vectorizer.fit_transform(preprocess_text_data(balanced_data['text']))
train_vec, test_vec, train_classification, test_classification = train_test_split(features, preprocess_classification_data(balanced_data), train_size=.9, test_size=.1)  

# model creation and metric evaluation
classifier = MultinomialNB()
classifier.fit(train_vec, train_classification)
print(accuracy_score(test_classification, classifier.predict(test_vec)))
print(confusion_matrix(test_classification, classifier.predict(test_vec)))


def prediction(article):
  """
  article (str) -> prediction (str)

  Performs prediction on article and gathers named entity
  """
  if article == "" or len(nlp(article).ents) == 0:
    return "No named entity found.", "[1]"

  pred = classifier.predict(vectorizer.transform([article.replace("[',-@/'`$#%&*()+,]", "")]))
  if pred == [0]:
    return_message = "The article has a negative outlook towards " 
  elif pred == [1]:
    return_message = "The article has a neutral outlook towards "
  else:
    return_message = "The article has a positive outlook towards "

  return (return_message + str((nlp(article).ents[0]))), str(pred)
