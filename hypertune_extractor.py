
import os
import json

def read_json(path):
    # print(path)
    with open(path, 'r') as f:
        data = json.load(f)

    return data


def extract_relevant_data(q):

    results = {}

    ## CHANGE THIS TO USE!!!!!

    results['config'] = q['hyperparameters']['values']

    results['val_loss'] = q['metrics']['metrics']['val_loss']['observations'][0]['value'][0]
    results['val_accuracy'] = q['metrics']['metrics']['val_accuracy']['observations'][0]['value'][0]

    return results

## CHANGE THIS TO USE!!!!!
rel_path = "hyper/celeba_hyperband"


x = os.listdir(rel_path)

list_of_dir = []

for file in x:
    if not "." in file:
        list_of_dir.append(file)

results = []

for folder in list_of_dir:
    temp_path = os.path.join(rel_path,folder,"trial.json")
    json_obj = read_json(temp_path)
    json_out = extract_relevant_data(json_obj)
    results.append(json_out)



def convert_result_to_row(result,t):
    row1 = ['Trial']
    row2 = [t]
    # print(result['config'])

    for key,value in result['config'].items():
        if key =="tuner/initial_epoch":
            break
        row1.append(key)
        row2.append(value)

    row1.append("")
    row2.append("")
    # print(result['config'])
    row1.append('val_loss')
    row2.append(result['val_loss'])

    row1.append('val_accuracy')
    row2.append(result['val_accuracy'])

    return row1,row2




FLAG = True
import csv

# open the file in the write mode
f = open('results.csv', 'w',newline='')
# create the csv writer
writer = csv.writer(f)
towrite=[]
i=1
for r in results:
    # print(r)
    title, val = convert_result_to_row(r,i)
    i+=1
    # write a row to the csv file
    # print(val)
    if FLAG:
        writer.writerow(title)
        FLAG = False
    header = title
    towrite.append(val)
    # writer.writerow(val)
writer.writerows(towrite)


# close the file
f.close()

