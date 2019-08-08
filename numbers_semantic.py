num_str = ["zero","one","two","three","four","five","six","seven","eight","nine",
"ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen",
"twenty","thirty","fourty","fifty","sixty","seventy","eighty","ninety",
"hundred","thousand"]

num_int = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,30,40,50,60,70,80,90,100,1000]

def num_or_not(current_element):
	#true means that the current element is a number and false means that the current element is not a number
	return current_element in num_str

def may_be_more_digit(str1):
	
	return (num_or_not(str1) or (str1 == "and"))

def find_num_str(current_element):
	if num_or_not(current_element):
		
		i = num_str.index(current_element)
		ret_index = num_int[i]
		
		return ret_index
	
	else:
		return -1

def concat_str(current_str,flag):
	concatenated_str=""
	if flag:
		flag = False
		concatenated_str = current_str
	else:
		concatenated_str = " "+current_str
	
	return concatenated_str,flag

def get_new_str(original_str):
	sum = 0
	flag_first_added = True	#this flag is used to know which is the first element to be added to the new string/last string, so if it was not the first element it will add a space caharcter before adding itself to the last string
	current_list_of_str = original_str.split(" ")
	last_str = ""
	
	if current_list_of_str[len(current_list_of_str)-1] == "and":
		del current_list_of_str[-1]
		
	for i in range(len(current_list_of_str)):
		current_element = current_list_of_str[i]
		if num_or_not(current_element):	#case1 means we got a number
			new_int=find_num_str(current_element)
			#check if the words before the current contained 1000, so the sum now is a multiple of 1000, to avoid what happens in str3
			if sum >=1000 and i < len(current_list_of_str)-1 and current_list_of_str[i+1] == "hundred":
				sum = sum//100
				sum += new_int
			else:
				if ((sum > 0) and (new_int >=100)): #new_int >= 100 meaning that the number stored in new_int is either 100 or 1000
					#if (i>0 and (num_or_not(current_list_of_str[i-1]))):
					#	sum += find_num_str(current_list_of_str[i-1]) * new_int
					sum = sum * new_int
				elif (i>0 and find_num_str(current_list_of_str[i-1])>10 and find_num_str(current_list_of_str[i-1])<20):
					#this is the case of str15 = in nineteen thirty three
					old_sum = sum * 100
					sum = new_int
					sum += old_sum
				else:
					sum += new_int
			#print("current sum = "+str(sum))
			#check if this was the last digit of the current number or not
			#i == len(current_list_of_str) #meaning that this was the last element in the statement so we add the sum to last_str
			if (i == len(current_list_of_str)-1) or ((i < len(current_list_of_str))and(not may_be_more_digit(current_list_of_str[i+1]))):
				#update the string
				
				concatenated_str,flag_first_added=concat_str(str(sum),flag_first_added)
				'''
				if flag_first_added:
					flag_first_added = False
					concatenated_str = str(sum)
				else:
					concatenated_str = " "+str(sum)
				'''
				sum = 0 #we should reset the sum when adding the current sum
				last_str += concatenated_str
			
		else: #case2, this is not a number
			if current_element == "and" and i < len(current_list_of_str)-1:
				#here we have also three cases, one that this "and" is part of a number, or not
				#case 1: ... num "and" num ...
				if ((i < len(current_list_of_str))and(num_or_not(current_list_of_str[i+1]))) and (i>0 and (num_or_not(current_list_of_str[i-1]))):
					#in this case we will not update last_str or sum
					#print("nooooo "+current_list_of_str[i+1] + str(i))
					#continue #I think or it may be other thing
					#continue
					last_str +=""
				
				#case 2: ... num "and" not_num ...
				elif ((i < len(current_list_of_str))and(not num_or_not(current_list_of_str[i+1]))) and (i>0 and (num_or_not(current_list_of_str[i-1]))):
					#update last_str with sum , reset sum, and add "and" to last_str
					#print("I am hereeeee")
					concatenated_str,flag_first_added=concat_str(str(sum) + " and",flag_first_added)
					'''
					concatenated_str=""
					if flag_first_added:
						flag_first_added = False
						concatenated_str = str(sum)+ " and"
					else:
						concatenated_str = " "+str(sum) + " and"
					'''
					sum = 0 #we should reset the sum when adding the current sum
					last_str += concatenated_str
				
				#case 3: ... not_num "and" not_num ..., or anything rather than the two above cases
				#in this case, "and" is as any other word in the given string, so we should remove this part from here and put it with the above else of case2 of not number but let it for now be as it is
				else:
					concatenated_str,flag_first_added=concat_str("and",flag_first_added)
					last_str += concatenated_str
			
			else: #if the current element was not number and not "and"
				concatenated_str,flag_first_added=concat_str(current_element,flag_first_added)
				last_str += concatenated_str
				
	return last_str			

'''
#testing the code:
str1 = "two men are there"
str2 = "there are one hundred and seventy dogs and"
str3 = "here are three thousand and four hundred cells" #drbat mny 34an lma kont b3ml drb f thousand w b3den drb f hundred, el rqm tl3 8lt, tl3: 300400 , wel mfrod 2nna bs n3ml multiply ll rqm elly 2bl el hundred 2w thousand
str4 = "there are four apples on the table and three bananas"
str5 = "one dog is chasing two cats and there are twenty people watching"
str6 = "one hundred and seventy cats"
str7 = "one hundred and seventy two"
str8 = "one hundred and seventy two and there are seventy one again"
str9 = "there are two hundred and seventy cats in the room"
str10 = "there are two hundred and seventy two cats in the room"
str11 = "there are many cats and a dog"
str12 = "one hundred and seventy two and" #de btdrab lma bn7ot and fe 2a5er el gomla, elmfrod tt4al 2slun l2nha fe 2a5er el gomla w mlha4 lazma hna--->solved by the if statement before the for loop of making the last_str
str13 = "we have hundred students"
str14 = "we have eleven courses"
str15 = "in nineteen thirty three" #not handeled (if new_int of previous current element was between 11 and 19 and the current element is a number, then we will split the number into two parts, the first part which will be multiplied by 100 and the second part will be added as it is
str16 = "there are 7 of them"
print(get_new_str(str16))
'''