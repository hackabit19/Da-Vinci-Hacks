import nltk
import string
import nltk
import pickle
import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def text_prepare(text):
    """Performs tokenization and simple preprocessing."""
    
    replace_by_space_re = re.compile('[/(){}\[\]\|@,;]')
    bad_symbols_re = re.compile('[^0-9a-z #+_]')
    stopwords_set = set(stopwords.words('english'))

    text = text.lower()
    text = replace_by_space_re.sub(' ', text)
    text = bad_symbols_re.sub('', text)
    text = ' '.join([x for x in text.split() if x and x not in stopwords_set])
    return text.strip()

def get_output(q_no,answer):
    student_response=text_prepare(answer)
    with open("a.text") as f:
        real=[]
        for line in f:
            real.append(line)
    text = word_tokenize(text_prepare(str(real[q_no])))
    text2=word_tokenize(student_response)
    f=nltk.pos_tag(text)
    f2=nltk.pos_tag(text2)
    noun_preceders = [a for (a, b) in f if b=='NNP' or b=='NN' or b=='NNS' ]
    adj_preceders = [a for (a, b) in f if b=='JJ' or b=='JJR' or b=='JJS']
    adj_preceders2 = [a for (a, b) in f2 if b=='JJ' or b=='JJR' or b=='JJS']
    score=0.0
    for n in noun_preceders:
        if n not in student_response:
            pass
        else:
            score=score+5/len(noun_preceders)
    print(score)
    from nltk.corpus import wordnet
    nltk.download('wordnet')
    synonyms=[]
    antonyms=[]
    for i in range(len(adj_preceders)):
        for syn in wordnet.synsets(adj_preceders[i]):
            for l in syn.lemmas():
                synonyms.append(l.name())

    print(set(synonyms))
    for i in range(len(adj_preceders2)):
        if(adj_preceders2[i] in synonyms):
            print("sahi h")
            score=score+3/len(adj_preceders2)
        else:
            print("sahi nhi h")
            pass
    return score
