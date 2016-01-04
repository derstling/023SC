# Hwa-seung Erstling
# CS 320, Fall 2015
# HW2
# interpret.py

# Starter code taken from Lapets' notes and then modified

import re

exec(open('parse.py').read())

Node = dict
Leaf = str

# Problem 2a
def evalTerm(env, t):
    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == 'Number':
                x = {'Number': [children[0]]}
                return x
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'Parens':
                f = children[0]
                v = evalTerm(env, f)
                return v
            elif label == 'If':
                f1 = children[0]
                v1 = evalFormula(env, f1)
                t2 = children[1]
                v2 = evalTerm(env, t2)
                t3 = children[2]
                v3 = evalTerm(env, t3)
                if v1 is 'True':
                    return v2
                elif v1 is 'False':
                    return v3
            elif label == 'Plus':
                f1 = children[0]
                v1 = evalTerm(env, f1)
                f2 = children[1]
                v2 = evalTerm(env, f2)
                return {'Number': [v1['Number'][0] + v2['Number'][0]]}
            elif label == 'Mult':
                f1 = children[0]
                v1 = evalTerm(env, f1)
                f2 = children[1]
                v2 = evalTerm(env, f2)
                return {'Number': [v1['Number'][0] * v2['Number'][0]]}            


# From Lapets' notes
def vnot(v):
    if v == 'True':  return 'False'
    if v == 'False': return 'True'

def vand(v1, v2):
    if v1 == 'True'  and v2 == 'True':  return 'True'
    if v1 == 'True'  and v2 == 'False': return 'False'
    if v1 == 'False' and v2 == 'True':  return 'False'
    if v1 == 'False' and v2 == 'False': return 'False'


# Problem 2b
def evalFormula(env, f):
    if type(f) == Node:
        for label in f:
            children = f[label]
            if label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'Nonzero':
                t1 = children[0]
                v1 = evalTerm(env, t1)
                if v1['Number'][0] != 0:
                    return 'True'
                elif v1['Number'][0] == 0:
                    return 'False'
            if label == 'Not':
                f = children[0]
                v = evalFormula(env, f)
                return vnot(v)
            elif label == 'And':
                f1 = children[0]
                v1 = evalFormula(env, f1)
                f2 = children[1]
                v2 = evalFormula(env, f2)
                return vand(v1, v2)
            elif label == 'Equal':
                f1 = children[0]
                v1 = evalTerm(env, f1)
                f2 = children[1]
                v2 = evalTerm(env, f2)
                if v1['Number'][0] == v2['Number'][0]:
                    return 'True'
                elif v1['Number'][0] != v2['Number'][0]:
                    return 'False'            
            elif label == 'Less':
                f1 = children[0]
                v1 = evalTerm(env, f1)
                f2 = children[1]
                v2 = evalTerm(env, f2)
                if v1['Number'][0] < v2['Number'][0]:
                    return 'True'
                elif v1['Number'][0] >= v2['Number'][0]:
                    return 'False'
            elif label == 'Greater':
                f1 = children[0]
                v1 = evalTerm(env, f1)
                f2 = children[1]
                v2 = evalTerm(env, f2)
                if v1['Number'][0] > v2['Number'][0]:
                    return 'True'
                elif v1['Number'][0] <= v2['Number'][0]:
                    return 'False'             

    elif type(f) == Leaf:
        if f == 'True':
            return 'True'
        if f == 'False':
            return 'False'  


# Problem 2c
def execProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return (env, [])
    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                children = s[label]
                e = children[0]
                p = children[1]
                v = evalTerm(env, e)
                if v is None:
                    v = evalFormula(env, e)
##                    if v is None:
##                        print("ERROR: Expressions is neither term nor formula")
                (env, o) = execProgram(env, p)
                return (env, [v] + o)
            if label == 'Assign':
                children = s[label]
                x = children[0]['Variable'][0]
                f = children[1]
                p = children[2]
                v = evalTerm(env, f)
                if v is None:
                    v = evalFormula(env, f)
##                    if v is None:
##                        print("ERROR: Expressions is neither term nor formula")
                env[x] = v
                (env, o) = execProgram(env, p)
                return (env, o)
            if label == 'If':
                children = s[label]
                e = children[0]
                p1 = children[1]
                p2 = children[2]
                v = evalTerm(env, e)
                if v is None:
                    v = evalFormula(env, e)
##                    if v is None:
##                        print("ERROR: Expressions is neither term nor formula")

                if v is 'False':
                    (env2, o) = execProgram(env, p2)
                    return (env2, o)
                elif v is 'True':
                    (env1, o1) = execProgram(env, p1)
                    (env2, o2) = execProgram(env1, p2)
                    return (env2, o1 + o2)

            if label == 'DoUntil':
                [body, cond, rest] = s[label]
                env1 = env
                (env2, o1) = execProgram(env1, body)

                v = evalTerm(env2, cond)
                if v is None:
                    v = evalFormula(env2, cond)
                    if v is None:
                        print("ERROR: Expressions is neither term nor formula")

                if v == 'True':
                    (env3, o2) = execProgram(env2, rest)
                    return (env3, o1 + o2)
                if v == 'False':
                    (env3, o2) = execProgram(env2, {'DoUntil':[body, cond, rest]})
                    return (env3, o1 + o2)


# From HW1
def regexp(tokens):
    x = [re.escape(a) for a in tokens]
    return "|".join([str(c) for c in x])

def tokenize(terminals,s):
    tokens = [t for t in re.split(r"(\s+|"+regexp(terminals)+")" ,s)]
    return [t for t in tokens if not t.isspace() and not t == ""]


# Problem 2d
def interpret(s):
    t = tokenize(['print', ';', ':=','assign','if','{','}','do', \
                      'until', 'true', 'false', 'nonzero', '(', ')', \
                      'not', 'and', ',', '+', '*', '=', '<', '>'],s)
    
    pt = program(t)

    if not pt is None:
        (env, o) = execProgram({}, pt[0])
        return o
    else:
        return None


# Problem 3
# Implemented in this file and in parse.py
