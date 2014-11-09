import nltk
import nltk.data
from nltk.collocations import *
import sys
import os
import re
import pandas
import csv


## only open file once
def build_dict():
  afinnfile = open("AFINN-111.txt")
  scores = {} # initialize an empty dictionary
  #scores_tuples = [line.decode('utf-8').split('\t') for line in afinnline]
  #scores = dict((a,int(b)) for a,b in scores_tuples)
  for line in afinnfile:
    term, score  = line.decode('utf-8').split("\t")  # The file is tab-delimited. "\t" means "tab character"
    scores[term] = int(score)  # Convert the score to an integer.
  return scores

def extract_weight(txt):
    match = re.search(r'BODY WEIGHT:\n[0-9]+\s(lb|kg)',txt)
    if match:
        weight = match.group(0).split('\n')[1]
        if weight.split(' ')[1] == 'lb':
            weight = int(weight.split(' ')[0])*(.4536)
        else:
            weight = int(weight.split(' ')[0])*1.0
        return weight

def extract_dosage(txt):
    match = re.search(r'[0-9]+\.?[0-9]* hit(s)?\n[a-z]*\nLSD',txt)
    if match:
        return match.group(0).split('\n')[0].split(' ')[0]

def extract_age(txt):
    match = re.search(r'Age at time of experience: [0-9]+',txt)
    if match:
        age = match.group(0).split(': ')[1]
        return age

def extract_gender(txt):
    match = re.search(r'Gender: [\w]*\s?[\w]*',txt)
    if match:
        return match.group(0).split(': ')[1]

def det_sent(sentences,sent_dict):
    sents = []
    for sent in sentences:
        count = 0.0
        curr_sent = 0
        tokens = nltk.word_tokenize(sent.strip())
        for token in tokens:
            token = token.lower().strip().replace('.','').replace('?','').replace('!','')
            if token.decode('utf-8') in sent_dict.keys():
                count += 1.0
                curr_sent += sent_dict[token.decode('utf-8')]
        if count != 0.0:
            curr_sent = curr_sent/count
        sents.append(curr_sent)
    return sum(sents)/len(sents)

def get_sentences(txt,det):
    return det.tokenize(txt.strip())

def main():
    drug = sys.argv[1] + '_'
    string = ''
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sent_dict = build_dict()
    with open(drug + 'data.csv','wb') as csvfile:
        with open(drug +'text.txt','wb') as datafile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(["weight","age","dose","gender", "sentiment"])
            for root, subdirs, files in os.walk(drug):
            #    print root,subdirs,files
                for file in files:
                    filepath = os.path.join(root,file)
                    with open(filepath) as f:
                        text = f.read()
                        weight = extract_weight(text)
                        dose = extract_dosage(text)
                        age = extract_age(text)
                        gender = extract_gender(text)
                        sentencess = get_sentences(text,sent_detector)
                        sentiment = det_sent(sentencess,sent_dict)
                        get_sentences(text,sent_detector)
                        writer.writerow([weight,age,dose,gender,sentiment])
                        for sentence in sentencess:
                            datafile.write(sentence + '\n')

main()
