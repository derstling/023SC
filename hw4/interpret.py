#####################################################################
#
# CAS CS 320, Fall 2015
# Assignment 4 (skeleton code)
# interpret.py
#

exec(open('parse.py').read())

Node = dict
Leaf = str

# reconstruct tree and replace 'Variable' nodes with their value
# in s, if any are available at all
def subst(s, a):
    for x in a:
        if x is 'Variable':
            if a[x][0] in s:
                return s[(a[x][0])]     # return result of substitution
            else:
                return a                # no subst...return original tree
        else:
            return {x: [subst(s, y) for y in a[x]]}

def unify(a, b):
    if type(a) is Leaf and type(b) is Leaf:
        if a == b:
            return {}
        else:
            return None
    for x in a:
        al = x
    if al is 'Variable':
        return { a[x][0] : b }
    for y in b:
        bl = y
    if bl is 'Variable':
        return { b[bl][0] : a }
    if al == bl and len(a[al]) == len(b[bl]):
        s = {}
        for i in range(0,len(a[al])):
            tmp = unify(a[al][i],b[bl][i])
            if tmp != {}:
                # Check that entry doesn't already exist in unification
                for j in s:
                    for k in tmp:
                        if j == k:
                            return None
                s.update(tmp)
        return s

    
def build(m, d):
    if type(d) == Leaf:
        if d == 'End':
            return m
    if type(d) == Node:
        for label in d:
            children = d[label]
            if label == 'Function':
                v = children[0]['Variable'][0]
                p = children[1]
                e = children[2]
                d2 = children[3]
                if v not in m:
                    m[v] = [(p,e)]
                else:
                    m[v] += [ (p,e) ]
                return build(m, d2)

def evaluate(m, env, e):
    # Expression-constructor-args
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'ConInd':
                c  = children[0]
                e1 = children[1]
                e2 = children[2]

                v1 = evaluate(m, env, e1)
                v2 = evaluate(m, env, e2)

                return { label: [c,v1,v2]}
            if label == 'ConBase':
                return e
            if label == 'Number':
                return e
            if label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
            if label == 'Mult':
                e1 = children[0]
                e2 = children[1]
                n1 = evaluate(m,env,e1)
                n2 = evaluate(m,env,e2)
                if 'Number' in n1 and 'Number' in n2:
                    return { 'Number': [ n1['Number'][0] * n2['Number'][0] ] }
            if label == 'Apply':
                f = children[0]['Variable'][0]
                e1 = children[1]

                v1 = evaluate(m,env,e1)

                if f in m:
                    # if there exists a pattern in m[f] (i.e. (p,e) )
                    #       where sub(p) unifies sub(v1)
                    for (p,e2) in m[f]:
                        temp = unify(p,v1)
                        if not temp is None:    # pattern found
                            env.update(temp)
                            v2 = evaluate(m,env,e2)
                            if not v2 is None:

                                return v2




def interact(s):
    # Build the module definition.
    m = build({}, parser(grammar, 'declaration')(s))

    # Interactive loop.
    while True:
        # Prompt the user for a query.
        s = input('> ') 
        if s == ':quit':
            break
        
        # Parse and evaluate the query.
        e = parser(grammar, 'expression')(s)
        if not e is None:
            print(evaluate(m, {}, e))
        else:
            print("Unknown input.")

#eof
