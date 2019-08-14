import spacy

objects_subjects = ["nsubj","pobj","dobj","nsubjpass"]
subjects =["nsubj","pobj"] 
objects = ["dobj","nsubjpass"]

def check_entities(sentence1,objs1,sentence2,objs2):
  #sentence1 is the model answer and sentence2 is the student answer
  score = 0
  for elem in sentence1:
      if elem in sentence2:
        index1 = sentence1.index(elem)
        index2 = sentence2.index(elem)
        type_elem1 = objs1[index1]
        type_elem2 = objs2[index2]
        if ((type_elem1 in subjects) and (type_elem2 in subjects)) or ((type_elem1 in objects) and (type_elem2 in objects)):
          score += 0.5
  return score
  
nlp = spacy.load('en_core_web_sm')
#doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')
doc1 = nlp(u'sara said that ben is beautiful')
doc2 = nlp(u'ben did this to maya')

my_sentence = []
original_sentence = []
for token in doc1:
    print(token.text, token.pos_, token.dep_)
    if (token.dep_ == "ROOT" and token.pos_ == "NOUN"):
         # print("shjdh")
          my_sentence.append("nsubj")
          original_sentence.append(token.text)
         
      
    if token.dep_ in objects_subjects:
          #print("asjhasjd")
          my_sentence.append(token.dep_)
          original_sentence.append(token.text)

print("-----------------------------------------")    
my_sentence2 = []
original_sentence2 = []    
for token in doc2:
     print(token.text, token.pos_, token.dep_)
     if (token.dep_ == "ROOT" and token.pos_ == "NOUN"):
          my_sentence2.append("nsubj")
          original_sentence2.append(token.text)
     elif token.dep_ in objects_subjects:
          my_sentence2.append(token.dep_)
          original_sentence2.append(token.text)
	  
final_score = check_entities(original_sentence,my_sentence,original_sentence2,my_sentence2)
print(final_score)
