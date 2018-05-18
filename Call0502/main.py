
from modules.preprocessing import Processor
from modules.loader import Loader
from modules.analyzer import Analyzer
from utils.constants import Var_NAME,STOP_LIST
from modules.cleaner import Cleaner
from modules.plotter import Plotter
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


savepath = "/Users/zhangyuan/Documents/Workspace/StageCiteosWorkspace/Call0502/save_data/"
# ==================load the data==================
loader = Loader()
Call_file = "Reporting Call Freshmile.xlsx"
raw_data = loader.load_Callfile(filename=Call_file, NAME_LIST=Var_NAME)

# ================merge "problem" and "action"====================
processor = Processor()
# raw_data = processor.merge_col(data,Var_lst=['Problem','Action'])

# ================remove stop words, numbers, punctuation, operator, tokenize， stemming===========
cleaner = Cleaner()
data = cleaner.remove_digits_dataframe(raw_data,var='Problem')
data.to_excel(savepath+'tp_rv_digits.xlsx')

data = cleaner.remove_punctuation_dataframe(data,var='Problem')
data.to_excel(savepath+'tp_rv_punctuation.xlsx')

data = cleaner.remove_stop_words_dataframe(data,stopwords_to_add=STOP_LIST,var='Problem')
data.to_excel(savepath+'tp_rv_stopwords.xlsx')

# data = cleaner.stemming_dataframe(data)
# data.to_excel(savepath+'tp_rv_stemming.xlsx')

data = cleaner.unidecode_dataframe(data,var='Problem')
data.to_excel(savepath+'tp_rv_unidecode.xlsx')

# =======================tf-idf analysis======================
analyzer = Analyzer()
df_count, df_idf, df_freqidf = analyzer.get_freq_idf(data,var='Problem')

df_count.to_excel(savepath+'without_stopwords/freq_all.xlsx')
df_idf.to_excel(savepath+'without_stopwords/idf_all.xlsx')
df_freqidf.to_excel(savepath+'without_stopwords/freq_IDF.xlsx')

# ===================apply hierarchical clustering====================
plotter = Plotter()

tfidfvectorizer = TfidfVectorizer(max_features=100,
                                  ngram_range=(1,2))

termdoc_matrix = tfidfvectorizer.fit_transform(data['Problem'])
hcluster_bi = linkage(termdoc_matrix.toarray(), 'ward')
plotter.plot_dendro(hcluster_bi, 'Dendrogram_stem_bigram')

# choose the number of clusters according to dendrogram
n_cluster = 7
labels = fcluster(hcluster_bi, n_cluster , criterion='maxclust')
clustersize_lst,df_merge = processor.merge_cluster(data=raw_data,labels=labels,n_cluster=n_cluster )
df_merge.to_excel(savepath+'/HC_cluster{}.xlsx'.format(n_cluster))
