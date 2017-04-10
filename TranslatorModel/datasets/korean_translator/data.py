EN_WHITELIST = '0123456789abcdefghijklmnopqrstuvwxyz '  # space is included in whitelist
BLACKLIST = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\''

FILENAME = 'formal_informal_paired_data.txt'

limit = {
    'maxq': 25,
    'minq': 0,
    'maxa': 25,
    'mina': 0
}

UNK = 'unk'
VOCAB_SIZE = 8000

import nltk
import itertools

import numpy as np

import pickle


def ddefault():
    return 1


'''
 read lines from file
     return [list of lines]
'''

def read_lines(filename):
   with open(filename, encoding='utf-8') as f:
      res = f.read().split('\n')[:-1]
   return res

'''
 split sentences in one line
  into multiple lines
    return [list of lines]
'''


def split_line(line):
    return line.split(':')


'''
 remove anything that isn't in the vocabulary
    return str(pure ta/en)
'''


def filter_line(line, whitelist):
    return ''.join([ch for ch in line if ch in whitelist])


'''
 read list of words, create index to word,
  word to index dictionaries
    return tuple( vocab->(word, count), idx2w, w2idx )
'''


def index_(tokenized_sentences, vocab_size):
    # get frequency distribution
    freq_dist = nltk.FreqDist(itertools.chain(*tokenized_sentences))
    # get vocabulary of 'vocab_size' most used words
    vocab = freq_dist.most_common(vocab_size)
    # index2word
    index2word = ['_'] + [UNK] + [x[0] for x in vocab]
    # word2index
    word2index = dict([(w, i) for i, w in enumerate(index2word)])
    return index2word, word2index, freq_dist



def zero_pad(qtokenized, atokenized, w2idx):
    # num of rows
    data_len = len(qtokenized)

    # numpy arrays to store indices
    idx_q = np.zeros([data_len, limit['maxq']], dtype=np.int32)
    idx_a = np.zeros([data_len, limit['maxa']], dtype=np.int32)

    for i in range(data_len):
        q_indices = pad_seq(qtokenized[i], w2idx, limit['maxq'])
        a_indices = pad_seq(atokenized[i], w2idx, limit['maxa'])

        # print(len(idx_q[i]), len(q_indices))
        # print(len(idx_a[i]), len(a_indices))
        idx_q[i] = np.array(q_indices)
        idx_a[i] = np.array(a_indices)

    return idx_q, idx_a


def pad_seq(seq, lookup, maxlen):
    indices = []
    for word in seq:
        if word in lookup:
            indices.append(lookup[word])
        else:
            indices.append(lookup[UNK])
    return indices + [0] * (maxlen - len(seq))



def process_data():
    print('\n>> Read lines from file')
    qlines, alines = [],[]
    lines = read_lines(filename=FILENAME)

    # change to lower case (just for en)
    #lines = [line.lower() for line in lines]

    print('\n:: Sample from read(p) lines')
    print(lines[121:125])
    for i in range(0,len(lines)):
        qlines.append(lines[i].split(':')[0])
        alines.append(lines[i].split(':')[1])

    # convert list of [lines of text] into list of [list of words ]
    print('\n>> Segment lines into words')
    qtokenized = [wordlist.split() for wordlist in qlines]
    atokenized = [wordlist.split() for wordlist in alines]
    for element in qtokenized:
        for i in range(0,len(element)):
            element[i] =  element[i].replace("!","")
            element[i] =  element[i].replace("?","")
            element[i] =  element[i].replace(".","")
            element[i] =  element[i].replace("~","")


    for element in atokenized:
        for i in range(0,len(element)):
            element[i] =  element[i].replace("!","")
            element[i] =  element[i].replace("?","")
            element[i] =  element[i].replace(".","")
            element[i] =  element[i].replace("~","")

    print('\n:: Sample from segmented list of words')
    #print('\nq : {0} ; a : {1}'.format(qtokenized[60], atokenized[60]))
    #print('\nq : {0} ; a : {1}'.format(qtokenized[61], atokenized[61]))

    # indexing -> idx2w, w2idx : en/ta
    print('\n >> Index words')
    idx2w, w2idx, freq_dist = index_(qtokenized + atokenized, vocab_size=VOCAB_SIZE)

    print('\n >> Zero Padding')
    idx_q, idx_a = zero_pad(qtokenized, atokenized, w2idx)

    print('\n >> Save numpy arrays to disk')
    # save them
    np.save('idx_q.npy', idx_q)
    np.save('idx_a.npy', idx_a)

    # let us now save the necessary dictionaries
    metadata = {
        'w2idx': w2idx,
        'idx2w': idx2w,
        'limit': limit,
        'freq_dist': freq_dist
    }

    # write to disk : data control dictionaries
    with open('metadata.pkl', 'wb') as f:
        pickle.dump(metadata, f)


def load_data(PATH=''):
    # read data control dictionaries
    with open(PATH + 'metadata.pkl', 'rb') as f:
        metadata = pickle.load(f)
    # read numpy arrays
    idx_q = np.load(PATH + 'idx_q.npy')
    idx_a = np.load(PATH + 'idx_a.npy')
    return metadata, idx_q, idx_a


if __name__ == '__main__':
    process_data()