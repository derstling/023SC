#####################################################################
# Hwa-seung Erstling
# CAS CS 320, Fall 2015
# Midterm
# analyze.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #3. ***************
#  ****************************************************************
#

exec(open('parse.py').read())

Node = dict
Leaf = str

def typeExpression(env, e):
    if type(e) == Leaf:
        if e == 'True' or e == 'False':
            return 'TyBoolean'
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                return 'TyNumber'

            elif label == 'Variable':
                x = children[0]
                if x in env:
                    if env[x] == 'TyNumber':
                        return 'TyNumber'
                
            elif label == 'Element':
                 [x, eArg] = children
                 x = x['Variable'][0] # Unpack.
                 tyArg = typeExpression(env, eArg)
                 if x in env:
                     tyFunArg = env[x]
                     if tyFunArg == 'TyArray' and tyArg == 'TyNumber':
                         return 'TyNumber'
            
            elif label == 'Plus':
                [e1,e2] = e[label]
                t1 = typeExpression(env, e1)
                t2 = typeExpression(env, e2)
                if t1 != 'TyNumber' or t2 != 'TyNumber':
                    print("+ requires integer arguments")
                    return None
                return 'TyNumber'
            
def typeProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return 'TyVoid'
    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                [e, p] = s[label]
                tExp  = typeExpression(env, e)
                tProg = typeProgram(env, p)

                if tExp is not None and tProg == 'TyVoid':
                    return 'TyVoid'
                
            if label == 'Assign':
                [xTree, e0, e1, e2, p] = s[label]
                x = xTree['Variable'][0]

                te0 = typeExpression(env, e0)
                te1 = typeExpression(env, e1)
                te2 = typeExpression(env, e2)

                if te0 != 'TyNumber' or te1 != 'TyNumber' or te2 !='TyNumber':
                    return None

                env[x] = 'TyArray'

                tProg = typeProgram(env, p)

                if tProg == 'TyVoid':
                    return 'TyVoid'

            if label == 'Loop':
                [xTree, nTree, p1, p2] = s[label]
                x = xTree['Variable'][0]

                tN = typeExpression(env, nTree)
                if tN != 'TyNumber':
                    return None

                env[x] = 'TyNumber'

                tP1 = typeProgram(env, p1)
                tP2 = typeProgram(env, p2)

                if tP1 == 'TyVoid' and tP2 == 'TyVoid':
                    return 'TyVoid'

# For testing
def typeCheckP(s):
    temp = tokenizeAndParse(s)
    #print(temp)
    return typeProgram({}, temp)

def typeCheckE(s):
    temp = tokenizeAndParse(s)
    #print(temp)
    return typeExpression({}, temp)


#eof
