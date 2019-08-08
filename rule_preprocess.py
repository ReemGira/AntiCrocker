def important_lists():
    f = open("semantic/names.txt" ,  "r")
    names = f.readlines()
    
    for i in range (0 , len(names)):
        names[i] = names[i].replace('\n' , '')
        names[i] = names[i].lower()
        
    #print(names)
    
    f= open ("semantic/countries.txt" , "r")
    countries = f.readlines()
    ##############################################################################################
    for i in range (0 , len(countries)):
        countries[i] = countries[i].replace('\n' , '')
        countries[i] = countries[i].lower()
        
    #print(len(countries))
    #############################################################################################
    
    f= open ("semantic/cities.txt" , "r")
    city = f.readlines()
    cc = []
    ##############################################################################################
    for i in range (0 , len(city)):
        if city[i] != "": 
            city[i] = city[i].replace('\n' , '')
            city[i] = city[i].lower()
            cc.append(city[i])
    #############################################################################################
    #numbers = ["one" , "two"  , "three" , "four" , "five" , "six" , "seven" , "eight" , "nine" , "ten" , "zero" , "true" , "false"]
    numbers = ["true" , "false"]
    f = open("semantic/arabicnames.txt" ,  "r")
    anames = f.readlines()
    
    for i in range (0 , len(anames)):
        anames[i] = anames[i].replace('\n' , '')
        anames[i] = anames[i].lower()
        
    #print(names)
    return anames, names , countries ,cc  , numbers

