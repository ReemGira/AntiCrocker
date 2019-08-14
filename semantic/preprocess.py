import spacy 
import semantic.neg_functions as fn

def negation_elimination (sentence1):
    #sentence1 ="he didn't seem glad about it "
    neg_count = 0
    sentence1 = sentence1.lower()
    index = sentence1.find("won't")
    while index > -1:
        sentence1 = sentence1.replace("won't" , "will not")
        index = sentence1.find("won't")
        
    nlp = spacy.load('en_core_web_sm')
    doc1=nlp(sentence1)    
    token_list=[]
    for token in doc1:
            x=token.lemma_
            #print(x)
            #print(token.text, token.dep_, token.head.text, token.head.pos_, [child for child in token.children])
            if str(token) == "n't":
                token_list.append("not")
            else:
                token_list.append(str(token))
            if str(x) == "not" or str(x) == "none" or str(x) == "neither":
                neg_count+=1
                
    #print(neg_count)
    if neg_count <= 0:
        print("this sentence has no negation ")
        return (sentence1)
    
    else:
        #there are more than one negation , split the sentence into smaller sentences 
        # split 3ala el and / or / also / but / though / although
        sentence_list = []
        split_list = ["or" , "and" , "also" , "but" , "though" , "therefore" ,"although" , "despite" , "so" , "that" , "because" , "for example" , "instead" , "so that" , "however" , "," , "." ]
        string = ""
        #print(token_list)
        for token in token_list:
            if token in split_list:
                # split the sentence 
                #sentence_list.append(string)
                sent = fn.main_function(string)
                string=""
                sentence_list.append(sent+token+" ")
            else:
                string =  string + token + " "
                #print(string)
        if string !="":
            sent = fn.main_function(string)
            sentence_list.append(sent)
            
                            
        #print(sentence_list)
        
    original_sentence = ""
    for sen in sentence_list:
           original_sentence +=sen
    
    #return(original_sentence) 
    # adjust el spaces fe el a5er 5ales
    '''
    doc1=nlp(original_sentence)    
    token_list=[]
    for token in doc1:
          #print(token)
          if  str(token) == "  ":
              original_sentence = original_sentence.replace(str(token) , ' ')
    '''
    return(original_sentence)
          
        
        
