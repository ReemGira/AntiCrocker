import semantic.rule_mod as rule
import semantic.preprocess2 as p2
import semantic.preprocess as p1
import pandas as pd
#from collections import Counter
import semantic.ss 
import semantic.who_parser as qparse
import spacy

def grading_module1():
	
    #train_df = pd.read_csv("H:\\flask2" ,  encoding='latin-1')
    train_df = pd.read_csv("C:\\Users\\Reem Salma Amr\\Desktop\\GP all\\website\\flask\\answers.csv" ,  encoding='latin-1')
    train_df = train_df.iloc[0:]
    sen1 = list(train_df['answer1'])
    sen2 = list(train_df ['answer2'])
    sen3 = list(train_df['question'])
    sen4 = list(train_df['numbers'])
    sen5 = list(train_df['ranges'])
    sen6 = list(train_df['type'])
    #new_score=[]
    #features1= []
    #features2= []
    
    #modelans_features1 =[] 
    #studentans_features1=[]      
    #print(Counter(sen3))
    #ans1 = []
    #ans2 = []
    scoores=[]
    #binary=[]
    f = open("semantic/output.txt" , "w")
    #f2 = open ("rule_output.txt" , "w")
    for i in range( 0 , len(sen1)):
    ##############################################################################################################
        #print(i)
        #print(sen6[i])
        s1 = sen1[i]
        s2 = sen2[i]
        #scoores=[]
        if s1 != "":
            s1 = p1.negation_elimination(s1)
        if s2 != "":
            s2 = p1.negation_elimination(s2)
        
        s1_list , s2_list = p2.preprocess2(s1 , s2)
        score_list=[]
        cc = 0
        modelans_features =[]
        studentans_features=[]
        numbers = sen4[i]
        ranges = sen5[i]
        ranges_list=[]
        if numbers == "ranged":
            r = ranges.split(":")
            ranges_list.append(int(r[0]))
            ranges_list.append(int(r[1]))
            
        q = sen3[i].lower()
    ###############################################################################################################    
        if q.startswith("who" , 0 , 3):
            cc=qparse.get_similarity_score(s1_list[0] , s2_list[0] , modelans_features , studentans_features)
            print("the final score1 :" + str(cc))
            if cc < 0 :
                cc = 0
            elif cc >= 0  and cc <= 0.39:
                cc= 0
            elif cc >= 0.4 and cc <= 0.55:
                cc = 0.5
            else:
                cc = 1
            
            scoores.append(cc)
            if sen6[i].lower()=="story":
                f.write(str(cc)+"\n")
                for ii in range (0 , len(modelans_features)):
                            f.write(str(modelans_features[ii]) + ",,")
                f.write("\n")
                for iii in range (0 , len(studentans_features)):
                         f.write(str(studentans_features[iii]) + ",,")
                f.write("\n")
                
    #####################################################################################################################        
        elif q.startswith("describe" , 0 ,8):
            cc = ss.get_score(s1_list[0] , s2_list[0]  , modelans_features , studentans_features)
            print("the final score1 :" + str(cc))
            if cc < 0 :
                cc = 0
            elif cc >= 0  and cc <= 0.39:
                cc= 0.3
            elif cc >= 0.4 and cc <= 0.55:
                cc = 0.5
            elif cc == 0.6666:
                c=0.66
            else:
                cc = 1
           
            scoores.append(cc)
            if sen6[i].lower()=="story":
                f.write(str(cc)+"\n")
                for ii in range (0 , len(modelans_features)):
                            f.write(str(modelans_features[ii]) + ",,")
                f.write("\n")
                for iii in range (0 , len(studentans_features)):
                         f.write(str(studentans_features[iii]) + ",,")
                f.write("\n")
    ###################################################################################################################        
        else:
            for ri in range ( 0 , len(s1_list)):
                for j in range ( 0 , len(s2_list)):
                    if s2_list[j] != "" and s1_list[ri] != "":
                        score , modelans_features , studentans_features, sentence1 , sentence2 = rule.main_function(s1_list[ri] , s2_list[j]\
                                                                                             , numbers , ranges_list ,\
                                                                             modelans_features , studentans_features)
                        
                        if score >= 0.33 and score <= 0.4 :
                            nlp = spacy.load('en_core_web_sm')
                            doc1=nlp(s1_list[ri])    
                            token_list1=[]
                            for token in doc1:
                                if not (token.is_stop):
                                    token_list1.append(str(token))
                            if len(token_list1) >= 8:
                                score = 0.5
                        score_list.append(score)
                        score_list.append(score)
                        print(score)
                        
                if  score_list:
                    #print(score)
                    c= max(score_list)
                    cc+=c
                    
            modelans_features = list(set(modelans_features))
            studentans_features = list(set(studentans_features))
            length = len(s1_list)
            if "" in s1_list:
                length -=1
                
            m = (cc / length)
            if m >= 0.33 and m <= 0.4 and len(s1_list) >= 8:
                m=0.5
            print("the final score1 :" + str(m)) 
            if m < 0 :
                m = 0
            elif m >= 0  and m <= 0.39:
                 m = 0
            elif m >= 0.4 and m <= 0.55:
                m = 0.5
            else:
                m = 1
            scoores.append(m)
            
            if sen6[i].lower() == "story":
                f.write(str(m) + "\n")
                print("da5al fe el i "+str(i))
                for ii in range (0 , len(modelans_features)):
                            f.write(str(modelans_features[ii]) + ",,")
                f.write("\n")
                for iii in range (0 , len(studentans_features)):
                         f.write(str(studentans_features[iii]) + ",,")
                f.write("\n")
            

###############################################################################################################
    reading_scores =[]     
    for i in range ( 0 , len(scoores)):
        if sen6[i] == "reading":
            reading_scores.append(scoores[i])
    
    f.close()
    return reading_scores
    #f2.close()
