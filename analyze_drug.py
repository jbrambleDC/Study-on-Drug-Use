from __future__ import division
import nltk
from nltk.book import *
import nltk.data
from nltk.collocations import *
import sys
import os
import pandas as pd
import vincent as v


def main():
    drug = sys.argv[1] + '_'
    print drug
    with open(drug + 'text.txt') as f:
        tokens = nltk.word_tokenize(f.read().lower().strip())
        fdist = FreqDist(tokens)
        lexical_diversity = len(set(tokens))/len(tokens)
        trigram_measures = nltk.collocations.TrigramAssocMeasures()
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        finder = TrigramCollocationFinder.from_words(tokens)
        finder2 = BigramCollocationFinder.from_words(tokens)
        finder.apply_freq_filter(4)
        finder2.apply_freq_filter(7)
        for i in finder.nbest(trigram_measures.pmi, 500):
            print i
        bigs = FreqDist(list(bigrams(tokens))).items()[:300]
    df = pd.read_csv(drug+'data.csv')
    mean_age = df['age'].mean()
    mean_sentiment = df['sentiment'].mean()
    print mean_age, mean_sentiment, lexical_diversity
    print tokens.count('pagan'), tokens.count('pyrotenknik'), tokens.count('ritual'), tokens.count('psychedelic'), tokens.count('fractal'), tokens.count('spiral')
    for i in bigs:
        print i
    pos_tokens = nltk.pos_tag(tokens)
    print pos_tokens
    words = ['JJ','JJR']
    noun = ['NNP','NN','NNS']
    descriptions = [word for (word,tag) in pos_tokens if tag in words]
    nouns = [word for (word,tag) in pos_tokens if tag in noun]
    adjdist = FreqDist(descriptions).items()[:250]
    noundist = FreqDist(nouns).items()[:250]
    newdesc = []
    newnouns = []
    for i in descriptions:
        try:
            newdesc.append(i.decode('utf-8'))
        except UnicodeDecodeError:
            pass
    for i in nouns:
        try:
            newnouns.append(i.decode('utf-8'))
        except UnicodeDecodeError:
            pass
    FreqDist(newdesc).plot(50)
    FreqDist(newnouns).plot(50)
    for i in adjdist:
        print i
    for j in noundist:
        print j
    plot_df = df[['weight','sentiment','dose']]
    age_df = df[['age','sentiment']]
    plot_df['value'] = plot_df['dose']/plot_df['weight']
    plot_df = plot_df[['value','sentiment']].dropna()
    line = v.Line(plot_df,iter_idx='value')
    line.axis_titles(x='dose/weight', y='sentiment')
    line.to_json('sentiment_score.json')


main()
