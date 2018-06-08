import os
import pandas as pd

class Saver(object):
    """docstring for Loader"""
    def __init__(self, datasavedir=""):
        if datasavedir == "":
            self.basedir = os.path.abspath(os.path.dirname(__file__))
            self.datasavedir = os.path.abspath(
                os.path.join(self.basedir, '../data_save'))
        else:
            self.datasavedir = datasavedir

    def save_excel(self, data,foldername,filename,):
        """save dataframe to excel"""
        save_path = self.datasavedir+'/excel/{}/{}.xlsx'.format(foldername,filename)
        try:
            os.remove(save_path)
        except OSError:
            pass
        writer = pd.ExcelWriter(save_path)
        data.to_excel(writer, 'Sheet1')
        writer.save()
        return data
