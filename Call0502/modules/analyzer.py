from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.corpus import stopwords
import numpy as np
import pandas as pd

class Analyzer(object):

    def get_tfidf(self,data,var,max_features,ngram_range,stopwprds,strip_accents=None):
        """
        generate tf-idf matrix for thr documents
        :param data: dataframe that need to be dealt with
        :param var: the column which includes the target text
        :param max_features: the number of features that we choose
        :param ngram_range: the ngram mode
        :param stopwprds: stopwords list
        :param strip_accents: Remove accents during the preprocessing step
        :return: term-document matrix(tf-idf value) and feature names
        """
        tfidfvectorizer = TfidfVectorizer(max_features=max_features,
                                          ngram_range=ngram_range,
                                          stop_words=stopwords,
                                          strip_accents=strip_accents)

        termdoc_matrix = tfidfvectorizer.fit_transform(data[var])
        feature_names = tfidfvectorizer.get_feature_names()
        return termdoc_matrix,feature_names

    def get_freq_idf(self,data,var,max_features=None, ngram_range=(1,1),strip_accents=None):
        """
        generate files for analyzing the term frequency(in all documents) and
        the term frequency(in all documents) weighed by inverse document frequency
        :param data: dataframe that need to be dealt with
        :param max_features: the number of features that we choose
        :param ngram_range: the ngram mode
        :param strip_accents: Remove accents during the preprocessing step
        :return: dataframes of term frequency(in all documents), idf,
                term frequecy(in all documents) weighted by idf
        """
        text = data[var]
        countvectorizer = CountVectorizer(max_features=max_features,
                                          ngram_range=ngram_range,
                                          strip_accents=strip_accents)

        tfidfvectorizer = TfidfVectorizer(max_features=max_features,
                                          ngram_range=ngram_range,
                                          strip_accents=strip_accents)

        # frequency in all documents
        count_termdoc = countvectorizer.fit_transform(text)
        total_count = np.sum(count_termdoc)
        freq = count_termdoc.sum(axis = 0)/total_count
        count_vocab = countvectorizer.vocabulary_
        count_vocab_tp = count_vocab.copy()
        # idf
        tfidf_termdoc = tfidfvectorizer.fit_transform(text)
        idf_matrix = tfidfvectorizer.idf_
        tfidf_vocab = tfidfvectorizer.vocabulary_
        tfidf_vocab_tp = tfidf_vocab.copy()

        for k1, v1 in count_vocab.items():
            count_vocab_tp[k1] = freq[0,v1]

        for k2,v2 in tfidf_vocab.items():
            tfidf_vocab_tp[k2] = idf_matrix[v2]

        df_count = pd.DataFrame(list(count_vocab_tp.items()), columns=['Term', 'Frequency'])
        df_idf = pd.DataFrame(list(tfidf_vocab_tp.items()), columns=['Term', 'IDF'])
        df_freqidf = pd.DataFrame(columns=['Term', 'Freq_IDF'])
        df_freqidf['Term'] = df_count['Term']
        df_freqidf['Freq_IDF'] = df_idf['IDF'].as_matrix()*df_count['Frequency'].as_matrix()

        df_count.sort_values(ascending=False,by=['Frequency'],inplace=True)
        df_idf.sort_values(ascending=False,by=['IDF'],inplace=True)
        df_freqidf.sort_values(ascending=False, by=['Freq_IDF'], inplace=True)
        return df_count, df_idf, df_freqidf

