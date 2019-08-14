def more_syns():
    f = open("semantic/synonyms.txt" , "r")
    lines = f.readlines()
    syn_list=[]
    for i in range ( 0 , len(lines)):
        listx =[]
        x= lines[i].split()
        for token in x:
            if token != " ":
                listx.append(token.lower())
        syn_list.append(listx)
    return syn_list


'''
l = more_syns()
s="he use my lapptop"
x=s.split()
for token in x :
    for i in range(0 , len(l)):
        if token in l[i]:
            print(l[i])

'''       
    
    
    
