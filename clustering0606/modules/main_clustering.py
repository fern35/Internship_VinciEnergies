# Q: 1. Int_Solde & Pan_Solde are different, why? and Mise en securite == mise en provisoire
# 2. what is 'pan_SourceEqt'? Armoire
# 2. define the proper range of 'arm_NoLampe','lampe_Puissance'
# 3. regroup some categorical vars: 'pl_Reseau', 'pan_Solde'(deja), 'int_ElemDefaut', 'int_Solde'(deja), 'int_TypeInt'
# NLP: 'pan_Defaut', 'pan_SourceEqt', 'int_ElemDefaut', 'int_Defaut', 'int_Commentaire'
# 4. the eqt of BOGOR Int and Armoire/PL can not be linked ???
# code_eqt ok : Guadeloupe, Bessancourt, Bogor(only armoire), cavb, goussainville, montesson, noumea
# 5. pan_Defaut, Int_ElementDefaut: too many categories
# 6; pl_reseau, sup_Materiau, sup_type : repeated variables
#


from modules.clustering import Cluster
from modules.saver import Saver
from utils.constants import VILLE_NAME, Armoire_CLUSTERING, PL_CLUSTERING, Int_CLUSTERING
import pandas as pd
pd.set_option('display.max_columns', 100)

cluster = Cluster()
saver = Saver()
"""first merge the data of Armoire, PL of all the cities
attention: keep 'eq_code', add a column 'region', this step does not include encoding,
so we keep all the interesting variables which are not standard
we will retrieve the code at last, because we need to trace the non-standard variables at the last step
"""

data_Armoire = cluster.merge_file(foldername='Armoire', villelst=VILLE_NAME, add_region=True, Var_lst=Armoire_CLUSTERING)
# saver.save_excel(data_Armoire, foldername='Armoire',filename='Armoire_cluster_pre')

# data_PL = cluster.merge_file(foldername='PL', villelst=VILLE_NAME, add_region=True, Var_lst=PL_CLUSTERING)
# saver.save_excel(data_PL, foldername='PL', filename='PL_cluster_pre')

data_Int = cluster.merge_file(foldername='Int', villelst=VILLE_NAME, add_region=True, Var_lst=Int_CLUSTERING)
# saver.save_excel(data_Int, foldername='Int', filename='Int_cluster_pre')

"""then pre-processing of BDD Armoire, BDD PL, BDD Int
CAT: 1. simply encode (NA included)
2. reclassify(cluster) the variables (NA included)
3. for the non-standard categorical variables, use NLP detect the classes automatically (not completed)
"""
dict_encode_eq_Vetuste, data_Armoire_encode = cluster.cat_encode(data=data_Armoire, var='eq_Vetuste', regroup_dict=None)
data_Armoire_encode = cluster.num_encode(data=data_Armoire_encode, var = 'arm_NoLampe', proper_range=None)
# saver.save_excel(data_Armoire_encode, foldername='Armoire', filename='Armoire_cluster_encode')

# dict_encode_pl_Reseau, data_PL_encode = cluster.cat_encode(data=data_PL, var='pl_Reseau', regroup_dict=None)
# dict_encode_lan_Vetuste, data_PL_encode = cluster.cat_encode(data=data_PL_encode, var='lan_Vetuste', regroup_dict=None)
# dict_encode_lampe_Type, data_PL_encode = cluster.cat_encode(data=data_PL_encode, var='lampe_Type', regroup_dict=None)
# data_PL_encode = cluster.num_encode(data=data_PL_encode, var='pl_NoLanterne', proper_range=None)
# data_PL_encode = cluster.num_encode(data=data_PL_encode, var='lampe_Puissance', proper_range=None)
# print(dict_encode_pl_Reseau, dict_encode_lan_Vetuste, dict_encode_lampe_Type)
# saver.save_excel(data_PL_encode, foldername='PL', filename='PL_cluster_encode')

dict_encode_pan_TypeEqt, data_Int_encode = cluster.cat_encode(data=data_Int, var='pan_TypeEqt', regroup_dict=None)
dict_encode_pan_Solde, data_Int_encode = cluster.cat_encode(data=data_Int_encode, var='pan_Solde', regroup_dict={'Solde':['Soldé'], 'Nonsolde':['Mise en provisoire','Mise en sécurité''Problème non résolu','Mise en attente','En cours']})
dict_encode_int_Solde, data_Int_encode = cluster.cat_encode(data=data_Int_encode, var='int_Solde', regroup_dict={'Solde':['Soldé'], 'Nonsolde':['Mise en provisoire','Mise en sécurité','Problème non résolu','Mise en attente','En cours'], 'NA':['NA']})
data_Int_encode = cluster.num_encode(data=data_Int_encode, var='pan_DateSignal', proper_range=None)
data_Int_encode = cluster.num_encode(data=data_Int_encode, var='pan_DelaiInt', proper_range=None)
data_Int_encode = cluster.num_encode(data=data_Int_encode, var='int_DateIntervention', proper_range=None)
data_Int_encode = cluster.num_encode(data=data_Int_encode, var='int_Fin', proper_range=None)
# saver.save_excel(data_Int_encode, foldername='Int', filename='Int_cluster_encode')

"""after that, merge the data of Armoire, PL, Int
so that every row of the new dataframe will describle an armoire or a point lumineux
"""
data_Armoire_merge = data_Armoire_encode.head(5)
data_Armoire_merge.apply(lambda x: cluster.add_Int(data_row=x, data_Int=data_Int_encode), axis=1)

