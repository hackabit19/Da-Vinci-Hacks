gloveFile = "glove.6B.50d.txt"
import numpy as np
import spacy

score=0

def loadGloveModel(gloveFile):
    print ("Loading Glove Model")
    with open(gloveFile, encoding="utf8" ) as f:
        content = f.readlines()
    model = {}
    for line in content:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print ("Done.",len(model)," words loaded!")
    return model

import re
from nltk.corpus import stopwords
import pandas as pd

def preprocess(raw_text):

    # keep only words
    letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)

    # convert to lower case and split 
    words = letters_only_text.lower().split()

    # remove stopwords
    stopword_set = set(stopwords.words("english"))
    cleaned_words = list(set([w for w in words if w not in stopword_set]))

    return cleaned_words

def cosine_distance_between_two_words(word1, word2):
    import scipy
    return (1- scipy.spatial.distance.cosine(model[word1], model[word2]))

def calculate_heat_matrix_for_two_sentences(s1,s2):
    s1 = preprocess(s1)
    s2 = preprocess(s2)
    result_list = [[cosine_distance_between_two_words(word1, word2) for word2 in s2] for word1 in s1]
    result_df = pd.DataFrame(result_list)
    result_df.columns = s2
    result_df.index = s1
    return result_df

def cosine_distance_wordembedding_method(s1, s2):
    import scipy
    global score
    vector_1 = np.mean([model[word] for word in preprocess(s1)],axis=0)
    vector_2 = np.mean([model[word] for word in preprocess(s2)],axis=0)
    cosine = scipy.spatial.distance.cosine(vector_1, vector_2)
    print('Word Embedding method with a cosine distance asses that our two sentences are similar to',round((1-cosine)*100,2),'%')
    if(round(1-cosine)==1):
        score += 10

def heat_map_matrix_between_two_sentences(s1,s2):
    df = calculate_heat_matrix_for_two_sentences(s1,s2)
    import seaborn as sns
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(5,5)) 
    ax_blue = sns.heatmap(df, cmap="YlGnBu")
    # ax_red = sns.heatmap(df)
    value = cosine_distance_wordembedding_method(s1, s2)
    return ax_blue

model = loadGloveModel(gloveFile)
spacy_nlp = spacy.load('en')
with open("a.txt")as f:
    arr1=[]
    for line in f:
     arr1.append(line)
with open("b.txt")as f:
    arr2=[]
    for line in f:
     arr2.append(line)
size = len(arr1)
for x in range(size):
 document1 = spacy_nlp(arr1[x])
 #document2 = spacy_nlp(arr2[x])

 #print (str(arr2[x]))
 marks = -1
 for element in document1.ents:
    s1 = str(element)
    s2 = str(arr2[x])
    if(s2.find(s1) == -1):
         marks=0;
         break;
      #if(str(element) not in str(arr2[x]))
         #marks = 0;
      #print(str(element))
    #print('Type: %s, Value: %s' % (element.label_, element))
 #for element in document1.ents:
    #print('Type: %s, Value: %s' % (element.label_, element))
 if(marks!=0):
       heat_map_matrix_between_two_sentences(arr1[x],arr2[x])
 else:
     score=score+0;

print(score);