#!/usr/bin/env python3

from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize
from lm_builder import SmoothedModel
from math import log2, inf


def readModels(f, prob_f):
    current_name = ''
    models = dict()
    for line in f:
        splt_l = line.split()
        length = len(splt_l)
        if length == 0:
            cls = next(f).strip()
            current_name = cls
            model = SmoothedModel()
            model.uni = defaultdict(lambda: 0)
            models[current_name] = model
        if length == 2:
            models[current_name].uni[splt_l[0]] = int(splt_l[1])
        if length == 3:
            models[current_name][(splt_l[0], splt_l[1])] = float(splt_l[2])
    for line in prob_f:
        genre, prob = line.split('\t')
        models[genre].prob = float(prob)
    return models


def classify(class_models, document):
    all_class = dict()
    current_class = ''
    cur_max = -inf
    words = [word_tokenize(sent) for sent in sent_tokenize(document)]
    word_count = 0
    for sent in words:
        word_count += len(sent)
    for cls, model in class_models.items():
        cur_val = 0
        for sent in words:
            prev_word = '<S>'
            for word in sent:
                cur_val += model[(prev_word, word)]
                prev_word = word
        cur_val = cur_val + word_count - model.prob
        if(cur_max < cur_val):
            cur_max = cur_val
            current_class = cls
        all_class[cls] = cur_val
    print(current_class)
    for cls, val in sorted(all_class.items(), key=lambda x: x[1]):
        print(cls, val)


main_args = ['name', 'models.mod', 'genresprobs.txt']


def main(args):
    with open(args[1]) as f, open(args[2]) as f2:
        models = readModels(f, f2)
    return models
    print('done')


def _getData():
    data = []
    with open('../dataset/test.txt') as f:
        for line in f:
            title, text, genres = line.split('\t')
            data.append(text)
    return data


if __name__ == '__main__':
    main(['name', 'models.mod'])
