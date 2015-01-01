from partition_for_transaction import partition, list_to_str
from anatomizer import anatomizer
import time
import pdb


_DEBUG = True
gl_att_tree = []
gl_data = []


def get_range(att_tree, tran):
    """compute probability for generlized set
    For example, age value 10 is generlized to 10-20.
    So the probability is 1/10, which means that this 
    range is 10 with probability 1/10. 
    """
    # store the probability of each value
    prob = 1.0
    for t in tran:
        if att_tree[t].support:
            support = att_tree[t].support
            prob /= support
    return prob


def PAA(att_tree, data, K=10, L=5):
    """Using Partition to anonymize SA (transaction) partition, 
    while applying Anatomize to separate QID and SA
    """
    global gl_att_tree, gl_data
    gl_att_tree = att_tree
    gl_data = data
    start_time = time.time()
    tran_tree = {}
    print "size of dataset %d" % len(gl_data)
    result = []
    trans = [t[-1] for t in gl_data]
    trans_set = partition(att_tree, trans, K)
    grouped_data = []
    for ttemp in trans_set:
        (index_list, tran_value) = ttemp
        parent = list_to_str(tran_value, cmp)
        try:
            tran_tree[parent]
        except:
            tran_tree[parent] = set()
        gtemp = []
        for t in index_list:
            temp = gl_data[t][:]
            leaf = list_to_str(temp[-1], cmp)
            tran_tree[parent].add(leaf)
            temp[-1] = tran_value[:]
            gtemp.append(temp)
        grouped_data.append(gtemp)
    print "Begin Anatomy"
    grouped_result = anatomizer(grouped_data, L)
    print("--- %s seconds ---" % (time.time()-start_time))
    # transform data format (QID1,.., QIDn, SA set, GroupID, 1/|group size|, SA_list (dict) :original SA (str) sets with prob)
    # 1/|group size|, original SA sets with prob (dict) will be used in evaluation
    for index, group in enumerate(grouped_result):
        length = len(group)
        leaf_list = []
        SA_list = {}
        parent_list = {}
        for t in group:
            parent = list_to_str(t[-1], cmp)
            gen_range = get_range(att_tree, t[-1])
            leaf_list = leaf_list + list(tran_tree[parent])
            parent_list[parent] = gen_range
        # all transactions covered by this group
        leaf_list = list(set(leaf_list))
        # pdb.set_trace()
        for temp in leaf_list:
            for p in parent_list.keys():
                if temp in tran_tree[p]:
                    try:
                        SA_list[temp] += parent_list[p]/length 
                    except:
                        SA_list[temp] = parent_list[p]/length
        # pdb.set_trace()
        for t in group:
            temp = t[:]
            temp.append(index)
            temp.append(1.0/length)
            temp.append(SA_list)
            result.append(temp)
    return result