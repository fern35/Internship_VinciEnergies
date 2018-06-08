import os
import pandas as pd
from docx import Document
import pandas as pd
import matplotlib.pyplot as plt
from docx.shared import Inches
import seaborn as sns
from utils.constants import Armoire_GROUP,Armoire_PICK
from utils.constants import PL_GROUP,PL_PICK
from utils.constants import Int_GROUP,Int_PICK
from utils.constants import VILLE_NAME

class Cluster(object):
    def __init__(self, datasavedir=""):
        if datasavedir == "":
            self.basedir = os.path.abspath(os.path.dirname(__file__))
            self.datasavedir = os.path.abspath(
                os.path.join(self.basedir, '../data_save'))
        else:
            self.datasavedir = datasavedir

    def merge_file(self, foldername='Armoire', villelst=VILLE_NAME, add_region=True, Var_lst=None):
        # retrieve the column names
        data_forcol = pd.read_excel(os.path.abspath(
            os.path.join(self.datasavedir, 'excel/{}/{}_{}.xlsx'.format(foldername, foldername, villelst[0]))))
        merge_data = pd.DataFrame(columns=data_forcol.columns)

        for ville in villelst:
            data_tp = pd.read_excel(os.path.abspath(
                os.path.join(self.datasavedir, 'excel/{}/{}_{}.xlsx'.format(foldername, foldername, ville))))
            data_tp['region'] = ville
            merge_data = pd.concat([merge_data, data_tp])

        if Var_lst is not None:
            merge_data = merge_data[Var_lst+['region']]
        if not add_region:
            merge_data.drop(['region'], axis=1, inplace=True)

        merge_data.reset_index(inplace=True, drop=True)
        merge_data.drop_duplicates(inplace=True)
        return merge_data

    def cat_encode(self, data, var, regroup_dict=None):
        """

        :param data:
        :param var:
        :param one_hot:
        :param regroup_dict: dict(new class: [old classes])
        :return:
        """
        new_data = data.fillna(value={var:'NA'})
        grouped = data.groupby(new_data[var])
        classes = list(grouped.groups.keys())
        def rep_vsdict(key,dict):
            return dict[key]

        if regroup_dict is None:
            dict_encode = dict(zip(classes, range(len(classes))))
            new_data[var+'_encode'] = new_data[var].apply(lambda x: rep_vsdict(x, dict=dict_encode))
        else:
            dict_encode = dict(zip(regroup_dict.keys(), range(len(regroup_dict))))
            dict_encode_ = dict.fromkeys(classes, None)
            for key, values in regroup_dict.items():
                for value in values:
                    assert value in classes, "The value: {} of group_dict does not correspond to the actual classes".format(value)
                    dict_encode_[value] = dict_encode[key]
            new_data[var+'_encode'] = new_data[var].apply(lambda x: rep_vsdict(x, dict=dict_encode_))

        return dict_encode, new_data

    def num_encode(self, data, var, proper_range=None):
        new_data = data.copy()
        new_data[var+'_NA'] = new_data[var].isnull().apply(lambda x: x*1)
        print(new_data[var+'_NA'].head())
        new_data = new_data.fillna(value={var: 0})
        if proper_range is not None:
            new_data[var] = new_data[var].clip(proper_range[0], proper_range[1])
        return new_data


