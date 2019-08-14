import spacy 
# import modules & set up logging
import logging
from gensim.models import Word2Vec
import time 

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

f = open("semantic/ch1.txt" , "r")
lines1 = f.readlines()
long_str=""
lines=[]

nlp = spacy.load('en_core_web_sm')

token_list=[]
listx=[] 

for i in range (0 , len(lines1)):
    
    doc1 = nlp(lines1[i])
    for token in doc1:
            x= token.lemma_
            z=token.is_stop
            if not z and x != "-PRON-" and x!= ":" and x!= "." and x!= "," and x !="\n" and x!= ";" and x!="‘":
                listx.append(x)
    
    token_list.append(listx)
    listx=[]
    
#model = gensim.models.Word2Vec(token_list, min_count=10)
w2v_model = Word2Vec(min_count=1,window=2,size=300)
t =  time.time()
w2v_model.build_vocab(token_list, progress_per=10000)
print('Time to build vocab: {} mins'.format(round(( time.time() - t) / 60, 2)))    

t =  time.time()
w2v_model.train(token_list, total_examples=w2v_model.corpus_count, epochs=700, report_delay=1)
print('Time to train the model: {} mins'.format(round(( time.time() - t) / 60, 2)))
w2v_model.save('mymodel.model')


#print(w2v_model.init_sims(replace=True))
#print(w2v_model.wv.most_similar(positive=["pound"]))
#print(w2v_model["circumstance"])

