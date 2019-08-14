from nltk.corpus import wordnet as wn
import spacy
import semantic.rule_preprocess as fun1
from decimal import Decimal
import semantic.dic2 as d
import semantic.syn_dic as sy
import semantic.numbers_semantic as nums

def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'
 
    if tag.startswith('V'):
        return 'v'
 
    if tag.startswith('J'):
        return 'a'
 
    if tag.startswith('R'):
        return 'r'
 
    return 'n'
 
def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
    #print(str(wn.synsets(word, wn_tag)[0]))
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None 

def sentence_similarity(sentence1, sentence2 , names , countries , cities , numbers , modelans_features , studentans_features):
    nlp = spacy.load('en_core_web_sm')
    filtered_sentence1 = []
    filtered_sentence2 = []
    if ',' in sentence1:
        sentence1=sentence1.replace(',','')
    if '.' in sentence1:
        sentence1=sentence1.replace('.','')
    if '.' in sentence2:
        sentence2=sentence2.replace('.','')
    if ',' in sentence2:
        sentence2 = sentence2.replace(',','')
    dic_words , dic_ant = d.extract_more_antonyms()
    abbrev = ["centimeter" , "kilometer" , "meter" , "seconds" , "milligram" , "gram" , "liter" ,"km" , "g" ,"mg", "m","cms" , "cm" , "l" , "s"]      
    
    doc1=nlp(sentence1)
    doc2=nlp(sentence2)
    avg = 0
    
    for token in doc1:
        x=token.lemma_
        y=token.tag_
        if  str(y)!= "_SP" and str(y)!= "":
            z=token.is_stop
            #print(x)
            if z is False and( str(token) in names or str(token) in countries or str(token) in cities or str(token) in numbers):
                if str(token) in names or str(token) in countries or str(token) in cities or str(token) in numbers or str(token) in abbrev:
                    print ("token : "+ str(token) + " is in the special list")
                    avg += 5
                    tuplex = (str(token) , 5)
                    modelans_features.append(tuplex)
                    filtered_sentence1.append((x , y))
                   # modelans_features.append(2)
            elif z is False and (str(y) != "_SP" or str(token) !="-") :
                    avg+=1
                    tuplex = (str(token) , 1)
                    modelans_features.append(tuplex)
                    filtered_sentence1.append((x , y))
                    
    for token in doc2:
        x=token.lemma_
        y=token.tag_
        if  str(y)!= "_SP" and str(y)!= "":
            z=token.is_stop
            if (z is False and (str(token) !="-")) \
            or (str(token) in names or str(token) in countries or str(token) in cities or str(token) in numbers):
                filtered_sentence2.append((x , y))
    ##########################################################################################
    synsets1=[]
    synsets2=[]
    
    for tagged_word1 in filtered_sentence1:
        if tagged_to_synset(*tagged_word1)is not None :
          synsets1.append(tagged_to_synset(*tagged_word1)) 

    for tagged_word2 in filtered_sentence2:
        if tagged_to_synset(*tagged_word2)is  not None:
            synsets2.append(tagged_to_synset(*tagged_word2))
    ##########################################################################################
    
    print(filtered_sentence1)
    print(filtered_sentence2)
    print(synsets1)
    print(synsets2)
    print("----------------------------------------------------------------------------")
    
    #n=0
    #m=0
    sim_list=[]
    #assumtion en el sentence1 hia el model answer we sentence2 hia el student's answer
    #count1=0.0
    max1=[]
    score = 0.0
    for i in range(0 , len(synsets1)):
        for j in range(0 , len(synsets2)):
            # if they are the exact same words
            xx = str(synsets1[i].lemmas()[0].name()).lower()
            yy = str(synsets2[j].lemmas()[0].name()).lower()
            
            syn_list = sy.more_syns()
            lemmas1 = []
            for k in range ( 0 , len(syn_list)):
                if xx in syn_list[k]:
                    for u in syn_list[k]:
                        lemmas1.append(u)
            #print(lemmas1)        
            if xx == yy :
                if (xx in numbers or xx in countries or xx in cities or xx in names ) and  (yy in numbers or yy in countries or yy in cities or yy in names )  :
                    score += 5
                    print("found an exact!:"+ str(synsets1[i].lemmas()[0].name()))
                    tupley = (yy , 5)
                    studentans_features.append(tupley)
                    break
                else:
                    score +=1
                    tupley = (yy , 1)
                    studentans_features.append(tupley)
                    print("found an exact!:"+ str(synsets1[i].lemmas()[0].name()))
                    break
            else:
                #find if they are similar in meaning or not
                #print(xx)
                #print(i)
                lemmas = []
                antonyms = [] 
                # find more similar meaning : 
                if len(lemmas1) != 0:
                    lemmas= lemmas+lemmas1
                    #print(type(lemmas1[0]))
                    print("found more synonyms for the word :" + xx)
                    #print(lemmas1)
                # find the similar meanings here :
                for synset in wn.synsets(str(synsets1[i].lemmas()[0].name())):
                     lemmas.append(str(synset.lemmas()[0].name()))
                     for l in synset.lemmas():
                         if l.name() not in lemmas:
                             lemmas.append(l.name()) 
                             
                #for synset in wn.synsets(str(synsets1[i].lemmas()[0].name())):
                #print(lemmas)
                #if len(lemmas) != 0 :
                if yy in lemmas  and not (xx in numbers or xx in abbrev or xx in countries or xx in cities or xx in names) and len(lemmas) != 0:
                        #count1=count1+1.0
                        score+=1
                        print("found something  alot similar to: " + str(synsets1[i].lemmas()[0].name()))
                        #studentans_features.append(1)
                        tupley = (yy , 1)
                        studentans_features.append(tupley)
                        break
                if yy in lemmas  and  (xx in numbers or xx in abbrev or xx in countries or xx in cities or xx in names) and len(lemmas) != 0:
                        #count1=count1+1.0
                        score+=5
                        print("found something  alot similar to: " + str(synsets1[i].lemmas()[0].name()))
                        #studentans_features.append(1)
                        tupley = (yy , 5)
                        studentans_features.append(tupley)
                        break
                   
                else:
                        #print("heeey")
                        # find if they have the opposite meanings
                        #print(xx)
                            if not (xx in numbers or xx in countries or xx in cities or xx in names or xx in abbrev):
                                    for v in lemmas:
                                        for syn in wn.synsets(v):
                                            for l in syn.lemmas():
                                                if l.antonyms(): 
                                                    if l.antonyms()[0].name() not in antonyms:
                                                        antonyms.append(l.antonyms()[0].name()) 
                            #print(antonyms)
                            if xx in dic_words :
                                index = dic_words.index(xx)
                                antonyms.append(dic_ant[index])
                                #print(index)
                                
                            if xx in dic_ant:
                                index = dic_ant.index(xx)
                                antonyms.append(dic_words[index])
                                #print(index)
                                
                                
                            if synsets2[j].lemmas()[0].name() in antonyms:
                                #count1 = count1-1.0
                                score -= 1.0
                                print("found the complete opposite1 for :" + str(synsets1[i].lemmas()[0].name()))
                                #studentans_features.append(-1)
                                tupley = (yy , -1)
                                studentans_features.append(tupley)
                                break
                            f=[]
                            if not (xx in numbers or xx in countries or xx in cities or xx in names or xx in abbrev):
                                #antonymsx = antonyms[:-3]
                                for k in antonyms:
                                     for synset in wn.synsets(k):
                                         if synset.lemmas()[0].name() not in f:
                                             f.append(synset.lemmas()[0].name())
                                        
                            if xx in dic_words :
                                    index = dic_words.index(xx)
                                    f.append(dic_ant[index])
                                    #print(index)
                            if xx in dic_ant:
                                    index = dic_ant.index(xx)
                                    f.append(dic_words[index])
                                    #print(index)
                            #print(f)    
                            if yy in f:
                                    #count1 = count1-1.0
                                    score -= 1.0
                                    print("found the complete2 opposite for :" + str(synsets1[i].lemmas()[0].name()))
                                    tupley = (yy , -1)
                                    studentans_features.append(tupley)
                                    break
                            #else:
                                #xxx=  str(synsets1[i].lemmas()[0].name())
                            if  xx in names or xx in countries or xx in cities or xx in numbers:
                                    if j == len(synsets2)-1 : 
                                        score -= 10
                                        print("did not find the important word : "+xx )
                                        break
                                #print(xx)
                                
                            if xx in abbrev:
                                    if j == len(synsets2)-1 : 
                                        score -= 15
                                        print("did not find the important measurement : "+xx )
                                        #studentans_features.append(-15)
                                        break 
                            else:
                                    # try to search for some mutual meaning
                                    sim = synsets1[i].path_similarity(synsets2[j])
                    
                                    if sim is not None:
                                        max1.append(sim)
                                        sim_list.append(synsets2[j])
                                        print(synsets2[j])
                                        print(sim)
                                    
                                    if j== len(synsets2)-1 :
                                        c=0
                                        #print(max1)
                                        if max1:
                                            c = max(max1)
                                            c_temp= max1.index(c)
                                            stri = sim_list[c_temp]
                                            ind = synsets2.index(stri)
                                            if c >= 0.8:
                                                score += 0.8
                                                #studentans_features.append(1)
                                                tupley = (synsets2[ind].lemmas()[0].name() , 0.8)
                                                studentans_features.append(tupley)
                                                print("found something similar to:"+ xx)
                                                #print(0.8)
                                                
                                            elif c >= 0.4 and c < 0.6 :
                                                score+= 0.25
                                                tupley = (synsets2[ind].lemmas()[0].name(), 0.25)
                                                studentans_features.append(tupley)
                                                print("found something little similar to:"+ xx)
                                                
                                            max1=[] 
                                            break
     
    print(score) 
    print(avg)       
    return score  , avg   , modelans_features ,   studentans_features  
def remove_abbrev (s1):
    #abbrev = ["km" , "kms" , "g" ,"mg", "m","cms" , "cm" , "l" , "s" , "ft" , "sec" , "fts"]
    nlp = spacy.load('en_core_web_sm')
    doc1=nlp(s1)
    for token in doc1:
        if str(token) == "km":
            s1 = s1.replace("km" , "kilometer")
        elif str(token) == "kms":
            s1 = s1.replace("kms" , "kilometer")
        elif str(token) == "g":
            s1 = s1.replace("g" , "gram")
        elif str(token) == "mg":
            s1 = s1.replace("mg" , "milligram")
        elif str(token) == "m":
            s1 = s1.replace("m" , "meter")
        elif str(token) == "cm":
            s1 = s1.replace("cm" , "centimeter")
        elif str(token) == "cms":
            s1 = s1.replace("cms" , "centimeter")
        elif str(token) == "l":
            s1 = s1.replace("l" , "liter")
            
        elif str(token) == "s":
            s1 = s1.replace("s" , "second")
        elif str(token) == "sec":
            s1 = s1.replace("sec" , "second")
        elif str(token) == "ft":
            s1 = s1.replace("ft" , "feet")
        elif str(token) == "fts":
            s1 = s1.replace("fts" , "feet")
    return s1
     
    
def main_function(sentence1 , sentence2 , numbersx , ranges , modelans_features , studentans_features):
    arabicnames , names , countries , cities , numbers = fun1.important_lists()
    # sentence 1 assumed to be the model answer , and sentence 2 assumed to be the student's answer .
    
    #long_list=["centimeter" , "kilometer" , "meter" , "seconds" , "milligram" , "gram" , "liter"  , "feets"]

    sentence1 = sentence1.lower()
    sentence2 = sentence2.lower()
    nlp = spacy.load('en_core_web_sm')
    sentence1 = remove_abbrev(sentence1)
    sentence2 = remove_abbrev(sentence2)
    doc1=nlp(sentence1)
    doc2=nlp(sentence2)
    score2 = 0.0 
    f = False 
    yes1 = False
    yes2 = False
    modelanswer_num = 0.0
    #print(numbersx)
    if numbersx =="accurate" or numbersx =="ranged":
        sentence1 = nums.get_new_str(sentence1)
        sentence2 = nums.get_new_str(sentence2)
        doc1=nlp(sentence1)
        doc2=nlp(sentence2)
        for token in doc1:
            #print(str(token))
            if str(token).isnumeric():
                yes1 =True
                modelanswer_num =  Decimal(str(token))
                #modelans_features.app
                #print("ghfjwhgfwjgfw" + str(modelanswer_num))
                break
            
    #print(modelanswer_num)  
    if numbersx =="accurate":
        doc2=nlp(sentence2)
        for token in doc2:
            #print(str(token).isnumeric())
            if str(token).isnumeric() and modelanswer_num ==  Decimal(str(token)):
                score2+=5
                tup = (str(modelanswer_num) , 5)
                modelans_features.append(tup)
                studentans_features.append(tup)
                print("found the accurate number")
                f = True
                break
   
    elif numbersx == "ranged":
         for token in doc2:
            #print(str(token).isnumeric())
            if str(token).isnumeric() :
                number = Decimal(str(token))
                if number >= ranges[0] and number <= ranges[1]:
                    score2+=5
                    tup = (str(modelanswer_num) , 5)
                    modelans_features.append(tup)
                    tup2 = (str(number) , 5)
                    studentans_features.append(tup2)
                    f = True
                    print("still in the range")
                    break
                
    if not f and numbersx != "nonumbers":
        score2 -= 10
        tup = (str(modelanswer_num) , 5)
        modelans_features.append(tup)

    for token in doc1:
        if str(token) in arabicnames:
            yes2 = True
            flag = False
            tup = (str(token) , 5)
            modelans_features.append(tup)
            print(modelans_features)
            for token2 in doc2 :
                if str(token) == str(token2):
                    score2+=5
                    studentans_features.append(tup)
                    flag = True
                    sentence1 = sentence1.replace(str(token) , "")
                    sentence2 = sentence2.replace(str(token) , "")
                    break
                
            if not flag:
                score2 -=10
                sentence1 = sentence1.replace(str(token) , "")
                #tup = (str(token) , 5)
                #modelans_features.append(tup)
                
    #print(score2)
    x2 = 0
    if yes1 : 
        x2 +=5
        sentence1 = sentence1.replace(str(modelanswer_num) , " ")
    
    
    if yes2 :
        x2+=5
   
    x1  ,x3  , modelans_features , studentans_features = sentence_similarity(sentence1 , sentence2 , names , countries ,\
                                                         cities , numbers , modelans_features , studentans_features)
    #print(x3)
    x3 += x2
    #print(x3)
    print("score is : " + str (x1 + score2))
    print("total avg : " + str(x3))
    if x3 ==0 :
        return 0, modelans_features , studentans_features , sentence1 , sentence2
    else: 
        return ((x1 + score2 )/ x3)  , modelans_features , studentans_features , sentence1 , sentence2
