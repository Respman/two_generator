#! /usr/bin/env python3.6

import sys
import os.path
import json
import random

def normalazer(element):
    prime_numbers = [2,3,5,7,11,13,17,19,23,
                    29,31,37,41,43,47,53,59,61,
                    67,71,73,79,83,89,97]
    normal_feature = []
    summ = 0
    for i in range(len(prime_numbers)):
        normal_feature.append(0)
        while ((element % prime_numbers[i]) == 0):
            element = element/prime_numbers[i]
            normal_feature[i] += 1
            summ += 1
    if (summ != 0):
        for i in range(len(normal_feature)):
               normal_feature[i] /= summ
    return normal_feature


filename = os.path.join(sys.path[0], 'generator_config.json')
config = json.loads(open(filename).read())
a1 = config['koeff_a1']
b1 = config['koeff_b1']
c1 = config['koeff_c2']
a2 = config['koeff_a2']
b2 = config['koeff_b2']
c2 = config['koeff_c2']
x1 = config['start_with_1']
x2 = config['start_with_2']
n = config['amount_of_exemplares']
directory = config["directory's_name_for_teaching_set"]
string1 = [x1]
string2 = [x1]
z1 = x1
z2 = x2
for i in range(n*2):
    z1 = (a1*z1+b1) % c1
    string1.append(z1)
    z2 = (a2*z2+b2) % c2
    string2.append(z2)

random.shuffle(string1)
random.shuffle(string2)
teaching_set_1 = []
teaching_set_2 = []
testing_set_1 = []
testing_set_2 = []
len1 = len(string1)
len2 = len(string2)
for element in range(int(len1/2)):
    teaching_set_1.append(string1[element])
for element in range(int(len1/2),len1):
    testing_set_1.append(string1[element])
for element in range(int(len2/2)):
    teaching_set_2.append(string2[element])
for element in range(int(len2/2),len2):
    testing_set_2.append(string2[element])



teaching_set_1_1 = []
teaching_set_2_1 = []
for i in range(len(teaching_set_1)):
    teaching_set_1_1.append(teaching_set_1[i])
    teaching_set_1[i] = normalazer(teaching_set_1[i])
    teaching_set_1[i].append(teaching_set_1_1[i])
    teaching_set_1[i].append(1)
for i in range(len(teaching_set_2)):
    teaching_set_2_1.append(teaching_set_2[i])
    teaching_set_2[i] = normalazer(teaching_set_2[i])
    teaching_set_2[i].append(teaching_set_2_1[i])
    teaching_set_2[i].append(2)
teaching_set = teaching_set_1 + teaching_set_2
random.shuffle(teaching_set)

testing_set_1_1 = []
testing_set_2_1 = []
for i in range(len(testing_set_1)):
    testing_set_1_1.append(testing_set_1[i])
    testing_set_1[i] = normalazer(testing_set_1[i])
    testing_set_1[i].append(testing_set_1_1[i])
    testing_set_1[i].append(1)
for i in range(len(testing_set_2)):
    testing_set_2_1.append(testing_set_2[i])
    testing_set_2[i] = normalazer(testing_set_2[i])
    testing_set_2[i].append(testing_set_2_1[i])
    testing_set_2[i].append(2)
testing_set = testing_set_1 + testing_set_2
random.shuffle(testing_set)


fileway = os.path.join(sys.path[0],directory+"_examples")
if os.path.exists(fileway):
    for filename in os.listdir(fileway):
        os.remove(os.path.join(fileway,filename))
    os.rmdir(fileway)
os.mkdir(fileway)

filename = os.path.join(fileway,'example_config.json')
file = open(filename, 'w')
len1 = len(teaching_set)
file.write("{\n")
file.write(f'"amount_of_examples" : {len1}\n')
file.write("}")
file.close

for i in range(len(teaching_set)):
    len1 = len(teaching_set[i])-1
    filename = os.path.join(fileway,'example'+str(i)+'.json')
    file = open(filename, 'w')
    file.write("{\n")
    generator_number = int(teaching_set[i][len1])
    current_number = int(teaching_set[i][len1-1])
    file.write(f'"generator" : {generator_number},\n')
    file.write(f'"current_number" : {current_number},\n')
    string1 = "["+str(teaching_set[i][0])
    for j in teaching_set[i][1:len1-1]:
        string1 +=","+str(j)
    string1 +="]\n"
    file.write(f'"input" :  {string1}')
    file.write("}")
    file.close

fileway = os.path.join(sys.path[0],directory+"_testing_set")
if os.path.exists(fileway):
    for filename in os.listdir(fileway):
        os.remove(os.path.join(fileway,filename))
    os.rmdir(fileway)
os.mkdir(fileway)

filename = os.path.join(fileway,'test_config.json')
file = open(filename, 'w')
len1 = len(testing_set)
file.write("{\n")
file.write(f'"amount_of_examples" : {len1}\n')
file.write("}")
file.close


for i in range(len(testing_set)):
    len1 = len(testing_set[i])-1
    filename = os.path.join(fileway,'test'+str(i)+'.json')
    file = open(filename, 'w')
    file.write("{\n")
    generator_number = int(testing_set[i][len1])
    current_number = int(testing_set[i][len1-1])
    file.write(f'"generator" : {generator_number},\n')
    file.write(f'"current_number" : {current_number},\n')
    string1 = "["+str(testing_set[i][0])
    for j in testing_set[i][1:len1-1]:
        string1 +=","+str(j)
    string1 +="]\n"
    file.write(f'"input" :  {string1}')
    file.write("}")
    file.close


