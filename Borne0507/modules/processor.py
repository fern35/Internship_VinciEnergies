import io
import pandas as pd


class Processor(object):

    def retriv_startstop(self,path,file_name):
        """
        retrieve the information about startTransaction/stopTransaction from the txt data
        :param path: the folder in which exists the txt file we want to deal with
        :param file_name: the name of the txt file
        :return: titlename and three dataframes corresponding to the startTransaction(ID=1,2) and stopTransaction
        """
        # the temperal container for message start, stop
        df_start1 = pd.DataFrame(columns=['connectorID', 'time', 'meter','mode'])
        df_start2 = pd.DataFrame(columns=['connectorID', 'time', 'meter','mode'])
        df_stop = pd.DataFrame(columns=['connectorID', 'time', 'meter','mode'])
        title_name = ''
        # read the file line by line
        with io.open(path+file_name+'.txt', encoding='utf-8') as f:
            # buffer list for saving the last line
            buffer_line = ['0']
            # buffer dictionary for df_start1, df_start2, df_stop
            buffer_dict1 = {'time':'0','connectorID':0,'meter':0,'mode':'start'}
            buffer_dict2 = {'time':'0','connectorID':0,'meter':0,'mode':'start'}
            buffer_dict3 = {'time':'0','connectorID':'','meter':0,'mode':'stop'}

            index_start1 = 0
            index_start2 = 0
            index_stop = 0

            start_signal1 = False
            start_signal2 = False
            stop_signal = False


            for i, line in enumerate(f):
                # current line
                line = line.strip('\n')

                # the first line indicates the source "borne" of the data
                if i == 0:
                    title_name = line

                # retrieve the last line from the buffer list and replace it with the current line
                last_line = buffer_line[0]
                buffer_line.pop(0)
                buffer_line.append(line)
                #split the current line by '\t'
                str_line = line.split('\t')

                # if we encounter startTransaction ID=1,or ID=2
                if str_line[0] == "/StartTransaction":
                    #print("Start Transaction======")
                    if str_line[1][-2] == '1':
                        #print('ID1')
                        start_signal1 = True
                        index_start1 = 1
                        buffer_dict1['connectorID'] = str_line[1][-2]
                        buffer_dict1['time'] = last_line
                    elif str_line[1][-2] == '2':
                        #print('ID2')
                        start_signal2 = True
                        index_start2 = 1
                        buffer_dict2['connectorID'] = str_line[1][-2]
                        buffer_dict2['time'] = last_line

                # if we are in the process of one transaction ID =1
                elif start_signal1 and str_line[0] != "/StopTransaction":
                    if index_start1 == 1 and index_stop == 0:
                        index_start1 += 1
                    elif index_start1 == 2 and index_stop== 0:
                        meter_str = str_line[0].split()[1].strip(',')
                        buffer_dict1['meter'] = int(meter_str)
                        # save one row of df and empty the dict
                        index_start1 = 0
                        start_signal1 = False
                        df_start1 = df_start1.append(buffer_dict1, ignore_index=True)


                # if we are in the process of one transaction Id=2
                elif start_signal2 and str_line[0] != "/StopTransaction":
                    if index_start2 == 1 and index_stop == 0:
                        index_start2 += 1
                    elif index_start2 ==2 and index_stop == 0:
                        meter_str = str_line[0].split()[1].strip(',')
                        buffer_dict2['meter'] = int(meter_str)
                        # save one row of df and empty the dict
                        index_start2 = 0
                        start_signal2 = False
                        df_start2 = df_start2.append(buffer_dict2, ignore_index=True)


                # if we encounter stop transaction
                # first decide which ID
                elif str_line[0] == "/StopTransaction":
                    buffer_dict3['time'] = last_line
                    index_stop = 1
                    stop_signal = True

                elif stop_signal :
                    if index_stop == 1 :
                        index_stop += 1
                    elif index_stop == 2:
                        buffer_dict3['meter'] = int(str_line[0].split()[-1])
                        index_stop = 0
                        stop_signal = False
                        df_stop = df_stop.append(buffer_dict3, ignore_index=True)

            df_start1['time'] = pd.to_datetime(df_start1['time'])
            df_start2['time'] = pd.to_datetime(df_start2['time'])
            df_stop['time'] = pd.to_datetime(df_stop['time'])
            return title_name, df_start1, df_start2, df_stop

    def merge_sort(self,path,title_name,df_lst,by='time'):
        df_result = pd.concat(df_lst)
        
        df_result.to_excel(path + title_name + '_sorttemp.xlsx')
        df_result.sort_values(by=by,inplace=True)
        df_result.to_excel(path+title_name+'_sorttemp.xlsx')
        return df_result

    def gen_conso(self,path, title_name,df_source):
        df_result = pd.DataFrame(columns=['ConnectorID', 'Start', 'Stop', 'Duration', 'Consumption'])
        dict_tp = {'ConnectorID': 0, 'Start': '0', 'Stop': '0', 'Duration': '0', 'Consumption': 0}

        for i in range(int(len(df_source) / 2)):
            row1 = df_source.iloc[i * 2]
            row2 = df_source.iloc[i * 2 + 1]
            print('i: ', i)
            dict_tp['ConnectorID'] = int(row1['connectorID'])
            dict_tp['Start'] = row1['time']
            dict_tp['Stop'] = row2['time']
            dict_tp['Consumption'] = int(row2['meter']) - int(row1['meter'])
            dict_tp['Duration'] = pd.to_datetime(row2['time']) - pd.to_datetime(row1['time'])
            df_result = df_result.append(dict_tp, ignore_index=True)

        df_result.to_excel(path+title_name+'_result.xlsx')
