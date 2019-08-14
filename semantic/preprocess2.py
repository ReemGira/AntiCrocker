import spacy 


def preprocess2(s1 , s2):
    nlp = spacy.load('en_core_web_sm')
    doc1=nlp(s1)    
    token_list1=[]
    for token in doc1:
        token_list1.append(str(token))
    doc2=nlp(s2)    
    token_list2=[]
    for token in doc2:
        token_list2.append(str(token))
        
    sentence_list1 = []
    sentence_list2= []
    #add the and again
    split_list = ["or" , "also" , "but" , "though" , "therefore" , "although","when" , "despite" , "so" , "for example" , "instead" , "so that" , "however" ]
    string = ""
    #print(token_list)
    for token in token_list1:
        if token in split_list:
            sentence_list1.append(string)
            string = ""
        else:
            string =  string + token + " "
            #print(string)
    if string !="":
        sentence_list1.append(string)
        string=""
        
    for token in token_list2:
        if token in split_list:
            sentence_list2.append(string)
            string = ""
        else:
            string =  string + token + " "
            #print(string)
    if string !="":
        sentence_list2.append(string)
        

    print(sentence_list1)
    print(sentence_list2)
    return sentence_list1 , sentence_list2

#preprocess2 ("he was happy and sad however he didnot know what to do so he helped his friend" \
 #            , "he was glad to see here despite being too lazy , he hugged her the moment he saw her")

