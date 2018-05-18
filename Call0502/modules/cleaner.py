# -*- coding: utf-8 -*-

import string
import unidecode
import nltk
from nltk.metrics import edit_distance
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords


class Cleaner(object):

    def remove_space(self, data,var):
        new_data = data.copy()
        new_data[var] = new_data[var].apply(lambda x: x.strip())

        return new_data

    def lower_case(self, data,var):
        new_data = data.copy()
        new_data[var] = new_data[var].apply(lambda x: x.lower())

        return new_data

    def remove_punctuation_dataframe(self, data,var):
        new_data = data.copy()
        new_data[var] = new_data[var].apply(
            lambda x: self.remove_punctuation(x))

        return new_data

    def remove_punctuation(self, data):
        str_lang = string.punctuation
        for punctuation in str_lang:
            data = data.replace(punctuation, ' ')
        new_data = ' '.join(data.split())
        return new_data

    def remove_digits_dataframe(self, data,var):
        new_data = data.copy()
        new_data[var] = new_data[var].apply(
            lambda x: self.remove_digits(x))

        return new_data

    def remove_digits(self,data):
        str_lang = string.digits
        for punctuation in str_lang:
            data = data.replace(punctuation, ' ')
        new_data = ' '.join(data.split())
        return new_data

    def remove_stop_words_dataframe(self, data,var, language="french", stopwords_to_add=None):
        new_data = data.copy()
        if stopwords_to_add is None:
            stop_words = set(stopwords.words(language))
        else:
            assert isinstance(stopwords_to_add,
                              list), 'stopwords_to_add should be a list'
            nltk_stopwords = stopwords.words(language)
            stop_words = set(nltk_stopwords + stopwords_to_add)

        new_data[var] = new_data[var].apply(
            lambda x: self.remove_stop_words(x, stop_words))

        return new_data

    def remove_stop_words(self, data, stopwords):
        words = data.split()
        new_data = []

        for word in words:
            if word.lower() not in stopwords:
                new_data.append(word)

        new_data = " ".join(new_data)

        return new_data

    def unidecode_dataframe(self, data, var):
        new_data = data.copy()
        new_data[var] = new_data[var].apply(
            lambda x: unidecode.unidecode(x))

        return new_data

    def stemming_dataframe(self, data,var, language='french'):
        new_data = data.copy()
        snowball_stemmer = SnowballStemmer(language)
        new_data[var] = new_data[var].apply(
            lambda x: self.stemming_onerow(x, snowball_stemmer))

        return new_data

    def stemming_onerow(self, data, stemmer):
        words = data.split()
        new_data = []

        for word in words:
            word = stemmer.stem(word)
            new_data.append(word)

        new_data = ' '.join(new_data)

        return new_data

    def remove_empty(self, data,var):
        new_data = data[data[var] != '']

        return new_data

    def replace_digits_by_zero_dataframe(self, data,var):
        new_data = data.copy()
        new_data[var] = new_data[var].apply(
            lambda x: self.replace_digits_by_zero(x))

        return new_data

    def replace_digits_by_zero(self, data):
        digits = string.digits[1:]
        words = data.split()
        new_data = []
        for word in words:
            for digit in digits:
                word = word.replace(str(digit), str(0))
            new_data.append(word)

        new_data = ' '.join(new_data)

        return new_data

    def replace_day_month_dataframe(self, data,var):
        new_data = data.copy()
        new_data[var] = new_data[var].apply(
            lambda x: self.replace_day_month(x))

        return new_data

    def replace_day_month(self, data):
        days_list = ['lundi', 'mardi', 'mercredi',
                     'jeudi', 'vendredi', 'samedi', 'dimanche']
        months_list = ['janvier', 'février', 'fevrier', 'mars', 'avril', 'mai', 'juin',
                       'juillet', 'aout', 'août', 'septembre', 'octobre', 'novembre', 'decembre', 'décembre']
        words = data.split()
        new_data = []

        for word in words:
            if word.lower() in days_list:
                word = 'day'
            if word.lower() in months_list:
                word = 'month'
            new_data.append(word)

        new_data = " ".join(new_data)

        return new_data
