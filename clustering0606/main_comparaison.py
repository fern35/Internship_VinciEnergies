from utils.constants import  Armoire_PICK,Armoire_GROUP,Armoire_NAME ,Armoire_ARM_CAT ,Armoire_DEPART_CAT,Armoire_TIME,Armoire_ARM_DIST
from utils.constants import PL_PICK,PL_GROUP,PL_NAME, PL_TIME,PL_PL_CAT,PL_PL_DIST,PL_LAN_CAT,PL_LAN_DIST
from utils.constants import Int_PICK,Int_GROUP,Int_NAME, Int_TIME ,Int_INT_CAT,Int_INT_DIST,Int_PAN_CAT,Int_PAN_DIST
from utils.constants import VILLE_NAME
from modules.loader import Loader
from modules.cleaner import Cleaner
from modules.analyser import Analyzer
from modules.saver import Saver
import datetime as dt
import pandas as pd

save_path = 'D:\\Users\\Yuan.ZHANG\\PycharmProjects\\compa0516\\data_save'
CURRENT_TIME_AP = '2018-05-15'
CURRENT_TIME_INT = '2018_05_15'
Intfilename_lst = ["BDDExportInterventions-{} du 01_01_2013 au 15_05_2018.xlsx".format(CURRENT_TIME_INT)]
loader = Loader(datadir="D:\\Users\Yuan.ZHANG\\PycharmProjects\\data")

saver = Saver()
cleaner = Cleaner()
analyzer = Analyzer()

# # standardize the format of the dataframe
# for ville in VILLE_NAME:
#     # rename the dataframe,remove redundant info and save
#     data_Arm = loader.load_ArmPL(foldername=ville,filename="BDDExport_ArmoireBt_{}_{}.xlsx".format(ville,CURRENT_TIME_AP), NAME_LIST=Armoire_NAME)
#     data_PL = loader.load_ArmPL(foldername=ville,filename="BDDExport_PointLumineux_{}_{}.xlsx".format(ville,CURRENT_TIME_AP), NAME_LIST=PL_NAME)
#     data_Int = loader.load_Intervention(foldername=ville,filename_lst=Intfilename_lst, NAME_LIST=Int_NAME)
#
#     data_Arm = cleaner.rv_dupRow(data_Arm)
#     data_Ar = cleaner.rep_dur(data_Arm, Var_lst=Armoire_TIME, currtime=dt.datetime(2018, 5, 15, 0, 0, 0, 0))
#     data_PL = cleaner.rv_dupRow(data_PL)
#     data_PL = cleaner.rep_dur(data_PL, Var_lst=PL_TIME, currtime=dt.datetime(2018, 5, 15, 0, 0, 0, 0))
#     data_Int = cleaner.rv_dupRow(data_Int)
#     data_Int = cleaner.rep_dur(data_Int, Var_lst=Int_TIME, currtime=dt.datetime(2018, 5, 15, 0, 0, 0, 0))
#
#     saver.save_excel(data_Arm,foldername='Armoire',filename='Armoire_{}'.format(ville))
#     saver.save_excel(data_PL,foldername='PL',filename='PL_{}'.format(ville))
#     saver.save_excel(data_Int,foldername='Intervention',filename='Int_{}'.format(ville))

# generate document for describing the condition of NAN of each group
# analyzer.gen_groupCompl_cities(foldername='Armoire',group_dict=Armoire_GROUP,threshold=0.05)
# analyzer.gen_groupCompl_cities(foldername='Int',group_dict=Int_GROUP,threshold=0.05)
# analyzer.gen_groupCompl_cities(foldername='PL',group_dict=PL_GROUP,threshold=0.05)

# generate common variables which satifies the according requirement
# Var_Arm = analyzer.gen_VarIntersection(foldername='Armoire',villelst=VILLE_NAME,group_dict=Armoire_GROUP,threshold=0.9)
# Var_PL = analyzer.gen_VarIntersection(foldername='PL',villelst=VILLE_NAME,group_dict=PL_GROUP,threshold=0.9)
# Var_Int = analyzer.gen_VarIntersection(foldername='Int',villelst=['CAVB','BESSANCOURT','GOUSSAINVILLE','GUADELOUPE','MONTESSON','NOUMEA'],group_dict=Int_GROUP,threshold=0.9)

# generate the distribution for variables vs cities
# 1. input: var_lst
# try to save the distribution of one var for different cities in a dataframe and use pd.plot
# 2. output: image
# analyzer.comp_Var_cities(foldername='Armoire',villelst=VILLE_NAME,group_dict= Armoire_PICK)
# analyzer.comp_Var_cities(foldername='Int',villelst=VILLE_NAME,group_dict= Int_PICK)
analyzer.comp_Var_cities(foldername='PL',villelst=VILLE_NAME,group_dict= PL_PICK)
