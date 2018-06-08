
from utils.constants import Armoire_NAME ,Armoire_ARM_CAT ,Armoire_DEPART_CAT,Armoire_TIME,Armoire_ARM_DIST
from modules.loader import Loader
from modules.cleaner import Cleaner
from modules.analyser import Analyzer
import datetime as dt


loader = Loader(datadir="/Users/zhangyuan/Documents/Workspace/StageCiteosWorkspace/data/noumea")
cleaner = Cleaner()
analyser = Analyzer()

# load the data
data_Ar = loader.load_ArmPL(filename="BDDExport_ArmoireBt_NOUMEA_2018-05-15.xlsx", NAME_LIST=Armoire_NAME)

# remove the duplicated rows and replace the date with the duration
data_Ar = cleaner.rv_dupRow(data_Ar)
data_Ar = cleaner.rep_dur(data_Ar,Var_lst=Armoire_TIME,currtime=dt.datetime(2018, 5, 5, 0, 0, 0, 0))

# generate the count for NAN for all the variables
analyser.gen_NAN_excel(data_Ar.iloc[:,0:43],'Armoire_arm','Armoire_arm_or')
analyser.gen_NAN_excel(data_Ar.iloc[:,43:],'Armoire_depart','Armoire_depart_or')

# pick the variables and regroup
data_Ar_arm = analyser.pick_Var(data=data_Ar, Var_lst=Armoire_ARM_CAT+Armoire_ARM_DIST)
data_Ar_depart = analyser.pick_Var(data=data_Ar, Var_lst=Armoire_DEPART_CAT)

# clear the duplicated rows for 'armoires'
data_Ar_arm = cleaner.rv_dupRow(data_Ar_arm)

# generate statistical characteristics
analyser.gen_histogram_Pie(data_Ar_arm, 'Armoire_arm', Var_lst=Armoire_ARM_CAT)
analyser.gen_histogram_Pie(data_Ar_depart, 'Armoire_depart', Var_lst=Armoire_DEPART_CAT)

analyser.gen_Dist(data_Ar_arm, 'Armoire_arm', Var_lst=Armoire_ARM_DIST)

analyser.gen_NAN_excel(data_Ar_arm,'Armoire_arm','Armoire_arm')
analyser.gen_NAN_excel(data_Ar_depart,'Armoire_depart','Armoire_depart')