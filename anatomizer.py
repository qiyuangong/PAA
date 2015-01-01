import random, heapq
import pdb


_DEBUG = True


class SABucket(object):

    def __init__(self, data, index):
        self.member = data[:]
        self.index = index

    def pop_element(self):
        """pop an element from SABucket
        """
        return self.member.pop()


class Group(object):

    def __init__(self):
        self.index = 0
        self.member = []
        self.checklist = set()

    def add_element(self, record, index):
        """add element pair (record, index) to Group
        """
        self.member.append(record[:])
        self.checklist.add(index)

    def check_index(self, index):
        """Check if index is in checklist
        """
        if index in self.checklist:
            return True
        return False


def anatomizer(gdata, L):
    """
    L is the denote l in l-diversity
    gdata is a 2-dimensional list, i.e. [[],[]]
    Separation grouped member into QIT and SAT
    Use heap to get l largest buckets
    """
    groups = []
    result = []
    suppress = []
    h = []
    if _DEBUG:
        print '*' * 10
        print "Begin Anatomy!"
    print "L=%d" % L
    for i, temp in enumerate(gdata):
        # push to heap reversely
        pos = len(temp) * -1
        if pos == 0:
            continue
        heapq.heappush(h, (pos, SABucket(temp, i)))
    # group step
    while len(h) >= L:
        newgroup = Group()
        length_list = []
        SAB_list = []
        for i in range(L):
            (length, temp) = heapq.heappop(h)
            length_list.append(length)
            SAB_list.append(temp)
        for i in range(L):
            temp = SAB_list[i]
            length = length_list[i]
            newgroup.add_element(temp.pop_element(), temp.index)
            length += 1
            if length == 0:
                continue
            # push new tuple to heap
            heapq.heappush(h, (length, temp))
        groups.append(newgroup)
    # residue-assign step
    while len(h):
        (length, temp) = heapq.heappop(h)
        index = temp.index
        while temp.member:
            for g in groups:
                if g.check_index(index) == False:
                    g.add_element(temp.pop_element(), index)
                    break
            else:
                suppress.extend(temp.member[:])
                break
    # transform result
    for i, t in enumerate(groups):
        t.index = i
        result.append(t.member[:])

    if _DEBUG:
        print 'NO. of Suppress after anatomy = %d' % len(suppress)
        print 'NO. of groups = %d' % len(result)
    return result







