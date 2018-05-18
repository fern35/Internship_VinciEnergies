from datetime import datetime
import os
from matplotlib import rcParams
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.cluster.hierarchy import dendrogram

class Plotter(object):
    """docstring for Plotter"""

    def __init__(self):
        """

        Parameters
        ----------

        Returns
        -------
        void
        """
        rcParams.update({'figure.autolayout': True})
        self.basedir = '/Users/zhangyuan/Documents/Workspace/StageCiteosWorkspace/Call0502/save_data'

    def plot_dendro(self,hcluster,title):
        fig=plt.figure(figsize=(25, 10))
        plt.title(title)
        plt.xlabel('sample index')
        plt.ylabel('distance')
        dendrogram(
            hcluster,
            leaf_rotation=90.,
            leaf_font_size=12,
            # count_sort=True,
            # distance_sort=True,
            show_leaf_counts=True
        )
        plt.show()
        fig.savefig(os.path.abspath(os.path.join(
            self.basedir, 'img','{0}.png'.format(title))))

    def fancy_dendrogram(sef,title,showdist,*args, **kwargs):
        """
        Description

        personalize the dendrogram
        """
        max_d = kwargs.pop('max_d', None)
        if max_d and 'color_threshold' not in kwargs:
            kwargs['color_threshold'] = max_d
        annotate_above = kwargs.pop('annotate_above', 0)
        ddata = dendrogram(*args, **kwargs)
        # fig = plt.figure(figsize=(25, 10))
        if not kwargs.get('no_plot', False):
            plt.title(title)
            plt.xlabel('sample index or (cluster size)')
            plt.ylabel('distance')
            for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
                x = 0.5 * sum(i[1:3])
                y = d[1]
                if y > annotate_above:
                    if showdist:
                    #plt.plot(x, y, 'o', c=c)
                        plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                                 textcoords='offset points',
                                 va='top', ha='center')
            if max_d:
                plt.axhline(y=max_d, c='k')

        return ddata

    def plot_fancy(self,title,hcluster,cutoff):
        fig = plt.figure()
        # fig = plt.figure(figsize=(25, 10))
        self.fancy_dendrogram(title, showdist=False,
                                 Z=hcluster,
                                 # truncate_mode='lastp',
                                 # p=50,
                                 leaf_rotation=90.,
                                 leaf_font_size=12.,
                                 annotate_above=10,
                                 max_d=cutoff,  # plot a horizontal cut-off line
                                 )
        plt.show()
        fig.savefig(os.path.abspath(os.path.join(
            self.basedir, 'FancyDendrogram','{0}.png'.format(title))))

if __name__ == '__main__':
    plotter = Plotter()
    x = np.random.rand(10)
    y = np.ran
