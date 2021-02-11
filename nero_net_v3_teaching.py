#!/usr/bin/env python3
import sys
from sys import argv
import math
import random
import json
import time
import subprocess
import os

random.seed()

# "cor" in the variable name means "correction"
# "cur" in the variable name means  "current"
# "out" in the variable name means "output"
# "inp" in the variable name means "input"
# "amnt" in the variable name means "amount"
# "w" in the variable name means "weight"
# "ans" in the variable name means "answer"


def nero_studying(amnt_of, n, part_from_teaching_set,
                  w_inp, directory, m):

    amnt_of_iterations_for_one_exercise = 1
    list_of_w = []
    for i in range(1, len(amnt_of)):
        w = []
        for j in range((amnt_of[i-1]+1)*amnt_of[i]):
            w.append(random.uniform(-w_inp, w_inp))
        list_of_w.append(w)

    delta_list_of_w = []
    for i in list_of_w:
        delta_w = []
        for j in range(len(i)):
            delta_w.append(0)
        delta_list_of_w.append(delta_w)

    filename = os.path.join(sys.path[0], directory, 'example_config.json')
    file_config = json.loads(open(filename).read())
    amnt_of_teaching_set = file_config['amount_of_examples']
    amnt_of_successful_attempts = 0

    while (amnt_of_successful_attempts <
            amnt_of_iterations_for_one_exercise *
            part_from_teaching_set * amnt_of_teaching_set):

        cur_example = random.randint(0, amnt_of_teaching_set-1)
        filename = os.path.join(sys.path[0], directory,
                                "example"+str(cur_example)+".json")
        teaching_set = json.loads(open(filename).read())
        inp_parametrs = []
        layer_out = []
        for x in teaching_set['input']:
            inp_parametrs.append(x)
        layer_out.append(inp_parametrs)
        for i in range(amnt_of[len(amnt_of)-1]):
            if i == (teaching_set['generator']-1):
                inp_parametrs.append(1)
            else:
                inp_parametrs.append(0)

# everyone of neurons has ordinal number on his layer:
        ordinal_w = 0

# apply inp_parametrs
        for i in range(1, len(amnt_of)):
            cur_layer_out = []
            for k in range(amnt_of[i]):
                summ = 1*list_of_w[i-1][k*(amnt_of[i-1]+1)]
                for j in range(1, amnt_of[i-1]+1):
                    ordinal_w = list_of_w[i-1][k*(amnt_of[i-1]+1)+j]
                    summ += layer_out[i-1][j-1]*ordinal_w
                cur_layer_out.append(1/(1+math.exp(-2*summ)))
            layer_out.append(cur_layer_out)
        out_cor = []
        correct_ans = []

        for i in range(amnt_of[0], amnt_of[0]+amnt_of[len(amnt_of)-1]):
            correct_ans.append(float(inp_parametrs[i]))

        for i in range(amnt_of[len(amnt_of)-1]):
            cur_out = layer_out[len(layer_out)-1][i]
            out_cor.append(cur_out*(1-cur_out)*(correct_ans[i]-cur_out))

        layer_cor = []
        layer_cor.append(out_cor)

        for k in range(len(amnt_of)-2):
            # amnt of hide layer
            hide_cor = []
            for i in range(amnt_of[len(amnt_of)-k-2]):
                # amnt of neurons in current hide layer
                shildren_summ = 0
                for j in range(amnt_of[len(amnt_of)-k-1]):
                    # amnt of neurons in previous layer
                    paste1 = (len(list_of_w)-1)-k
                    paste2 = j*(amnt_of[len(amnt_of)-k-2]+1) + (i+1)
                    paste3 = list_of_w[paste1][paste2]
                    shildren_summ += layer_cor[k][j] * paste3
                paste1 = (len(layer_out)-1) - (k+1)
                paste2 = (1-layer_out[paste1][i]) * (shildren_summ)
                paste3 = layer_out[paste1][i] * paste2
                hide_cor.append(paste3)
            layer_cor.append(hide_cor)
            # making delta_nero_list_of_weight
        layer_cor.reverse()

        for k in range(1, len(amnt_of)):
            # number of layer
            for i in range(amnt_of[k]):
                paste1 = delta_list_of_w[k-1][i*(amnt_of[k-1]+1)]
                paste3 = layer_cor[k-1][i]
                paste1 = n * paste3 + m * paste1
                delta_list_of_w[k-1][i*(amnt_of[k-1]+1)] = paste1
                for j in range(1, amnt_of[k-1]+1):
                    paste1 = delta_list_of_w[k-1][i*(amnt_of[k-1]+1)+j]
                    paste3 = layer_cor[k-1][i]*layer_out[k-1][j-1]
                    paste1 = n * paste3 + m * paste1
                    delta_list_of_w[k-1][i*(amnt_of[k-1]+1)+j] = paste1
        for i in range(len(list_of_w)):
            for j in range(len(list_of_w[i])):
                list_of_w[i][j] += delta_list_of_w[i][j]

        print("\033c")
        # console cleaner
        # print(f"hide parametrs is: {hide_parametrs}")
        print(f"input parametrs is {inp_parametrs}")
        print(f"output parametrs is: {layer_out[len(layer_out)-1]}")
        print(f"correct outputs is: {correct_ans}")
        paste = f"{layer_cor[len(layer_cor)-1]}"
        write = "output correction is:" + paste
        print(write)
        # test for stopping studing:

        maximum_out = 0
        maximum_correct_out = 0
        for i in range(amnt_of[len(amnt_of)-1]):
            paste1 = len(layer_out)-1
            paste2 = layer_out[paste1][maximum_out]
            if layer_out[len(layer_out)-1][i] > paste2:
                maximum_out = i
            paste1 = correct_ans[maximum_correct_out]
            if correct_ans[i] > paste1:
                maximum_correct_out = i
        condition = math.fabs(maximum_correct_out - maximum_out)< 0.3
        if (maximum_correct_out == maximum_out) and condition:
            amnt_of_successful_attempts += 1
        else:
            amnt_of_successful_attempts = 0

        paste1 = f"{amnt_of_successful_attempts}"
        write = "amount of successful attempts: " + paste1
        print(write)

    paste1 = f"{math.floor(time.time())}_w{round(w_inp, 1)}.txt"
    name = "./new_list_of_weights_t" + paste1
    new_list_of_w = open(name, 'w')

    new_list_of_w.write(str(len(amnt_of)-2) + "\n")
    for i in amnt_of:
        new_list_of_w.write(str(i) + "\n")

    for i in range(len(list_of_w)):
        for j in list_of_w[i]:
            new_list_of_w.write(str(j) + "\n")
    new_list_of_w.close()

    print(f"nero_list_of_weights is: {list_of_w}")


# //////////////////////////////////////////////////////////////////////

def nero_using(list_of_w):
    list_of_w = open(list_of_w)

    amnt_of_hide_layers = int(list_of_w.readline())
    amnt_of_neurons_in_layer = []
    amnt_of_neurons_in_layer.append(int(list_of_w.readline()))
    for i in range(amnt_of_hide_layers):
        amnt_of_neurons_in_layer.append(int(list_of_w.readline()))
    amnt_of_neurons_in_layer.append(int(list_of_w.readline()))
    inp_parametrs = []

    for i in range(amnt_of_neurons_in_layer[0]):
        inp_parametrs.append(inp(f" input {i+1}-t input's parametrs: "))

    # /////////////////////////////////////////////////////////

    ordinal_w = 0
    layer_out = []

    layer_out.append(inp_parametrs)
    # apply input_parametrs

    for i in range(1, len(amnt_of_neurons_in_layer)):
        cur_layer_out = []
        for k in range(amnt_of_neurons_in_layer[i]):
            summ = 1*(float(nero_list_of_w.readline()))
            for j in range(amnt_of_neurons_in_layer[i-1]):
                ordinal_w = (float(list_of_w.readline()))
                summ += (float(layer_out[i-1][j]))*ordinal_w
            cur_layer_out.append(1/(1+math.exp(-2*summ)))
            layer_out.append(cur_layer_out)
    number_of_maximum_out = 0
    for i in range(amnt_of_neurons_in_layer[
        len(amnt_of_neurons_in_layer)-1
    ]):
        if layer_out[len(layer_out)-1][i] > layer_out[
            len(layer_out)-1
        ][number_of_maximum_out]:
            number_of_maximum_out = i
    # /////////////////////////////////////////////////////////////

    print(f"The number of maximum output is {number_of_maximum_out + 1}")
    list_of_w.close()
    return (layer_out[len(layer_out)-1])

#__main__//////////
studying = json.loads(open("nero_net_teaching_config.json").read())
amnt_of_inp_neurons = studying['amount of input neurons']
amnt_of_output_neurons = studying['amount of output neurons']
directory = studying["directory_with_examples"]
part_from_teaching_set = studying['part from teaching set']
w_inp = studying['weight_interval']
momentum = studying['momentum']
# part of teaching set sufficient to pass the exam
amnt_of = []
amnt_of.append(amnt_of_inp_neurons)
for x in studying['amount of hide neurons']:
    amnt_of.append(x)
amnt_of.append(amnt_of_output_neurons)
speed = studying['speed']
nero_studying(amnt_of, speed, part_from_teaching_set,
              w_inp, directory, momentum)

