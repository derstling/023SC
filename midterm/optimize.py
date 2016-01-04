#####################################################################
#
# CAS CS 320, Fall 2015
# Midterm (skeleton code)
# optimize.py
#
#  ****************************************************************
#  ************* You do not need to modify this file. *************
#  ****************************************************************
#

Node = dict
Leaf = str

def foldConstants(a):
    if type(a) == Leaf:
        return a
    if type(a) == Node:
        for label in a:
            children = a[label]
            if label == 'Element':
                [x, e] = children
                return {'Element':[x, foldConstants(e)]}
            elif label == 'Plus':
                [e1, e2] = children
                e1 = foldConstants(e1)
                e2 = foldConstants(e2)
                if 'Number' in e1 and 'Number' in e2:
                    return {'Number':[e1['Number'][0] + e2['Number'][0]]}
                return a
            elif label == 'Print':
                [e, p] = children
                return {'Print':[foldConstants(e), foldConstants(p)]}
            elif label == 'Assign':
                [x, e0, e1, e2, p] = children
                return {'Assign':[x, foldConstants(e0), foldConstants(e1), foldConstants(e2), foldConstants(p)]}
            elif label == 'Loop':
                [x, n, p1, p2] = children
                return {'Loop':[x, n, foldConstants(p1), foldConstants(p2)]}
            else:
                return a

def eliminateDeadCode(s):
    if type(s) == Leaf:
        return s
    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                [e, p] = children
                return {'Print':[e, eliminateDeadCode(p)]}
            elif label == 'Assign':
                [x, e0, e1, e2, p] = children
                return {'Assign':[x, e0, e1, e2, eliminateDeadCode(p)]}
            elif label == 'Loop':
                [xTree, nTree, p1, p2] = children
                if nTree['Number'][0] < 0:
                    return eliminateDeadCode(p2)
                else:
                    return {'Loop':[xTree, nTree, eliminateDeadCode(p1), eliminateDeadCode(p2)]}            

#eof