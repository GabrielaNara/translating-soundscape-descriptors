import pandas as pd
import re
import spacy
import nltk

# import csv
data = pd.read_csv('data-filtered.csv')

# agroup strings
string = " ".join(data['text'])

############### Cleaning data process ##################
##################  FOR ENGLISH  #######################
########################################################
spc_en = spacy.load("en_core_web_sm")

#example
#text = "He determined to drop his litigation with the monastry, and relinguish his claims to the wood-cuting and fishery rihgts at once. He was the more ready to do this becuase the rights had become much less valuable, and he had indeed the vaguest idea where the wood and river in question were."

def clean_text_en(text):
    # Remove characters that aren't letters and run the "tokenization" process
    letters =  re.findall(r'\b[A-zÀ-úü]+\b', text.lower())
    
    # Defining stopwords
    stopwords = nltk.corpus.stopwords.words('english')
    #stopwords = set(stopwords.words('english'))
    meaningful_words = [w for w in letters if w not in stopwords]
    meaningful_words_string = " ".join(meaningful_words)
    
    # Creating the object spacy
    spc_letters =  spc_en(meaningful_words_string)
    
    # Lemmatization 
    tokens = [token.lemma_ if token.pos_ == 'VERB' else str(token) for token in spc_letters]
    
    return tokens

strg = []
# Generate tokens
for i in data['text']:
    words = clean_text_en(i)
    strg += [", ".join(words)]
    
data['words'] = strg
data.to_csv('data-tweets-nlp.csv')
