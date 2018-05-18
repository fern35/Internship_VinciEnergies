import pandas as pd
import os

class Loader(object):

    def __init__(self, datadir=""):
        if datadir == "":
            self.basedir = os.path.abspath(os.path.dirname(__file__))
            self.datadir = os.path.abspath(
                os.path.join(self.basedir,'../', 'source_data'))
        else:
            self.datadir = datadir

    def load_Callfile(self, filename, NAME_LIST):
        # read the excel
        data = pd.read_excel(os.path.abspath(os.path.join(self.datadir, filename)))
        # change the names of the variables
        data.columns = NAME_LIST
        return data