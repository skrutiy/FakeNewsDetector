import os
import csv
import numpy as np
import gensim
import re

def process_train_data(train_path, n_articles, n_words, max_words=2000, min_words=50):
    ''' method to read in the training data
    and shape it into the correct dimensions '''
    word_embeddings = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)

    train_data = []
    train_file = open(train_path, 'r', encoding='utf8')
    train_str = train_file.readlines()

    csv.field_size_limit(100000000)
    n_1 = 0
    for entry in csv.reader(train_str, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
        if n_1 < n_articles:
            train_data.append(entry)
            n_1 += 1
        else:
            break

    #train_x = []
    train_x = np.zeros((n_articles-1, n_words*300))
    train_y = np.zeros((n_articles-1, 2))
    # print(train_x.shape)
    # print(train_y.shape)

    removed = 0

    for i, data in enumerate(train_data[1:]):
        # print("Converting article: ", data[1], "...")
        rmv_pnc = re.sub(r'[^\w\s]', '', data[3])
        words = rmv_pnc.split()
        if len(words) > min_words and len(words) < max_words:
            n_2 = 0
            word_matrix = []
            for word in words:
                # print(word)
                if n_2 < n_words:
                    if word in word_embeddings:
                        # print(word, " was in the embedding")
                        embedding = word_embeddings[word]
                        word_matrix.extend(embedding)
                        n_2 += 1

            if(len(word_matrix) < train_x.shape[1]):
                padding = np.zeros(train_x.shape[1]-len(word_matrix))
                word_matrix.extend(padding)

            label = data[4]
            if int(label) == 0:
                train_y[i] = [1, 0]
            else:
                train_y[i] = [0, 1]
            # print(len(word_matrix))
            train_x[i] = word_matrix
        else:
            removed += 1

        # print("len(word_matrix):", len(word_matrix))
        #
        # print("words in article: ", len(data[3].split()))
        # print("shape of word matrix: ", np.array(word_matrix).shape)

    # testing size of training data
    # for article in training:
    #     print(article[0].shape, " ", article[1])
    #     if article[0].shape[0]%300 is not 0:
    #         print("bruh its rong")
    train_x, train_y = train_x[-removed:], train_y[-removed:]
    print("x shape: ", train_x.shape)
    print("y shape: ", train_y.shape)

    print("Articles removed because of length: ", removed)

    return train_x, train_y

# Returns two tuples (train_x, train_y), (test_x, test_y)


#---------------------------------

def get_original_test_data(path, percentage, n_articles):

    split_idx = int(percentage*n_articles-1)
 
    test_data = []
 
    file = open(path, 'r', encoding='utf8')
 
    string = file.readlines()
 
    n_1 = 0  # TEMP FIX, WANT TO PASS BATCHES INTO READER TO GET ALL DATA.
    for entry in csv.reader(string, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
        if n_1 < n_articles:
            if n_1 < split_idx:
                # print('id: ', entry[0])
                # print('title: ', entry[1])
                # print('author: ', entry[2])
                # print('text: ', entry[3])
                # print('label: ', entry[4])
                n_1 += 1
            else:
                test_data.append(entry)
                n_1 += 1
        else:
            break

    test_data.pop(0)
    print(np.array(test_data).shape)
     # Data now organized in nested list, now need to embed the words for each article.
 
    return test_data


#---------------------------------

# TODO: Implement optional shuffle
def train_test_split(x, y, percentage, shuffle=False):
    if shuffle:
        zipped = zip(x, y)
        zipped = list(zipped)
        np.random.shuffle(zipped)
        x, y = zip(*zipped)
        print(type(x))

    split_idx = int(percentage*len(x))

    train_x = x[:split_idx]
    test_x = x[split_idx:]

    train_y = y[:split_idx]
    test_y = y[split_idx:]

    return (train_x, train_y), (test_x, test_y)


def withhold_data(training_data, percentage):
    train_size = int(percentage * len(training_data))
    train_data = training_data[:train_size]
    withheld_data = training_data[train_size:]

    return train_data, withheld_data


#train_data, test_data = process_csv_data('../data/train.csv', '../data/test.csv', 10, 5)

# tx, ty = process_train_data('../data/train.csv', 10, 100)

# x, y = process_train_data('../data/train.csv', 50, 100)

# train, test = train_test_split(x, y, 0.6)

#test_data = get_original_test_data('../data/train.csv', .8, 1000)
#print(test_data)




