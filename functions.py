from nltk.corpus import wordnet as wn
from collections import Counter
import semantic.dic2 as d

#import spacy
def chunck (x , num):
    arr = x.split('.')
    if num == 0:
        return arr[0] 
    else:
        return arr[1]
##################################################################################################################
def get_antoynm (x):
    prefix = []
    f=open("semantic/prefixes.txt", "r")
    prefix = f.readlines()
    
    for i in range(0 , len(prefix)-1):
        prefix[i] = prefix[i][:-1]  
    f.close()
    #print(prefix)
    dic_words , dic_ant = d.extract_more_antonyms()
    xx = [] 
    ant_a=[]
    ant_n=[]
    ant_v=[]
    temp = []
    for syn in wn.synsets(str(x)):
        xx.append(chunck(syn.name() , 0))  
    #print(xx)
    for synx in xx:
        for syn in wn.synsets(synx):
            for l in syn.lemmas(): 
                string = l.name()
                #print("jgdkgj" + string)
                if string in dic_words:
                    #print("morun1")
                    index = dic_words.index(string)
                    ant_v.append(dic_ant[index])
                    #print("!")
                    #print(dic_ant[index])
                                    #print(index)
                if string in dic_ant:
                     #print("morun2")
                     index = dic_ant.index(string)
                     ant_v.append(dic_words[index])
                     #print("!!")
                     #print(dic_words[index])
                     
                if l.antonyms(): 
                    i=0
                    while i < len(l.antonyms()):
                           n = chunck(str(l.antonyms()[i]) , 1)
                           if str(l.antonyms()[i].name()).startswith("re" , 0 , 2) and str(l.antonyms()[i].name()) in prefix:
                               string = str(l.antonyms()[i].name())
                               temp.append(string[2:])
                           elif (str(l.antonyms()[i].name()).startswith("un" , 0 , 2) or str(l.antonyms()[i].name()).startswith("ir" , 0 , 2) or str(l.antonyms()[i].name()).startswith("il" , 0 , 2) or str(l.antonyms()[i].name()).startswith("im" , 0 , 2) or str(l.antonyms()[i].name()).startswith("non" , 0 , 3) or str(l.antonyms()[i].name()).startswith("in" , 0 , 2)) and str(l.antonyms()[i].name()) in prefix:
                                   temp.append(str(l.antonyms()[i].name()))
                           else:
                               if n == "a" or n =="s":
                                   ant_a.append(l.antonyms()[i].name())
                               if n == "n":
                                   ant_n.append(l.antonyms()[i].name())
                               else:
                                   ant_v.append(l.antonyms()[i].name())
                           i+=1
                           

    
    
    #print(ant_a)
    #print(ant_n) 
    #print(ant_v)
    #print(temp)
    
    
    if len(ant_a) == 0 and len(ant_v) == 0 and len(ant_n) == 0 and len(temp) == 0 :
        return None
    else:
        if len(ant_a) >=1 and n!="v":
            c= Counter(ant_a)
            for i in c.elements():
                print(i , c[i])
                return i
            
        if len(ant_n) >=1 and n!="v" :
            c= Counter(ant_n)
            for i in c.elements():
                print(i , c[i])
                return i
         
        if len(ant_v) >=1:
            c= Counter(ant_v)
            for i in c.elements():
                print(i , c[i])
                return i
        else:
            ## read from the list of prefixes 
            c= Counter(temp)
            for i in c.elements():
                print(i , c[i])
                return i
   
#####################################################################################################################
