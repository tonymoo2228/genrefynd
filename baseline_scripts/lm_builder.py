from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize
from typing import NamedTuple
from ast import literal_eval
from math import log2


Unigram = str

Bigram = NamedTuple('Bigram', [('prev_word', str), ('word', str)])

uniques = set()
uniques_count = 135576


class CountDict(dict):
    def __missing__(self, key):
        return 0


def countWords(corpus_file):
    global uniques
    for doc in corpus_file:
        sents = sent_tokenize(doc.split('\t')[1])
        for sent in sents:
            for word in word_tokenize(sent):
                uniques.add(word)
    print(len(uniques))


def getGenreProbs(corpus_file):
    genre_counts = defaultdict(lambda: 0)
    total_count = 0
    for doc in corpus_file:
        split_doc = doc.split('\t')
        if(len(split_doc) < 3):
            break
        cur_genres = literal_eval(split_doc[2])
        for genre in cur_genres:
            genre_counts[genre] += 1
            total_count += 1
    genre_prob = dict()
    for genre, count in genre_counts.items():
        genre_prob[genre] = log2(count/total_count)
    with open('genresprobs.txt', 'w') as f:
        outstr = ''
        for genre, prob in genre_prob.items():
            outstr += genre + '\t' + str(prob) + '\n'
        f.write(outstr.strip())


def getStats(corpus):
    """ Returns the counts for every word for every genre """
    uni_map = defaultdict(lambda: CountDict())
    bi_map = defaultdict(lambda: CountDict())
    total_map = defaultdict(lambda: 0)
    total_words = 0

    text = ''
    genres = []
    corpus = corpus[:-1]

    timer = 1000
    doc_count = 0
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
            prev_word = '<S>'
            for word in words:
                total_words += 1
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
        doc_count += 1
        timer -= 1
        if(timer == 0):
            print("Document " + str(doc_count) + " completed!")
            timer = 1000
    print('Words = ' + str(total_words))
    return (uni_map, bi_map, total_map)


def probLaplaceUni(prev, word, bi, uni):
    """ Returns the log probability """
    return log2((bi[(prev, word)] + 1)/(uni[word] + len(uni) + 1))


class SmoothedModel(dict):
    def __missing__(self, key):
        return -40000
        # if self.uni[key[1]] != 0:
        #     return log2(1/(self.uni[key[1]] + len(self.uni)))
        # else:
        #     return log2(1/uniques_count)


def getAllProbs(uni, bi):
    models = dict()
    genres = set()
    for genre in uni:
        genres.add(genre)

    for genre in genres:
        big = bi[genre]
        unig = uni[genre]
        model = SmoothedModel()
        model.uni = unig
        models[genre] = model

        for word_pair in big:
            model[word_pair] = probLaplaceUni(word_pair.prev_word,
                                              word_pair.word, big, unig)
    return models


def writeModel(model, name, f):
    outstr = ''
    unistr = ''
    for pair in model:
        outstr += pair[0] + ' ' + pair[1] + ' ' + str(model[pair]) + '\n'
    for word in model.uni:
        unistr += word + ' ' + str(model.uni[word]) + '\n'
    f.write('\n' + name + '\n')
    f.write(outstr)
    f.write(unistr)
#    with open(name + '.unimodel', 'w') as f2:
#        f2.write(unistr)


def main(args):
    print('Beginning training.')
    with open(args[1]) as f:
        data = f.read().split('\n')
    s = getStats(data)
    print('Done counting, now calculating probabilities.')
    models = getAllProbs(s[0], s[1])
    print('Done Calculating probabilities')
    with open('models.mod', 'w') as f:
        for model in models:
            writeModel(models[model], model, f)
    print('Completed training.')
    return models


if __name__ == '__main__':
    main(['name_of_file', '../dataset/train.txt', 'models.pickle'])
