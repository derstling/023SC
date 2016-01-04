#####################################################################
# Hwa-seung Erstling
# CAS CS 320, Fall 2015
# Midterm
# interpret.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #2. ***************
#  ****************************************************************
#

exec(open('parse.py').read())
exec(open('analyze.py').read())

Node = dict
Leaf = str

def evalExpression(env, e):
    if type(e) == Leaf:
        if e == 'True':
            return 'True'
        if e == 'False':
            return 'False'
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                x = {'Number': [children[0]]}
                return x
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return {'Number':[env[x]]}
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'Plus':
                f1 = children[0]
                v1 = evalExpression(env, f1)
                f2 = children[1]
                v2 = evalExpression(env, f2)
                return {'Number': [v1['Number'][0] + v2['Number'][0]]}
            elif label == 'Element':
                x = children[0]['Variable'][0]
                e = children[1]
                k = evalExpression(env, e)['Number'][0]
##                if not (k >= 0 and k <= 2) :
##                    print(k + " is invalid array index.")
##                    exit()
                return env[x][k]
    

def execProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return (env, [])
    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                [e,p] = s[label]
                v = evalExpression(env, e)
                (env, o) = execProgram(env, p)
                return (env, [v] + o)
            elif label == 'Assign':
                children = s[label]
                x = children[0]['Variable'][0]
                (e0, e1, e2) = (children[1], children[2], children[3])
                p = children[4]

                env1 = env
                n0 = evalExpression(env1, e0)
                n1 = evalExpression(env1, e1)
                n2 = evalExpression(env1, e2)
                env1[x] = [n0,n1,n2]

                (env2, o) = execProgram(env1, p)
                return (env2, o)
            elif label == 'Loop':
                children = s[label]
                x  = children[0]['Variable'][0]
                n  = children[1]['Number'][0]
                p1 = children[2]
                p2 = children[3]
                env1 = env

                if n >= 0:
                    n1 = n-1
                    env1[x] = n
                    (env2, o1) = execProgram(env1, p1)
                    (env3, o2) = execProgram(env2, {'Loop':[{'Variable':[x]}, {'Number':[n1]}, p1, p2]})
                    return (env3, o1 + o2)
                elif n < 0:
                    (env2, o1) = execProgram(env1, p2)
                    return (env2, o1)

                
def interpret(s):
    temp = tokenizeAndParse(s)
    if temp is None:
        return None
    # Only interpret programs that are well-typed
    if typeProgram({},temp) == 'TyVoid':
        (env, o) = execProgram({}, temp)
        return o
#eof
