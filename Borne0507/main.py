
from modules.processor import Processor

# path
source_folder= "/Users/zhangyuan/Documents/Workspace/StageCiteosWorkspace/Borne0507/source_data/"
result_folder= "/Users/zhangyuan/Documents/Workspace/StageCiteosWorkspace/Borne0507/result_data/"
source_file = "Borne SBM-21SMO-043"

processor = Processor()

#retrieve the information of startTransaction, stopTransaction
title_name, df_start1, df_start2, df_stop = processor.retriv_startstop(source_folder,source_file)

# merge the dataframe which stores the info of startTransaction, stopTransaction. Sort the result
df_sort = processor.merge_sort(path=result_folder,title_name=title_name,df_lst=[df_start1,df_stop,df_start2])

# then check the excel file and remove the anomalies

# use the correct excel file to generate the final result.
df_result = processor.gen_conso(result_folder,title_name,df_sort)