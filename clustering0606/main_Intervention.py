from utils.constants import Int_NAME, Int_TIME ,Int_INT_CAT,Int_INT_DIST,Int_PAN_CAT,Int_PAN_DIST
from modules.loader import Loader
from modules.cleaner import Cleaner
from modules.analyser import Analyzer
import datetime as dt

loader = Loader(datadir="/Users/zhangyuan/Documents/Workspace/StageCiteosWorkspace/data/noumea")
cleaner = Cleaner()
analyser = Analyzer()

Intfilename_lst = ["BDDExportInterventions-2018_05_15 du 01_01_2013 au 15_05_2018.xlsx"]

data_Int = loader.load_Intervention(filename_lst=Intfilename_lst, NAME_LIST=Int_NAME)
data_Int = cleaner.rv_dupRow(data_Int)
data_Int = cleaner.rep_dur(data_Int,Var_lst=Int_TIME,currtime=dt.datetime(2018, 5, 15, 0, 0, 0, 0))

data_Int_PAN = analyser.pick_Var(data=data_Int, Var_lst=Int_PAN_CAT+Int_PAN_DIST+['pan_Code'])
data_Int_PAN = cleaner.rv_dupRow(data=data_Int_PAN,Var_lst=['pan_Code'])
data_Int_INT = analyser.pick_Var(data=data_Int, Var_lst=Int_INT_CAT+Int_INT_DIST)
data_Int_INT = cleaner.rv_dupRow(data_Int_INT)

analyser.gen_NAN_excel(data_Int.iloc[:,0:23],'Intervention_int','Intervention_int_or')
analyser.gen_NAN_excel(data_Int.iloc[:,23:],'Intervention_pan','Intervention_pan_or')

analyser.gen_histogram_Pie(data_Int_INT, 'Intervention_int', Var_lst=Int_INT_CAT)
analyser.gen_histogram_Pie(data_Int_PAN, 'Intervention_pan', Var_lst=Int_PAN_CAT)

analyser.gen_Dist(data_Int_INT, 'Intervention_int', Var_lst=Int_INT_DIST)
analyser.gen_Dist(data_Int_PAN, 'Intervention_pan',Var_lst=Int_PAN_DIST)

analyser.gen_NAN_excel(data_Int_INT,'Intervention_int','Intervention_int')
analyser.gen_NAN_excel(data_Int_PAN,'Intervention_pan','Intervention_pan')

print(len(Int_NAME))

