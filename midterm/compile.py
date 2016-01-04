#####################################################################
# Hwa-seung Erstling
# CAS CS 320, Fall 2015
# Midterm 
# compile.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #4. ***************
#  ****************************************************************
#

from random import randint
exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('optimize.py').read())
exec(open('machine.py').read())

Leaf = str
Node = dict

def freshStr():
    return str(randint(0,10000000))

def compileExpression(env, e, heap):
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                f = children[0]
                insts = ['set '+str(heap)+' '+str(f)]
                heap += 1
                return (insts, heap-1, heap)
            if label == 'Variable':
                f = children[0]
                varAddr = env[f]
                insts = []
                return (insts, varAddr, heap)
            if label == 'Plus':
                e1 = children[0]
                e2 = children[1]
                (insts1, addr1, heap1) = compileExpression(env, e1, heap)
                (insts2, addr2, heap2) = compileExpression(env, e2, heap1)
                instsPlus = copy(addr1, 1) +\
                            copy(addr2, 2) +\
                            ['add'] +\
                            copy(0, heap2)
                heap3 = heap2 + 1
                return (insts1 + insts2 + instsPlus, heap2, heap3)
            if label == 'Element':
                x = children[0]['Variable'][0]
                e = children[1]
                (insts1, addr1, heap) = compileExpression(env, e, heap)

                if x not in env:
                    print("error")
                    exit()

                startAddr = env[x]

                # Add value stored in e to starting address of array
                # ...to read e-th index and store at top of heap
                instsElement = ['set 1 ' + str(startAddr)]+\
                               copy(addr1, 2) +\
                               ['add'] +\
                               copy(0,3) +\
                               ['set 4 ' + str(heap),\
                                'copy']
                heap2 = heap + 1
                return (insts1 + instsElement, heap, heap2)

    if type(e) == Leaf:
        if e == 'True':
            # Generate instruction to store the integer representing True on the heap.
            inst = 'set ' + str(heap) + ' 1'
            heap2 = heap + 1
            # Return the instruction list and top of the heap.
            return ([inst], heap, heap2)
        if e == 'False':
            # Generate instruction to store the integer representing False on the heap.
            inst = 'set ' + str(heap) + ' 0'
            heap2 = heap + 1
            # Return the instruction list and top of the heap.
            return ([inst], heap, heap2)

def compileProgram(env, s, heap = 8): # Set initial heap default address.
    if type(s) == Leaf:
        if s == 'End':
            return (env, [], heap)

    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                [e, p] = children
                (instsE, addr, heap) = compileExpression(env, e, heap)
                (env, instsP, heap) = compileProgram(env, p, heap)
                return (env, instsE + copy(addr, 5) + instsP, heap)
            if label == 'Assign':
                var = children[0]['Variable'][0]
                e1  = children[1]
                e2  = children[2]
                e3  = children[3]
                prg = children[4]

                # Compile the expressions
                #   -store in 3 contiguous memory spots starting with heap
                (insts1, addr1, heap) = compileExpression(env, e1, heap)
                (insts2, addr2, heap) = compileExpression(env, e2, heap)
                (insts3, addr3, heap) = compileExpression(env, e3, heap)

                # Check that variable is in environment
                # ...if not, create an entry in list
                # ...and assign it 1st of 3 array entries
                if var not in env:
                    env[var] = addr1
                    instsAssign = []
                else:
                    instsAssign = copy(addr1, env[var])
                
                j = compileProgram(env, prg, heap)
                if j is None:
                    print("Program Compilation error...")
                (env2, instsProg, heap) = j
                
                return (env2, insts1 + insts2 + insts3 + instsAssign + instsProg, heap)
            if label == 'Loop':
                x  = children[0]['Variable'][0]
                n  = children[1]['Number'][0]
                p1 = children[2]
                p2 = children[3]

                env[x] = heap
                envF = env.copy()
                heap = heap + 1

                # Compile nested program first
                j = compileProgram(envF, p1, heap)
                if j is None:
                    print("Program Compilation error...")
                (env1, instsNestedProg, heap) = j

                fresh = freshStr()
                instsLoop = ['set ' + str(env[x]) + ' ' + str(n),\
                        "label startLoop"+fresh ] +\
                        copy(env[x],-1) +\
                        increment(-1) +\
                        ["branch bodyLoop"+fresh + " -1",\
                         "goto finishLoop"+fresh,\
                         "label bodyLoop"+fresh \
                        ] +\
                        instsNestedProg +\
                        decrement(env[x]) +\
                        [\
                        "goto startLoop"+fresh,\
                        "label finishLoop" +fresh\
                        ]
                
                # Compile remaining program
                k = compileProgram(env, p2, heap)
                if k is None:
                    print("Program Compilation error...")
                (env, instsExitProg, heap) = k                
                
                return (env, instsLoop + instsExitProg, heap)

def compile(s):
    p = tokenizeAndParse(s)
    # Add calls to type checking and optimization algorithms
    
    # First perform typechecking - no point to reduce parse tree in following
    #   opt. algs. if program will not compile according to type system
    if typeProgram({}, p) != 'TyVoid':
        return None
    # Next, eliminate dead code that won't be used
    p = eliminateDeadCode(p)
    # Finally, make useable code more concise
    p = foldConstants(p)

    (env, insts, heap) = compileProgram({}, p)
    return insts

def compileAndSimulate(s):
    return simulate(compile(s))


# Helper functions from HW3------------------------------------------------------
def increment(addr):
  return [\
        'set 1 1',\
        'set 3 ' + str(addr),\
        'set 4 2',\
        'copy',\
        'add',\
        'set 3 0',\
        'set 4 ' + str(addr),\
        'copy',\
        'set 0 0',\
        'set 1 0',\
        'set 2 0',\
        'set 3 0',\
        'set 4 0'\
        ]

def decrement(addr):
  return [\
        'set 1 -1',\
        ]\
        + copy(addr,2)\
        + [\
        'add'
        ]\
        + copy(0,addr)\
        + [\
        'set 0 0',\
        'set 1 0',\
        'set 2 0',\
        'set 3 0',\
        'set 4 0'\
        ]

#eof
