import time
import os
import pandas as pd
import glob
list_csv = ["Static\output_misc.csv","Static\output_pol.csv","Static\output_tech.csv","Static\output_worl.csv"]

def build_train():
    path = 'Static/*.csv'
    all_files = glob.glob(path)
    data_list = []
    for filename in all_files:
        df = pd.read_csv(filename, header=None)
        data_list.append(df)
    df_concat = pd.concat(data_list, axis=0, ignore_index=True)
    df_concat.to_csv('Static/train.csv', index=False, header=None)

def fetch_data():
    import world
    import model
 
    for i in range (len(list_csv)):  
        model.summrise(list_csv[i])
    
    build_train()

while True:
    # your code here
    fetch_data()
    # sleep for 15 minutes before running the code again
    time.sleep(900)
