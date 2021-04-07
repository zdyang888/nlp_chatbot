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
        questions.append(conversation[i])
        answers.append(conversations[i+1])
