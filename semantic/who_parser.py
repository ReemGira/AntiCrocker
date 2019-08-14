import spacy
nlp = spacy.load('en_core_web_sm')

def get_imp_parts(doc):
	entity_txt = []
	entity_dep = []
	entity_pos = []
	entity_parent = []
	#make the first threee lists at first
	for token in doc:
		entity_txt.append(token.text)
		entity_dep.append(token.dep_)
		entity_pos.append(token.pos_)
		entity_parent.append("None")

	#get the parent of each entity
	for token in doc:
		if token.text == "by" or token.text == "to":
			list_of_children = [child for child in token.children]
			for child in list_of_children:
				my_index = entity_txt.index(str(child))
				entity_parent[my_index] = token.text#str(token.text)

		elif token.pos_ == "ADP" and token.dep_ == "prep":
			list_of_children = [child for child in token.children]
			for child in list_of_children:
				my_index = entity_txt.index(str(child))
				entity_parent[my_index] = "prep"

		elif token.pos_ == "VERB" and (token.dep_ == "xcomp" or token.dep_ == "advcl"):
			list_of_children = [child for child in token.children]
			for child in list_of_children:
				if str(child) == "to":
					my_index = entity_txt.index(token.text)
					entity_parent[my_index] = "to"

		elif token.pos_ == "NOUN" and token.dep_ == "ROOT":
			list_of_children = [child for child in token.children]
			for child in list_of_children:
				if str(child) == "the":
					my_index = entity_txt.index(token.text)
					entity_parent[my_index] = "the"
					
	#make each conjugate know that it has a parent that was before the conjunction 
	#for i in range(len(names))
	for token1 in doc:
		list_of_children = [str(child) for child in token1.children]
		for token2 in doc:
			if token2.dep_ == "conj" and token1.i != token2.i and token2.text in list_of_children:
				entity_parent[token2.i]=token1.text

	return  entity_txt, entity_dep, entity_pos, entity_parent

def get_subj_obj(names,dep,pos,parents):
	subjs = []
	objs = []
	arr_indeces_subjs = []
	arr_indeces_objs = []
	for i in range(len(names)):
		if len(names)==1:
			subjs.append(names[i])
			arr_indeces_subjs.append(i)
		elif len(names) <= 6 and dep[i] == "ROOT" and (pos[i] == "VERB" or pos[i] == "NOUN" or pos[i]=="ADJ")and i == 0:
			subjs.append(names[i])
			arr_indeces_subjs.append(i)
		elif dep[i]=="conj":#I think we should make this condition also for "acomp"
			if parents[i] in subjs:
				subjs.append(names[i])
			elif parents[i] in objs:
				objs.append(names[i])
		elif pos[i] == "PRON" or pos[i] == "NOUN" or pos[i] == "PROPN":
			if dep[i] == "nsubj" or parents[i] == "by" or dep[i] == "acomp" or dep[i] == "attr":# or dep[i]=="conj":
				subjs.append(names[i])
				arr_indeces_subjs.append(i)
			elif dep[i] == "dobj" or dep[i] == "nsubjpass" or parents[i] == "prep":
				objs.append(names[i])
				arr_indeces_objs.append(i)
			elif dep[i]=="dative":
				objs.append(names[i])
				arr_indeces_objs.append(i)
			elif dep[i] == "ROOT" and (i==0 or parents[i]=="the"): #I changed from len(names)<=3 to i==0 in case of a statement like:sarah and the little blonde girl
				subjs.append(names[i])
				arr_indeces_subjs.append(i)
			elif dep[i] == "pobj" and parents[i] == "to":
				objs.append(names[i])
				arr_indeces_objs.append(i)
		elif pos[i] == "VERB" and (dep[i] == "pobj" or dep[i] == "xcomp" or dep[i] == "advcl") and parents[i] == "to": #advcl was added for "ben did this to sarah"
			objs.append(names[i])
			arr_indeces_objs.append(i)
		elif (pos[i] == "VERB" or pos[i] == "ADJ") and dep[i] == "acomp": #(dep[i] == "conj" or dep[i] == "acomp"):
			subjs.append(names[i])
			arr_indeces_subjs.append(i)#to be edited later so we can detect if the element a conj and acomp elements are realy nouns or they were just verbs

	return subjs,objs,arr_indeces_subjs,arr_indeces_objs

def get_similarity_score(model_answer,student_answer,  modelans_features , studentans_features):
  last_score = 0
  the_sum = 0
  
  doc1 = nlp(model_answer) #the first argument here should be the model answer as string
  doc2 = nlp(student_answer)#also the student answer should be string
  
  names1,dep1,pos1,parents1 = get_imp_parts(doc1)
  names2,dep2,pos2,parents2 = get_imp_parts(doc2)
  
  #print(names1)
  #print(names2)
  
  subjs1,objs1,arr_indeces_subjs1,arr_indeces_objs1 = get_subj_obj(names1,dep1,pos1,parents1)
  subjs2,objs2,arr_indeces_subjs2,arr_indeces_objs2 = get_subj_obj(names2,dep2,pos2,parents2)
  
  print(subjs1)
  print(objs1)
  print(subjs2)
  print(objs2)
  the_sum = len(subjs1) + len(objs1)
  
  for s in subjs1:
        #print(s)
        modelans_features.append((s , 2))
        if s in subjs2:
            #print(s)
            last_score += 1
            studentans_features.append((s , 2))
         
             
      
  for b in objs1:
       # print(b)
        modelans_features.append((b , 2))
        if b in objs2:
              #print(b)
              last_score += 1
              studentans_features.append((b , 2))
      
  last_score = last_score/the_sum
  
  
  return last_score

def iterate_list_get_common(list1,list2):
	num_common_elements = 0
	for element in list1:
		for element2 in list2:
			if element == element2:
				num_common_elements += 1
	
	return num_common_elements
	
def get_common_objs_or_subjs(list1,list2):
	num_common_elements = 0
	
	if len(list1) >= len(list2):
		num_common_elements = iterate_list_get_common(list1,list2)
	else:
		num_common_elements = iterate_list_get_common(list2,list1)
	
	
	return num_common_elements

def get_total_distance_subjs_objs(subjs,objs):
	#this function computes the total distance between all subjects and objects of the same statement
	sum_distance = 0
	for s in subjs:
		for b in objs:
			sum_distance += abs(s-b)
	return sum_distance

def get_advs_adjs(names,dep,pos):
	advs = []
	adjs = []
	
	for i in range(len(names)):
		if pos[i] == "ADJ" and dep[i] != "poss":
			adjs.append(names[i])
		elif pos[i] == "ADV":
			advs.append(names[i])
	
	return adjs,advs
	
	
def get_dep_array(model_answer,student_answer):
	doc1 = nlp(model_answer) #the first argument here should be the model answer as string
	doc2 = nlp(student_answer)#also the student answer should be string
	entity_txt1, entity_dep1, entity_pos1, entity_parent1 = get_imp_parts(doc1)
	entity_txt2, entity_dep2, entity_pos2, entity_parent2 = get_imp_parts(doc2)
	
	subjs1,objs1,arr_indeces_subjs1,arr_indeces_objs1 = get_subj_obj(entity_txt1, entity_dep1, entity_pos1, entity_parent1)
	subjs2,objs2,arr_indeces_subjs2,arr_indeces_objs2 = get_subj_obj(entity_txt2, entity_dep2, entity_pos2, entity_parent2)
	
	arr_features1 = [0]*10	#for the model answer
	arr_features2 = [0]*10	#for student's answer
	#feature array structure is:
	#arr_features1[0]= no. of objects in the current statement, arr_features1[1]= no. of subjects in the current statement, arr_features1[2]=no of common objects between the two sentences, arr_features1[3]=no. of common subjects between the two statements, arr_features1[4]=total distance between all the subjects and objects in the current statement, arr_features1[5]=no. of adjectives in the statement, arr_features1[6]= no. of adverbs in the statement, arr_features1[7]=similarity score if student answer has objects and subjects as the model answer, arr_features1[8] = no of common adjs in the two stmts, arr_features1[9] = no of common advs in the two stmts
	
	#no of objects and subjects in the current stmt
	arr_features1[0] = len(objs1)
	arr_features1[1] = len(subjs1)
	arr_features2[0] = len(objs2)
	arr_features2[1] = len(subjs2)
	
	#no of common objects and subjects in the two stmts:
	arr_features1[2] = get_common_objs_or_subjs(objs1,objs2)
	arr_features2[2] = arr_features1[2]
	
	arr_features1[3] = get_common_objs_or_subjs(subjs1,subjs2)
	arr_features2[3] = arr_features1[3]
	
	#sum of distances between all subjects and objects for each stmt:
	arr_features1[4] = get_total_distance_subjs_objs(arr_indeces_subjs1,arr_indeces_objs1)
	arr_features2[4] = get_total_distance_subjs_objs(arr_indeces_subjs2,arr_indeces_objs2)
	
	
	#get number of adjectives and adverbs in each statement:
	adjs1,advs1 = get_advs_adjs(entity_txt1, entity_dep1, entity_pos1)
	adjs2,advs2 = get_advs_adjs(entity_txt2, entity_dep2, entity_pos2)
	arr_features1[5] = len(adjs1)
	arr_features1[6] = len(advs1)
	arr_features2[5] = len(adjs2)
	arr_features2[6] = len(advs2)
	
	#get the similarity score between the two statements considering the if both student answer has the same subjs and objs as the model answer
	modelans_features = []
	studentans_features = []
	arr_features1[7] = get_similarity_score(model_answer,student_answer,  modelans_features , studentans_features)
	arr_features2[7] = arr_features1[7]
	
	#get the number of common adjs and advs in the two sentences
	arr_features1[8] = get_common_objs_or_subjs(adjs1,adjs2)
	arr_features1[9] = get_common_objs_or_subjs(advs1,advs2)
	arr_features2[8] = arr_features1[8]
	arr_features2[9] = arr_features1[9]
	
	return arr_features1,arr_features2
  
'''
stmt ="cliniton defeated dole"

s1= "dole was defeated by cliniton"
s2= "dole defeated cliniton"
s3= "cliniton won over dole"

print(get_similarity_score(stmt , s1 , [] , []))

print(get_similarity_score(stmt , s2, [] , []))

print(get_similarity_score(stmt , s3, [] , []))
'''
