import os
import pandas as pd

class Loader(object):
    """docstring for Loader"""

    def __init__(self, datadir=""):
        if datadir == "":
            self.basedir = os.path.abspath(os.path.dirname(__file__))
            self.datadir = os.path.abspath(
                os.path.join(self.basedir, '../', 'data'))
        else:
            self.datadir = datadir

    def load_ArmPL(self, foldername,filename, NAME_LIST):
        # read the excel
        data = pd.read_excel(os.path.abspath(os.path.join(self.datadir, foldername,filename)), skiprows=[0])
        # change the names of the variables
        data.columns = NAME_LIST
        return data

    def load_Intervention(self, foldername,filename_lst, NAME_LIST):
        data_Int = pd.DataFrame(columns=NAME_LIST)
        for file_name in filename_lst:
            data_Int_tp = pd.read_excel(os.path.abspath(os.path.join(self.datadir,foldername,'Intervention' ,file_name)), skiprows=[0])
            data_Int_tp.drop(columns=[data_Int_tp.columns[0]], inplace=True)
            data_Int_tp.columns = NAME_LIST
            data_Int = data_Int.append(data_Int_tp, ignore_index=True)
        data_Int.dropna(axis=0, how='all',inplace=True)
        return data_Int