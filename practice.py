from time import time, sleep
from print_functions_for_lab_checks import *
from get_input_args import get_input_args
from get_pet_labels import get_pet_labels
from classify_images import classify_images
from adjust_results4_isadog import adjust_results4_isadog
from calculates_results_stats import calculates_results_stats
from print_results import print_results
import argparse
from os import listdir
from classifier import classifier
import os
from pathlib import Path
import pathlib

## Exo_ 1

start_time = time()

end_time = time()
tot_time = start_time - end_time

parser = argparse.ArgumentParser()
    
# Create 3 command line arguments as mentioned above using add_argument() from ArguementParser method
parser.add_argument('--dir', type = str, help = 'path to the folder of pet images')
parser.add_argument('--classifier', type = str, default = 'vgg', help = 'Type of classifier')
parser.add_argument('--file', type = str, default = 'dognames.txt', help = 'dognames file')

in_args = parser.parse_args(os.sys.argv[1:])

arguments = []
arguments.append(in_args.dir)
arguments.append(in_args.classifier)
arguments.append(in_args.file)


## Exo_2

name_list = listdir(in_args.dir)
result_dic = {}

name_pet = ""

for el in name_list:
	name = el.split("_")
	for i in name:
		if i.isalpha():
			name_pet += i + ' '
	name_pet += ','


new_name_pet = name_pet.split(',')

for id in range(0, len(name_list), 1):
    if name_list[id] not in result_dic:
         result_dic[name_list[id]] = [new_name_pet[id].lower().strip()]
    else:
         print("** Warning: Key=", name_list[id], 
               "already exists in results_dic with value =", 
               result_dic[name_list[id]])

### Exo_3

print(result_dic)

in_file = listdir()

for key in result_dic:
	# images_dir = os.path.join('pet_images/', key)
	images_dir = os.path.join('pet_images/', key)
	model_name = classifier(images_dir, 'vgg')

	model_name = model_name.lower().split(',')
	model_name = [x.strip(' ') for x in model_name]

	truth = result_dic[key][0]
	if truth in model_name:
		result_dic[key].extend((truth, 1))
	else:
		result_dic[key].extend((truth, 0))

# print(result_dic)

### Exo_4


dognames_dic = {}

with open('dognames.txt', 'r') as infile:
	line = infile.readline()

	while line != '':
		clean_line = line.rstrip()
		if clean_line not in dognames_dic:
			dognames_dic[clean_line] = 1
		else:
			print("** Warning: Key already exists in dognames_dic with value = ", clean_line)
		line = infile.readline()
# print(dognames_dic)

for key in result_dic:
	if result_dic[key][0] in dognames_dic:
		if result_dic[key][1] in dognames_dic:
			result_dic[key].extend((1, 1))
		else:
			result_dic[key].extend((1, 0))
	else:
		if result_dic[key][1] in dognames_dic:
			result_dic[key].extend((0, 1))
		else:
			result_dic[key].extend((0, 0))

# print(result_dic)

### Exo_5

results_stats_dic = {}

results_stats_dic['n_dogs_img'] = 0 # 2
results_stats_dic['n_correct_dogs'] = 0 #1
results_stats_dic['n_correct_notdogs'] = 0 #3
results_stats_dic['n_correct_breed'] = 0 #5
results_stats_dic['n_match'] = 0

for key in result_dic:
	if result_dic[key][2] == 1:
		results_stats_dic['n_match'] += 1

	if result_dic[key][3] == 1 and result_dic[key][2] == 1:
		results_stats_dic['n_correct_breed'] += 1

	if result_dic[key][3] == 1:
		results_stats_dic['n_dogs_img'] += 1

		if result_dic[key][4] == 1:
			results_stats_dic['n_correct_dogs'] += 1

	else:
		if result_dic[key][4] == 0:
			results_stats_dic['n_correct_notdogs'] += 1

results_stats_dic['n_images'] = len(result_dic)

results_stats_dic['n_notdog_img'] = results_stats_dic['n_images'] - results_stats_dic['n_dogs_img']

results_stats_dic['pct_match'] = (results_stats_dic['n_match'] / results_stats_dic['n_images']) * 100.0

results_stats_dic['pct_correct_dogs'] = (results_stats_dic['n_correct_dogs'] / results_stats_dic['n_dogs_img']) * 100.0

results_stats_dic['pct_correct_breed'] = (results_stats_dic['n_correct_breed'] / results_stats_dic['n_dogs_img']) * 100.0

if results_stats_dic['n_notdog_img'] > 0:
	results_stats_dic['pct_correct_notdogs'] = (results_stats_dic['n_correct_notdogs'] / results_stats_dic['n_notdog_img'] * 100.0)
else:
	results_stats_dic['pct_correct_notdogs'] = 0.0

# print(results_stats_dic)


### Exo_6

print("\n\n*** Results Summary for CNN Model Architecture ***") #model.upper(), 
          # "***")
print("{:20}: {:3d}".format('N Images', results_stats_dic['n_images']))
print("{:20}: {:3d}".format('N Dog Images', results_stats_dic['n_dogs_img']))

print('{:20}: {:3d}'.format('N Not-Dog Images', results_stats_dic['n_notdog_img']))

print(' ')

print('\n****SUMMARY STATISTICS (Pourcentage) ON MODEL RUN ****')

for key in results_stats_dic:
	if key[0] == 'p':
		print('{}: {}'.format(key, results_stats_dic[key]))


if ((results_stats_dic['n_correct_dogs'] + results_stats_dic['n_correct_notdogs']) != results_stats_dic['n_images']):
	print('\nINCORRECT Dog/NOT Dog Assignments:')

	for key in results_dic:
		if ((result_dic[key][3] == 1 and result_dic[key][4] == 0) or
			(result_dic[key][3] == 0 and result_dic[key][4] == 1)):
			print('{:20}: {:20}'.format('Pet Label', results_dic[key][3]))
			print('{:20}: {:20}'.format('Classifier label', result_dic[key][4]))


if (results_stats_dic['n_correct_dogs'] != results_stats_dic['n_correct_breed']):
	print('\nINCORRECT Dog Breed Assignments: ')

	for key in result_dic:
		if (result_dic[key][2] == 0 and result_dic[key][3] == 1 and result_dic[key][4] == 1):
			print('Real: {:>26}		Classifier: {:>30}'.format(result_dic[key][0], result_dic[key][1]))


