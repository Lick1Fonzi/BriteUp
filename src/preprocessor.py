import string
import nltk
from nltk.corpus import stopwords
#nltk.download('book')
#nltk.download('stopwords')
#nltk.download('omw-1.4')
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import wordnet as wn

def preprocess_query(query):
        RELOP = {'OR','AND','(',')',':','url','content','event'}
        q = []
        for word in query.split():
                for op in RELOP:
                        if op not in word:
                                q.append(preprocess(word))
                        else:
                                q.append(word)
        return ' '.join(q)

def preprocess(text):
    tokens = tokenize(text.lower())
    tokens = removePunctuation(tokens)
    tokens = removeStopWords(tokens)
    tokens = lemmatize(tokens)
    #tokens = stem(tokens)
    return ' '.join(tokens)

def removePunctuation(tokens):
        exclude = set(string.punctuation)
        return [x for x in tokens if x not in exclude]

def removeStopWords(tokens):
    return [x for x in tokens if (x not in stopwords.words('english') or x not in stopwords.words('italian'))]

def tokenize(text):
    return nltk.word_tokenize(text.lower())

#Funzione lemmatizzatrice, riceve lista di tokens e restituisce lista di lemmi senza stopwords
def lemmatize(tokens):
    lemmatizer = nltk.WordNetLemmatizer()
    return [lemmatizer.lemmatize(t) for t in tokens]

#Funzione Stemmer using Lancaster/Porter, restituisce lista con stem di lista di tokens passati come parametro
def stem(tokens):
    lancaster = LancasterStemmer()
    return [lancaster.stem(t) for t in tokens]

#Function that tags every token passed as parameter and returns them in a list of tuples(token,tag)
def tag(self,tokens):
    return nltk.pos_tag(tokens)
    
#Function disambiguating the terms passed as parameters, determining the right sense using wupalmer similarity
def disambiguateTerms(self,terms):
    for t_i in terms:    # t_i is target term
            selSense = None
            selScore = 0.0
    #        print(wn.synsets(t_i,wn.NOUN))
            for s_ti in wn.synsets(t_i, wn.NOUN):
                    score_i = 0.0
                    for t_j in terms:    # t_j term in t_i's context window
                            if (t_i==t_j):
                                    continue
                            bestScore = 0.0
                            for s_tj in wn.synsets(t_j, wn.NOUN):
                                    tempScore = s_ti.wup_similarity(s_tj)
                                    if (tempScore>bestScore):
                                            bestScore=tempScore
                            score_i = score_i + bestScore
                    if (score_i>selScore):
                            selScore = score_i
                            selSense = s_ti
            if (selSense is not None):
                    print(t_i,": ",selSense,", ",selSense.definition())   
                    print("Score: ",selScore)
            else:
                    print(t_i,": --")
