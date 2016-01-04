######################################################################
# Hwa-seung Erstling U36770098
# CAS CS 320, Fall 2015
# Assignment 3
# compile.py
#

exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('machine.py').read())

Node = dict
Leaf = str

# Used to create unique labels (ex: whileLoop1, whileLoop2...)
fresh = 0

# Problem 3a
def compileTerm(env, t, heap):
    if type(t) == Node:
        for label in t:
            children = t[label]
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
                # Compile the two subtrees and get the instructions
                # lists as well as the addresses in which the results
                # of computing the two subtrees would be stored if someone
                # were to run those machine instructions.
                f1 = children[0]
                f2 = children[1]
                (insts1, addr1, heap1) = compileTerm(env, f1, heap)
                (insts2, addr2, heap2) = compileTerm(env, f2, heap1)
                # Increment the heap counter so we store the
                # result of computing Or in a new location.
                heap3 = heap2 + 1
                # Add instructions that compute the result of the
                # Plus operation.
                instsPlus = \
                    copy(addr1, 1) + \
                    copy(addr2, 2) + \
                    ["add"] + \
                    copy(0,heap2)
                return (insts1 + insts2 + instsPlus, heap2, heap3)

# Problem 3b
def compileFormula(env, f, heap):

    global fresh

    if type(f) == Leaf:
        if f == 'True':
            # Generate instruction to store the integer representing True on the heap.
            inst = 'set ' + str(heap) + ' 1'
            heap2 = heap + 1
            # Return the instruction list and top of the heap.
            return ([inst], heap, heap2)
        if f == 'False':
            # Generate instruction to store the integer representing False on the heap.
            inst = 'set ' + str(heap) + ' 0'
            heap2 = heap + 1
            # Return the instruction list and top of the heap.
            return ([inst], heap, heap2)
    if type(f) == Node:
        for label in f:
            children = f[label]
            if label == 'Variable':
                f1 = children[0]
                varAddr = env[f1]
                insts = []
                return (insts, varAddr, heap)
            if label == 'Not':
                # Compile the subtree f to obtain the list of
                # instructions that computes the value represented
                # by f.
                f1 = children[0]
                (insts, addr, heap) = compileFormula(env, f1, heap)
                # Generate more instructions to change the memory
                # location in accordance with the definition of the
                # Not operation.
                fresh = fresh + 1
                instsNot = \
                   ["branch setZero" + str(fresh) + " " + str(addr),\
                    "set " + str(heap) + " 1",\
                    "goto finish" + str(fresh),\
                    "label setZero" + str(fresh),\
                    "set " + str(heap) + " 0",\
                    "label finish" + str(fresh)\
                   ]
                heap1 = heap + 1
                return (insts + instsNot, heap, heap1)
            if label == 'And':
                f1 = children[0]
                f2 = children[1]
                (insts1, addr1, heap2) = compileFormula(env, f1, heap)
                (insts2, addr2, heap3) = compileFormula(env, f2, heap2)

                fresh = fresh + 1
                instsAnd = \
                    copy(addr1, 1) + \
                    copy(addr2, 2) + \
                    ['add',\
                     'set 1 -2'] + \
                    copy(0, 2) + \
                    ['add',\
                    "branch setOne" + str(fresh) + " 0",\
                    "set " + str(heap3) + " 1",\
                    "goto finish" + str(fresh),\
                    "label setOne" + str(fresh),\
                    "set " + str(heap3) + " 0",\
                    "label finish" + str(fresh)\
                   ]
                heap4 = heap3 + 1
                return (insts1 + insts2 + instsAnd, heap3, heap4)
            if label == 'Xor':
                f1 = children[0]
                f2 = children[1]
                (insts1, addr1, heap2) = compileFormula(env, f1, heap)
                (insts2, addr2, heap3) = compileFormula(env, f2, heap2)

                fresh = fresh + 1
                instsXor = \
                    copy(addr1, 1) + \
                    copy(addr2, 2) + \
                    ['add',\
                     'set 1 -1'] + \
                    copy(0, 2) + \
                    ['add',\
                    "branch setOne" + str(fresh) + " 0",\
                    "set " + str(heap3) + " 1",\
                    "goto finish" + str(fresh),\
                    "label setOne" + str(fresh),\
                    "set " + str(heap3) + " 0",\
                    "label finish" + str(fresh)\
                   ]
                heap4 = heap3 + 1
                return (insts1 + insts2 + instsXor, heap3, heap4)



# Problem 3c
def compileProgram(env, s, heap):

    global fresh

    # Program::= [empty parse tree]
    if s == [] or s == 'End':
        return (env, [], heap)

    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                ex = children[0]
                pr = children[1]

                # Compile the expression
                r = compileTerm(env, ex, heap)
                if r is None:
                    r = compileFormula(env, ex, heap)
                (insts1, addr1, heap2) = r

                instsPrint = copy(addr1, 5)

                j = compileProgram(env, pr, heap2)
                if j is None:
                    print("Program Compilation error...")
                (env2, instsProg, heap3) = j
                
                return (env2, insts1 + instsPrint + instsProg, heap3)
            if label == 'Assign':
                var = children[0]['Variable'][0]
                exp = children[1]
                prg = children[2]

                # Compile the expression
                r = compileTerm(env, exp, heap)
                if r is None:
                    r = compileFormula(env, exp, heap)

                (insts1, addr1, heap2) = r

                # Check that variable is in environment
                # ...if not, create an entry in list
                # ...and assign it directly to heap address
                if var not in env:
                    env[var] = addr1
                    instsAssign = []
                else:
                    instsAssign = copy(addr1, env[var])
                
                j = compileProgram(env, prg, heap2)
                if j is None:
                    print("Program Compilation error...")
                (env2, instsProg, heap3) = j
                
                return (env2, insts1 + instsAssign + instsProg, heap3)
            if label == 'If':
                exp = children[0]
                pr1 = children[1]
                pr2 = children[2]

                # Compile the expression
                r = compileTerm(env, exp, heap)
                if r is None:
                    r = compileFormula(env, exp, heap)
                (insts1, addr1, heap2) = r

                # Compile nested program first
                j = compileProgram(env, pr1, heap2)
                if j is None:
                    print("Program Compilation error...")
                (env2, instsNestedProg, heap3) = j

                fresh = fresh + 1
                instsIf = [\
                    "branch setIf" + str(fresh) + " " + str(addr1),\
                    "goto finishIf" + str(fresh),\
                    "label setIf" + str(fresh)
                    ] + \
                    instsNestedProg + \
                    ["label finishIf" + str(fresh)]

                # Compile remaining program
                k = compileProgram(env2, pr2, heap3)
                if k is None:
                    print("Program Compilation error...")
                (env3, instsExitProg, heap4) = k                
                
                return (env3, insts1 + instsIf + instsExitProg, heap4)
            if label == 'Until':
                exp = children[0]
                pr1 = children[1]
                pr2 = children[2]

                # Compile the expression
                r = compileTerm(env, exp, heap)
                if r is None:
                    r = compileFormula(env, exp, heap)
                (insts1, addr1, heap2) = r

                # Compile nested program first
                j = compileProgram(env, pr1, heap2)
                if j is None:
                    print("Program Compilation error...")
                (env2, instsNestedProg, heap3) = j

                fresh = fresh + 1
                instsUntil = [\
                    "label startUntil"+str(fresh),\
                    "branch finishUntil"+str(fresh) + " " + str(addr1),\
                    ] + \
                    instsNestedProg + \
                    [\
                    "goto startUntil"+str(fresh),\
                    "label finishUntil" + str(fresh)\
                    ]
                
                # Compile remaining program
                k = compileProgram(env2, pr2, heap3)
                if k is None:
                    print("Program Compilation error...")
                (env3, instsExitProg, heap4) = k                
                
                return (env3, insts1 + instsUntil + instsExitProg, heap4)
            if label == 'Procedure':
                var = children[0]['Variable'][0]    # var = 'label'
                pr1 = children[1]
                pr2 = children[2]

                # Compile nested program first
                j = compileProgram(env, pr1, heap)
                if j is None:
                    instsNested = []
                    heap2 = heap
                    env2 = env
                (env2, instsNested, heap2) = j

                # Generate procedure machine instr.
                instsProc = procedure(var, instsNested)
                
                # Compile remaining program
                k = compileProgram(env2, pr2, heap2)
                if k is None:
                    print("Program Compilation error...")
                (env3, instsExitProg, heap3) = k                
                
                return (env3, instsProc + instsExitProg, heap3)
            if label == 'Call':
                var = children[0]['Variable'][0]    # var = 'label'
                pr1 = children[1]

                # Run procedure var, save machine instr.
                instsCall = call(var)

                # Compile remaining program
                k = compileProgram(env, pr1, heap)
                if k is None:
                    print("Program Compilation error...")
                (env2, instsExitProg, heap2) = k                
                
                return (env2, instsCall + instsExitProg, heap2)


# Problem 3d
def compile(s):
    global memorySetUp
    # Run string through interpreter
    parseTree = tokenizeAndParse(s)
    if not parseTree is None:
        # Need to reinitialize stack frame for
        # serparate, succesive calls to compile() in same Python Runtime Environment
        memorySetUp = False
        return (compileProgram({}, parseTree, 8))[1]


# eof
