import spacy
#from nltk.stem.lancaster import LancasterStemmer
#from spacy.lemmatizer import Lemmatizer
from nltk.stem import PorterStemmer
import semantic.syn_dic as synonyms

def get_score(sentence1 , sentence2 , modelans_features , studentans_features):
    c2=[]
    c1 = []
    c3=[]
    ps = PorterStemmer() 
    nlp = spacy.load('en_core_web_sm')
    colors = ["white" , "black" , "blue" ,"red" ,  "yellow" , "green" ,\
                  "pink" , "mouve" , "gray" , "grey","violet" , "violette" , "purple" , "brown"]

    synonyms_lists = synonyms.more_syns()
    doc1 = nlp(sentence1)
    for token in doc1:
        if str(token) in colors:
            v = str(token.head.text)
            if v != "animal" and v != "animals":
                v = ps.stem(v)
        
                #print(v)
            string = str(token) + " " + v
            c1.append(string)
    
    
    doc2 = nlp(sentence2)
    for token in doc2:
        #print(token.text, token.dep_, token.head.text, token.head.pos_, [child for child in token.children])
        if str(token) in colors:
            v = str(token.head.text)
            if v != "animal" and v != "animals":
                v = ps.stem(v)
                #print(v)
            flag = False
            for i in range ( 0 , 40):
                if v in synonyms_lists[i]:
                    #print(synonyms_lists[i])
                    #print(v)
                    string = str(token) + " " + v
                    c2.append(string)
                    for j in range ( 0 , len(synonyms_lists[i])):
                        #print(synonyms_lists[i][j])
                        string = str(token) + " " + synonyms_lists[i][j]
                        c3.append(string)
                        flag =True
                    break
            if not flag:
                 string = str(token) + " " + v
                 c2.append(string)
                 c3.append(string)
                 
    score = 0  
    print(c1)
    print(c2)   
    print(c3)   
    for i in range( 0 , len(c1)):
        str_list = c1[i].split(" ")
        modelans_features.append((str_list[0] , 1))
        modelans_features.append((str_list[1] , 1))
        for j in range ( 0 , len(c3)):
            if c1[i] == c3[j]:
                score+=1
                break
            
    score = score / len(c1)
    okay = []
    lo = False
    
    for i in range (0 , len(c1)):
        stri = c1[i].split(" ")
        st1 = stri[1]   # dogs , animals
        st0 = stri[0]   # red , white , blue
        for j in range ( 0 , 40):
            if st1 in synonyms_lists[j]:
                for k in range ( 0 ,len(synonyms_lists[j])):
                    t = st0 + " " + synonyms_lists[j][k]
                    if t in c2:
                        okay.append(t)
                        studentans_features.append((st0 , 1))
                        studentans_features.append((synonyms_lists[j][k] , 1))
                        lo = True
                        break
                if lo :
                    break
    print(okay)
    for l in range ( 0 , len(c2)):
        if c2[l] not in okay and c2[l] not in c1:
            stri = c2[l].split(" ")
            st1 = stri[1]   # dogs , animals
            st0 = stri[0]   
            studentans_features.append((st0 , 0))
            studentans_features.append((st1 , 0))
            
        elif c2[l] not in okay and c2[l] in c1:
            stri = c2[l].split(" ")
            st1 = stri[1]   # dogs , animals
            st0 = stri[0]   
            studentans_features.append((st0 , 1))
            studentans_features.append((st1 , 1))
                      
    return score
