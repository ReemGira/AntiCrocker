
def extract_more_antonyms ():
    f= open("semantic/antonyms.txt" , "r")
    lines = f.readlines()
    words=[]
    antonyms = []
    
    
    for i in range ( 0 , len(lines)-1):
        lines[i] = lines[i].replace("\n" , "")
        lines[i] = lines[i].lower()
        
    for i in range ( 0 , len(lines)-1 , 2):
        #print(i)
        words.append(lines[i])
        antonyms.append(lines[i+1])
    #words= words.lower()
    #antonyms = antonyms.lower()
    return words , antonyms
      
    
    
    
