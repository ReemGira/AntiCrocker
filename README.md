# AntiCrocker
Essay Grading project, that gives a grade to the student answer based on how it is related semantically to corresponding model answer

# Semantic analysis code
We are using both machine learning and rule based modules to give a rate on how two sentences are similar to each other semantically.

For the rule-based module, the accuracy first was 71% when using NLTK and WordNet only, but after manually collecting some other dictionary semantically related words, the accuracy reached 75%. Then, and as we are grading English language high school exams, we concentrated also on English people names, Country names, Continent names and hence our accuracy reached 76%.
It is known that in some questions numbers are as important as people names to detect if the answer is correct or not, so we transformed all the numbers in their word-written forms insyead of digits form so it is easy to compare the numbers in the student's answer with the numbers in the model answer to detect if the numbers in the student's answer are within the accepted range in the model answer or not. Also the numbers have high weight as names. And for describing a scene, it is completely different to say "Brown wall and white floor" and "White wall and brown floor", so it was necassary to  detect the objects and their related adjectives, also using Spacy library. We also added another feature that is detecting the real subjects and objects of a statement to detect if the student's answer contains the same subjects and objects as the model answer or not, as the student can write the same subject and object but in an order that gives different meaning than that intended in the model answer, as example: "the man bites the dog" and "the dog bites the man", the two statements contain the same words but the meaning differs. So using Spacy library we could detect the real subjects and objects for simple statements. After adding all these features, our accuracy reached 80%.

For the machine module:
There were many attempts to use a NN to get the semantic similarity score between two given statements, and because we needed also to concentrate that the student answer should be compared to the model answer, we tried to use the well-known siamese NN, with google-news pre-trained embeddings, but it gave very poor accuracy for our task. So other approaches were made. First we applied the machine learning module on the story questions to use the story pdf/text to be used as the vocabulary for the embeddings of our semantic NN, as this was our problem with google-news embeddings, as it doesn't contain all the vocabulary needed for grading an English Essay Exam. "Gulliver's Travels" was used to be the vocabulary. First attempt was by combining glove vocabulary with the vocabulary of the story we have, and with the help of the features extraceted from the rule-based module, accuracy was 50%. When using only the vocabulary of the story, with the help of features extracted from the rule-based module, accuracy reached 79%. These previous two approaches were made using gensim library. 
Another approach was by just using the features extracted from the rule-based module, but need more time and dataset to be trained.

# Datasets used:
 Stanford dataset for training: https://nlp.stanford.edu/projects/snli/
 google-news Word2vec embeddings: https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
 GloVe: https://nlp.stanford.edu/projects/glove/
 and finally the text of "Gulliver's Travels"
