import gensim
from scipy import spatial
import spacy
import numpy
import time

def semantic_module2():
    start = time.time()
    # Load pre-trained Word2Vec model.
    model = gensim.models.Word2Vec.load("semantic/mymodel.model")
    
    print("time to finish" + str((time.time() - start) / 60))
    f2 = open("semantic/macine.txt" , "w")
    #print(model["gulliver"])
    v = model["pound"]
    v2= model["thirty"]
    scores=[]
    f = open("semantic/output.txt" , "r")
    lines = f.readlines()
    ans1=[]
    ans2=[]
    sc = []
    for i in range (0 , len(lines) , 3):
        lines[i] = lines[i].replace("\n" , "")
        sc.append(str(lines[i]))
        ans1.append(lines[i+1])
        ans2.append(lines[i+2])
        
    nlp = spacy.load('en_core_web_sm')
    #print("\n\n")
    a=[]
    b=[]
    a1=[]
    b1=[]
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    #a[0]=0
    for i in range ( 0 , len(ans1)):
        ans1[i] = ans1[i].replace("\n" , "")
        ans2[i] = ans2[i].replace("\n" , "")
        avg=0
        avg2=0
        a = ans1[i].split(",,")
        for x in a :
            if x:
                a1.append(x)
        b = ans2[i].split(",,")
        for x in b :
            if x:
                b1.append(x)
        #print(a1)
        for tuplea in a1:
            strx = tuplea.split(",")
            strx[0]= strx[0].replace('(' , "")
            strx[0] = strx[0].replace("'" , "")
            
            strx[1] = strx[1].replace(")" , "")
            strx[1] = strx[1].replace(" " , "")
            #print(strx)
            list1.append(strx[0])
            list2.append(strx[1])
            avg +=float(strx[1])
            
        print(avg)
        print(list1)
        print(list2)
        
        for tuplea in b1:
            strx = tuplea.split(",")
            strx[0]= strx[0].replace('(' , "")
            strx[0] = strx[0].replace("'" , "")
            
            strx[1] = strx[1].replace(")" , "")
            strx[1] = strx[1].replace(" " , "")
            #print(strx)
            list3.append(strx[0])
            list4.append(strx[1])
            avg2 +=float(strx[1])
            
        print(list3)
        print(list4)
        print(avg2)
        ####################################################################33
        for k in range( 0 , len( list1)):
            doc1 = nlp(list1[k])
            lem = doc1[0].lemma_
            try:
                xx = str(lem)
                if k==0:
                    v.setflags(write=1)
                    v = model[xx] * float(list2[k])
                    #print(v.shape)
                else:
                    v.setflags(write=1)
                    v += (model[xx] * float(list2[k]))
            except:
                print("didn't find the lemma:" + xx)
                if k==0:
                    v.setflags(write=1)
                    v = numpy.ones((300,)) * float(list2[k])
                    #print(v.shape)
                else:
                    v.setflags(write=1)
                    v += (numpy.ones((300,)) * float(list2[k]))
                    #v *= float(list2[k])
            
            
            #v.setflags(write=1)
            #v *= avg
        #print(v)
           ########################################################################
        for j in range( 0 , len( list3)):
                doc2 = nlp(list3[j])
                lemy = doc2[0].lemma_
                try:
                    yy = str(lemy)
                    if j==0:
                        v2.setflags(write=1)
                        v2 = (model[yy] * float(list4[j]))
                        #print(v)
                    else:
                        v2.setflags(write=1)
                        v2 += (model[yy]  * float(list4[j]))
                except:
                    print("didn't find the lemma:" + yy)
                    if j==0:
                        v2.setflags(write=1)
                        v2 = (numpy.ones((300,)) * float(list4[j]))
                        #print(v)
                    else:
                        v2.setflags(write=1)
                        v2 += (numpy.ones((300,)) * float(list4[j]))
                
                
                #v2.setflags(write=1)
                #v2 *= avg2
        #print(v2)
                
        eudistance = spatial.distance.euclidean(v, v2)
        print("similarity score is : ", 1 / (1.1 ** eudistance))
        f2.write(str(1 / (1.1 ** eudistance)) + "\n")
        scores.append( 1 / (1.1 ** eudistance))
        a1=[]
        b1=[]
        list1=[]
        list2=[]
        list3=[]
        list4=[]
        #break
    machine_scores=[]    
    for i in range( 0 , len(scores)):
        if float(sc[i]) >= 0.6 and scores[i] <= 0.2:
            s=1
        elif float(sc[i]) >= 0.5 and scores[i] <= 0.2:
            s=0.55
        elif float(sc[i]) <= 0.1:
            s=0
        else:
            s = (scores[i]+ float(sc[i])) / 2.0
            if s <= 0 or s <= 0.34:
                s=0
            elif s>= 0.35 and s <= 0.62:
                s=0.55
            else:
                s=1
        #print(s)
        machine_scores.append(s)
    f2.close()
    return machine_scores