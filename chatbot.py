# Building a Chatbot with Deep NLP
# import lib
import numpy as np
import tensorflow as tf
import re
import time
import os


## Data preprocessing ##
# Import dataset
filePath = 'cornell_movie_dialogs_corpus'
lines = open(os.path.join(filePath,'movie_lines.txt'),encoding='utf-8',errors='ignore').read().split('\n')
conversations = open(os.path.join(filePath,'movie_conversations.txt'),encoding='utf-8',errors='ignore').read().split('\n')

# Build dictionary to connet the output and input.
id2line = {}
for line in lines:
    _line = line.split(' +++$+++ ')
    if len(_line)==5:
        id2line[_line[0]] = _line[4]

# Create a list of conversation
conversations_ids = []
for conversation in conversations[:-1]:
    _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
    conversations_ids.append(_conversation.split(','))

# Getting separately the questions and the answers
questions = []
answers = []

for conversation in conversations_ids:
    for i in range(len(conversation)-1):
        questions.append(id2line[conversation[i]])
        answers.append(id2line[conversation[i+1]])


# Clean function of the texts

def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am",text)
    text = re.sub(r"he's", "he is",text)
    text = re.sub(r"she's", "she is",text)
    text = re.sub(r"she's", "she is",text)
    text = re.sub(r"that's", "that is",text)
    text = re.sub(r"what's", "what is",text)
    text = re.sub(r"where's", "where is",text)
    text = re.sub(r"\'ll", " will",text)
    text = re.sub(r"\'ve", " have",text)
    text = re.sub(r"\'d", " would",text)
    text = re.sub(r"\'re", " are",text)
    text = re.sub(r"won't", "will not",text)
    text = re.sub(r"can't", "cannot",text)
    text = re.sub(r"!", " !",text)
    text = re.sub(r"[\-\(\)\"\#\/\@\;\:\<\>\{\}\+\=\-\|\.\?\,]", "",text)
    return text
# print(clean_text(questions[0]))
# Clean the questions and the answers
cleaned_questions = list(map(clean_text,questions))
cleaned_answers = list(map(clean_text,answers))


# Remove the non-frequent words
word2cnt = {}
for question in cleaned_questions:
    for word in question.split():
        word2cnt[word] = word2cnt.get(word,0)+1
for ans in cleaned_answers:
    for word in ans.split():
        word2cnt[word] = word2cnt.get(word,0)+1

### Make two indepedent dictionaries still because the questions and the answers 
### cannot be of different threshold values.
threshold = 20
questionsword2int = {}
word_num = 0
for word,cnt in word2cnt.items():
    if cnt>=threshold:
        questionsword2int[word] = word_num
        word_num+=1
answersword2int = {}
word_num = 0
for word,cnt in word2cnt.items():
    if cnt>=threshold:
        answersword2int[word] = word_num
        word_num+=1

# Adding the last tokens to these two dictionaries.
tokens = ['<PAD>','<EOS>','<OUT>','<SOS>']  
# Padding, end of sentence, out of vocabulary, start of string
for token in tokens:
    questionsword2int[token] = len(questionsword2int)
    answersword2int[token] = len(answersword2int)

