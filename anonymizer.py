#!/usr/bin/env python
#coding=utf-8
from PAA import PAA
from utils.read_data import read_data, read_tree
from utils.save_result import save_to_file
from utils.make_tree import gen_gh_trees
import sys, copy
import pdb



# set k=10, l=5 as default!

def get_result_one(att_trees, data, K=10, L=5):
    "fix K=10, L=5"
    data_back = copy.deepcopy(data)
    result = PAA(att_trees[-1], data, K, L)
    data = copy.deepcopy(data_back)
    save_to_file((att_trees, data, result, K, L))


def get_result_K(att_trees, data, L=5):
    "change K, while fixing L"
    data_back = copy.deepcopy(data)
    for K in range(5, 55, 5):
        result = PAA(att_trees[-1], data, K, L)
        data = copy.deepcopy(data_back)
        save_to_file((att_trees, data, result, K, L))


def get_result_L(att_trees, data, K=10):
    "change L, while fixing K"
    data_back = copy.deepcopy(data)
    for L in range(5, 55, 5):
        result = PAA(att_trees[-1], data, K, L)
        data = copy.deepcopy(data_back)
        save_to_file((att_trees, data, result, K, L))


def get_result_dataset(att_trees, data, K=10, L=5):
    "fix k and l, while changign dataset size"
    data_back = copy.deepcopy(data)
    length = len(data_back)
    joint = 5000
    h = length / joint
    if length % joint == 0:
        h += 1
    for i in range(1, h+1):
        pos = i * joint
        if pos > length:
            continue
        result = PAA(att_trees[-1], data[0:pos], K, L)
        data = copy.deepcopy(data_back)
        save_to_file((att_trees, data[0:pos], result, K, L))


if __name__ == '__main__':
    flag = ''
    len_argv = len(sys.argv)
    K = 10
    L = 5
    try:
        flag = sys.argv[1]
        K = int(sys.argv[2])
        L = int(sys.argv[3])
    except:
        pass
    print '*'*30
    # make generalization hierarchies
    gen_gh_trees()
    #read gentree tax
    att_trees = read_tree()
    #read record
    data = read_data()
    # PAA need only GH for transaction
    if flag == 'k':
        get_result_K(att_trees, data)
    elif flag == 'l':
        get_result_L(att_trees, data)
    elif flag == 'data':
        get_result_dataset(att_trees, data)
    elif flag == 'paa':
        if len_argv > 2:
            get_result_one(att_trees, data, K, L)
        else:
            get_result_one(att_trees, data)
    elif flag =='':
        get_result_one(att_trees, data)
    else:
        print "Usage: python anonymizer [k | l | data | paa]"
    print "Finish PAA!!"
    print '*'*30
    
