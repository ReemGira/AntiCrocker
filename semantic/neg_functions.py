import spacy 
#from nltk.corpus import wordnet as wn 
#import string
nlp = spacy.load('en_core_web_sm')
import semantic.functions as fun

def check_negation(sentence):
    doc = nlp(sentence)
    for token in doc:
        #print(token.text, token.dep_, token.head.text, token.head.pos_, [child for child in token.children])
        
        if token.dep_ == "neg":
            #print("\n")
            return "not"
        else:
            if token.text == "none" or token.text=="neither":
                return token.text
            else:    
                continue
        
    #print("\n")
    return None  
######################################################################################################################
#def negation_list(sentence):
 #   neg = ["not" , "never" , "nowhere" ,"no" , "none" , "nobody" , "nothing" , "neither" ]
 
def get_negated_word(sentence):
     list1=[]
     x=None
     #Flag=False
     ll = ["is" , "am" , "are" , "has" , "have" , "had" , "did" , "was" , "were"  , "will" , "seem" , "'s" ]
     doc = nlp(sentence)
     for token in doc:
         for child in token.children:
             list1.append(child)
             #print(child)
         #print(len(list1))
          #print(token.text, token.dep_, token.head.text, token.head.pos_, [child for child in token.children])
         if token.dep_ == "neg":
             if str(token.head.text) not in ll:
                 #print("yes")
                 return str(token.head.text)
             
         if len(list1) != 0:
             for i in range(0 , len(list1)):
                 if (str(list1[i]) =="not" or str(list1[i]) =="n't" or str(list1[i]) =="none" or str(list1[i]) =="neither" ) and i != (len(list1)-1) and (token.head.text) in ll:     
                     return(list1[i+1])
                 else:
                     x= str(token.head.text)
     return x
#####################################################################################################################          
#####################################################################################################################  
   
#####################################################################################################################
def main_function(M):
#M =  "is not mean about it"
    new_sentence=M
    #substring1=""
    ## convert to lower case ###
    new_sentence = new_sentence.lower()
    #print(new_sentence)
    flag = check_negation(new_sentence)
    #print(flag)
    #print("\n")
    #substring=""
    #index = -1
    
    if flag != None :
        x = get_negated_word(new_sentence)
        print("The Negated word: ")
        print(x)
        y = fun.get_antoynm(x)
        print ("the antonym is:")
        print(y)
        if y != None:
            if flag == "not":
                #substring = "not "+ str(x)
                #index = new_sentence.find(substring)
                new_sentence = new_sentence.replace("not","")
                new_sentence = new_sentence.replace(str(x),str(y))
                print(new_sentence)
                return new_sentence
           
            else:  # no not so there is none or neither 
                new_sentence = new_sentence.replace(flag ,"all")
                new_sentence = new_sentence.replace(str(x) ,str(y))
                print(new_sentence)
                return new_sentence
        else:
             print("the word : " + str(x) + " has no antonym in the wordnet.")
             return new_sentence
    else:
        return new_sentence
####################################################################################################################
