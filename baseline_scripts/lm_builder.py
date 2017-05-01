from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize
from typing import NamedTuple
from ast import literal_eval


Unigram = str

Bigram = NamedTuple('Bigram', [('prev_word', str), ('word', str)])


def getStats(corpus):
    """ Returns the counts for every word for every genre """
    uni_map = defaultdict(lambda: defaultdict(lambda: 0))
    bi_map = defaultdict(lambda: defaultdict(lambda: 0))
    total_map = defaultdict(lambda: 0)

    text = ''
    genres = []
    corpus = corpus[:-1]
    for document in corpus:
        split_doc = document.split('\t')
        text = split_doc[1]
        genres = literal_eval(split_doc[2])
        sents = sent_tokenize(text)

        temp_uni = defaultdict(lambda: 0)
        temp_big = defaultdict(lambda: 0)
        temp_tot = 0

        for sent in sents:
            words = word_tokenize(sent)
            prev_word = ''
            for word in words:
                if prev_word != '':
                    temp_big[Bigram(prev_word, word)] += 1
                temp_uni[Unigram(word)] += 1
                prev_word = word
                temp_tot += 1
        for genre in genres:
            for word in temp_uni:
                uni_map[genre][word] += temp_uni[word]
            for bigram in temp_big:
                bi_map[genre][bigram] += temp_big[bigram]
            total_map[genre] += temp_tot
    return (uni_map, bi_map, total_map)


if __name__ == '__main__':
    with open('../dataset/train.txt') as f:
        data = f.read().split('\n')
    getStats(data)
    print('complete')
