#####################################################################
# Hwa-seung Erstling
# CAS CS 320, Fall 2015
# Midterm
# validate.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #5. ***************
#  ****************************************************************
#

exec(open('analyze.py').read())
exec(open('interpret.py').read())
exec(open('compile.py').read())

def convertValue(v):
    if type(v) == Leaf:
        if v == 'True':
            return 1
        if v == 'False':
            return 0
    if type(v) == Node:
        for label in v:
            if label == 'Number':
                children = v[label]
                return children[0]

# Converts an output (a list of values) from the
# value representation to the machine representation
def convert(o):
    return [convertValue(v) for v in o]

def expressions(n):
    if n <= 0:
        return []
    elif n == 1:
        return ['True', 'False', {'Number':[1]}] # Add all base case(s) for Problem #5.
    else:
        fs = expressions(n-1)
        fsN = []
        fsN += [ {'Element':[{'Variable':['a']},f]} for f in fs]
        return fs + fsN

def programs(n):
    if n <= 0:
        return []
    elif n == 1:
        return ['End'] # Add base case(s) for Problem #5.
    else:
        ps = programs(n-1)
        es = expressions(n-1)
        psN = []
        psN += [ {'Assign':[{'Variable':['a']}, e1, e2, e3, p1]} for e1 in es for e2 in es for e3 in es for p1 in ps \
                 if typeProgram({},{'Assign':[{'Variable':['a']}, e1, e2, e3, p1]}) == 'TyVoid']
        psN += [ {'Print':[e1, p1]} for e1 in es for p1 in ps \
                 if typeProgram({},{'Print':[e1, p1]}) == 'TyVoid']
        psN += [ {'Loop':[{'Variable':['x']},{'Number':[1]}, p1, p2]} for p1 in ps for p2 in ps \
                 if typeProgram({},{'Loop':[{'Variable':['x']},{'Number':[1]}, p1, p2]}) == 'TyVoid']
        return ps + psN
   
# Compute the formula that defines correct behavior for the
# compiler for all program parse trees of depth at most k.
# Any outputs indicate that the behavior of the compiled
# program does not match the behavior of the interpreted
# program.

def exhaustive(k):
    for p in programs(k):
        try:
            if simulate(compileProgram({}, p)[1]) != convert(execProgram({}, p)[1]):
                print('\nIncorrect behavior on: ' + str(p))
        except:

            print('\nError on: ' + str(p))

#eof
