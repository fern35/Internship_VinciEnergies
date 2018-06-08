
from utils.constants import PL_NAME, PL_TIME,PL_PL_CAT,PL_PL_DIST,PL_LAN_CAT,PL_LAN_DIST
from modules.loader import Loader
from modules.cleaner import Cleaner
from modules.analyser import Analyzer
import datetime as dt

loader = Loader(datadir="/Users/zhangyuan/Documents/Workspace/StageCiteosWorkspace/data/noumea")
cleaner = Cleaner()
analyser = Analyzer()
data_PL = loader.load_ArmPL(filename="BDDExport_PointLumineux_NOUMEA_2018-05-15.xlsx", NAME_LIST=PL_NAME)

data_PL = cleaner.rv_dupRow(data_PL)
data_PL = cleaner.rep_dur(data_PL,Var_lst=PL_TIME,currtime=dt.datetime(2018, 5, 5, 0, 0, 0, 0))

data_PL_PL = analyser.pick_Var(data=data_PL, Var_lst=PL_PL_CAT+PL_PL_DIST)
data_PL_LAN = analyser.pick_Var(data=data_PL, Var_lst=PL_LAN_CAT+PL_LAN_DIST)
data_PL_PL = cleaner.rv_dupRow(data_PL_PL)

analyser.gen_NAN_excel(data_PL.iloc[:,0:60],'PL_PL','PL_PL_or')
analyser.gen_NAN_excel(data_PL.iloc[:,60:],'PL_LAN','PL_LAN_or')

analyser.gen_histogram_Pie(data_PL_PL, 'PL_PL', Var_lst=PL_PL_CAT)
analyser.gen_histogram_Pie(data_PL_LAN, 'PL_LAN', Var_lst=PL_LAN_CAT)

analyser.gen_Dist(data_PL, 'PL_PL', Var_lst=PL_PL_DIST)
analyser.gen_Dist(data_PL_LAN,'PL_LAN',Var_lst=PL_LAN_DIST)

analyser.gen_NAN_excel(data_PL_PL,'PL_PL','PL_PL')
analyser.gen_NAN_excel(data_PL_LAN,'PL_LAN','PL_LAN')

# print(len(PL_NAME))