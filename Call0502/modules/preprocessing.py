import pandas as pd
import numpy as np

class Processor(object):

    def merge_col(self,data,Var_lst):
        """
        merge several columns of the dataframe

        """
        def _merge(data):
            str_list = []
            for var in Var_lst:
                str_list.append(data[var])
            return ' '.join(str_list)

        new_data = data.copy()
        new_data ['merge'] = new_data.apply(_merge,axis=1)

        return new_data

    def merge_cluster(self,data,labels,n_cluster):
        df = pd.DataFrame(columns=['cluster_index','cluster_size','Date','merge'])
        clustersize_lst=[]
        for i in range(1,n_cluster+1):
            cluster_size,dfcluster=self.getcluster_index(data,labels,i)
            clustersize_lst.append(cluster_size)
            df=df.append(dfcluster, ignore_index=True)
        return clustersize_lst,df

    def getcluster_index(self,data,labels,cluster_index):
        # the index of the mails which belong to the cluster
        index_data=np.where(labels == cluster_index)[0].tolist()

        cluster_size=len(index_data)

        newdf = pd.concat([data['Date'][index_data], data['merge'][index_data]], axis=1)
        newdf.reset_index(drop=True, inplace=True)
        index_size_df = pd.DataFrame({'cluster_index': [cluster_index for i in range(cluster_size)], 'cluster_size': [cluster_size for i in range(cluster_size)]})
        index_size_df.reset_index(drop=True, inplace=True)
        result = pd.concat([newdf,index_size_df],axis=1)
        return cluster_size,result