import adi # adicht driver
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import argparse

# https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def progressBar(current, total, barLength = 20): # copied from https://stackoverflow.com/questions/6169217/replace-console-output-in-python
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')  


def main_generate_csv(filename, folder = ""):
    f = adi.read_file(filename)
    final_list = []
    print(f'Computing for {filename}...')

    # my files here have a poll rate of 1000 Hz. so index is 1 ms
    # f.channels
    for record_id in range(1, f.n_records):
        channel_id = 1
        # print(record_id)
        # record_id = 2
        progressBar(record_id, f.n_records+1)
        data = f.channels[channel_id-1].get_data(record_id)
        
        # plt.plot(data)
        # plt.show()

        peak_tension = np.max(data) - np.min(data)

        # in theory you should compute np.argmax(data) first and store it as char, but apparently it is "blazingly fast"
        # create a new array containing only the values before the maximum. Python starts from 0 hence the +1...
        bef_peak_vals = data[0:np.argmax(data)+1] 
        time_to_peak_tension = np.argmax(data) - np.argmin(bef_peak_vals)

        # t1/2r
        after_peak_vals = data[np.argmax(data)+1:] # find peak values after
        x = find_nearest(after_peak_vals, peak_tension/2) # find half response value
        time_to_half_resp = np.max(np.where(after_peak_vals == x)) # find index of half resp time AFTER THE CUTOFF

        # make dataframe
        drug_type = filename.lstrip(folder).rstrip('.adicht')
        add_array = [record_id, drug_type, peak_tension, time_to_peak_tension, time_to_half_resp]
        final_list.append(add_array) # store as list of lists initially

    return final_list


if __name__ == "__main__":
    # argument parser
    parser = argparse.ArgumentParser(description='Script to extract peak_tension, time_to_peak_tension, time_to_half_resp from a folder of adicht files.')
    parser.add_argument('-i', '--folder', type=str, help = "Folder with input .adicht files, provide in format './folder")
    parser.add_argument('-o', '--output', type=str, default="results.csv", help = "Output csv file to store the results. Defaults to results.csv")
    args = parser.parse_args() # parse argument

    # mypath = "./drugs"
    mypath = args.folder
    adchart_files = [f for f in os.listdir(mypath) if (os.path.isfile(os.path.join(mypath, f)) and f.endswith('.adicht'))] # get only files in subfolder with ending .adicht
    storage_list = []
    for file in adchart_files:
        filepath = f"{mypath}/{file}" # kludgy but it will do for now
        new_list = main_generate_csv(filename = filepath, folder = mypath)
        storage_list.extend(new_list)

    # then finally convert to array and dump
    final_array = np.array(storage_list)
    df = pd.DataFrame(data = final_array, columns = ['record_id', 'drug_type', 'peak_tension', 'time_to_peak_tension', 'time_to_half_resp'])
    df.to_csv(args.output, index=False)

    
