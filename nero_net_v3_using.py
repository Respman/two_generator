#!/usr/bin/env python3
import sys
from sys import argv
import math
import random
import json
import os

# //////////////////////////////////////////////////////////////////////


def nero_using(nero_list_of_weights, input_answers,true):
    nero_list_of_weights = open(nero_list_of_weights)
    amount_of_hide_layers = int(nero_list_of_weights.readline())
    amount_of_neurons_in_layer = []
    amount_of_neurons_in_layer.append(int(nero_list_of_weights.readline()))
    for i in range(amount_of_hide_layers):
        amount_of_neurons_in_layer.append(int(nero_list_of_weights.readline()))
    amount_of_neurons_in_layer.append(int(nero_list_of_weights.readline()))
    input_parametrs = input_answers

# /////////////////////////////////////////////////////////

    ordinal_weight = 0
    layer_outputs = []

    layer_outputs.append(input_parametrs)
    # apply input_parametrs

    for i in range(1, len(amount_of_neurons_in_layer)):
        current_layer_outputs = []
        for k in range(amount_of_neurons_in_layer[i]):
            summ = 1*(float(nero_list_of_weights.readline()))
            for j in range(1, amount_of_neurons_in_layer[i-1]+1):
                ordinal_weight = (float(nero_list_of_weights.readline()))
                summ += (float(layer_outputs[i-1][j-1]))*ordinal_weight
            current_layer_outputs.append(1/(1+math.exp(-2*summ)))
            layer_outputs.append(current_layer_outputs)

    number_of_maximum_output = 0
    for i in range(amount_of_neurons_in_layer[
        len(amount_of_neurons_in_layer)-1
    ]):
        if layer_outputs[len(layer_outputs)-1][i] > layer_outputs[
            len(layer_outputs)-1
        ][number_of_maximum_output]:
            number_of_maximum_output = i

# /////////////////////////////////////////////////////////////

    nero_list_of_weights.close()
    if (number_of_maximum_output != (true-1)):
        return (0)
    else:
        return(1)


# __main__/////////////////////////////////

using = json.loads(open('nero_net_using_config.json').read())
directory = using['directory_with_examples']
nero_list_of_weights = using['nero_list_of_weights']

summ = 0
all_summ = 0
filename = os.path.join(sys.path[0],directory,'test_config.json')
file_config = json.loads(open(filename).read())
amnt_of_testing_set = file_config['amount_of_examples']
for cur_example in range(amnt_of_testing_set):
    filename = os.path.join(sys.path[0],directory,
                            "test" + str(cur_example)+".json")
    testing_set = json.loads(open(filename).read())
    input_answers = []
    for x in testing_set['input']:
        input_answers.append(x)
    true = testing_set['generator']
    summ += nero_using(nero_list_of_weights, input_answers,true)
    all_summ += 1
print(f"{summ} in {all_summ}")
# ////////////////////////////////////////
