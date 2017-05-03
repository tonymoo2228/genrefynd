#!/usr/bin/env python3
from sys import argv
from nltk.tokenize import word_tokenize, sent_tokenize


def main(args):
    with open(args[1]) as inf, open(args[2], 'w') as outf:
        for line in inf:
            outstr = ''
            title, text, genres = line.split('\t')
            for sent in (sent_tokenize(text)):
                for word in word_tokenize(sent):
                    outstr += word + ' '
                outstr += '\n'
            # for genre in eval(genres):
            #     outstr += ' __label__' + genre
            outstr.strip()
            outf.write(outstr)


if __name__ == '__main__':
    main(argv)
