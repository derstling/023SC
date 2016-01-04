# Hwa-seung Erstling
# CS 320, Fall 2015
# HW2
# parse.py

# Starter code taken from Lapets' notes and then modified

import re

# Problem 1a
def number(tokens, top = True):
    if re.match(r"^(0|([1-9][0-9]*))$", tokens[0]):
        return (int(tokens[0]), tokens[1:])

def variable(tokens, top = True):
    unusable = ['true','false','and','nonzero','not','if','print','assign','do','until']
    if re.match(r"^([a-z](([A-Z]|[a-z]|[0-9])*))$", tokens[0]) \
       and tokens[0] not in unusable:
        return (tokens[0], tokens[1:])

def variableWithLabel(tokens, top = True):
    unusable = ['true','false','and','nonzero','not','if','print','assign','do','until']
    if re.match(r"^([a-z](([A-Z]|[a-z]|[0-9])*))$", tokens[0]) \
       and tokens[0] not in unusable:
        return ({'Variable':[tokens[0]]}, tokens[1:])

# Problem 1b
def formula(tmp, top = True):
    seqs = [\
        ('And', [leftFormula, 'and', formula]), \
        ('LEFT', [leftFormula]) ]

    # Try each choice sequence.
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect parse trees from recursive calls.

        for x in seq:
            if type(x) == type(""): # Terminal.

                if len(tokens) > 0 and tokens[0] == x: # Does terminal match token?
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.

            else: # Parsing function.

                r = x(tokens, False) 
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]

        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                if label is 'LEFT':
                    return r
                else:
                    return ({label:es} if len(es) > 0 else label, tokens)

def leftFormula(tmp, top = True):
    seqs = [\
        ('Nonzero', ['nonzero','(', term, ')']), \
        ('Not', ['not','(', formula, ')']), \
        ('Variable', [variable]), \
        ('True', ['true']), \
        ('False', ['false']), \
        ('Equal', ['(', term, '=', term, ')']), \
        ('Less', ['(', term, '<', term, ')']), \
        ('Greater', ['(', term, '>', term, ')']) \
        ]

    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = []
        es = []
            
        for x in seq:
            if type(x) == type(""): # Terminal.

                if len(tokens) > 0 and tokens[0] == x: # Does terminal match token?
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.

            else: # Parsing function.

                # Call parsing function recursively
                r = x(tokens, False) 
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]

            if len(ss) + len(es) == len(seq):
                if not top or len(tokens) == 0:
                    return ({label:es} if len(es) > 0 else label, tokens)


# Problem 1c
def term(tmp, top = True):
    seqs = [\
        ('Plus', [factor, '+', term]), \
        ('SKIP', [factor]) ]

    # Try each choice sequence.
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect parse trees from recursive calls.

        for x in seq:
            if type(x) == type(""): # Terminal.

                if len(tokens) > 0 and tokens[0] == x: # Does terminal match token?
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.

            else: # Parsing function.

                r = x(tokens, False) 
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]

        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                if label is 'SKIP':
                    return r
                else:
                    return ({label:es} if len(es) > 0 else label, tokens)

def factor(tmp, top = True):
    seqs = [\
        ('Mult', [leftFactor, '*', factor]), \
        ('SKIP', [leftFactor]) ]

    # Try each choice sequence.
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect parse trees from recursive calls.

        for x in seq:
            if type(x) == type(""): # Terminal.

                if len(tokens) > 0 and tokens[0] == x: # Does terminal match token?
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.

            else: # Parsing function.

                r = x(tokens, False) 
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]

        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                if label is 'SKIP':
                    return r
                else:
                    return ({label:es} if len(es) > 0 else label, tokens)

def leftFactor(tmp, top = True):
    seqs = [\
        ('Parens', ['(', term, ')']), \
        ('If', ['if','(', formula, ',', term, ',', term, ')']), \
        ('Variable', [variable]), \
        ('Number', [number]) \
        ]

    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = []
        es = []
            
        for x in seq:
            if type(x) == type(""): # Terminal.

                if len(tokens) > 0 and tokens[0] == x: # Does terminal match token?
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.

            else: # Parsing function.

                # Call parsing function recursively
                r = x(tokens, False) 
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]

            if len(ss) + len(es) == len(seq):
                if not top or len(tokens) == 0:
                    return ({label:es} if len(es) > 0 else label, tokens)

# Not needed since we will try both possibilities (formula, term) in program() below 
# def expression(tmp, top = True):

# Problem 1d
def program(tmp, top = True):

    seqs = [\
        ('Print', ['print', formula, ';', program]), \
        ('Print', ['print', term, ';', program]), \
        ('Assign', ['assign', variableWithLabel, ':=', formula, ';', program]), \
        ('Assign', ['assign', variableWithLabel, ':=', term, ';', program]), \
        ('If', ['if', formula, '{', program, '}', program]), \
        ('If', ['if', term, '{', program, '}', program]), \
        ('DoUntil', ['do', '{', program, '}', 'until', formula, ';', program]), \
        ('DoUntil', ['do', '{', program, '}', 'until', term, ';', program]) \
        ]    

    if len(tmp) == 0:
        return ('End', tmp)

    if len(tmp) > 0 and tmp[0] is '}':
        return ('End', tmp)

    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = []
        es = []
            
        for x in seq:

            if type(x) == type(""): # Terminal.

                if len(tokens) > 0 and tokens[0] == x: # Does terminal match token?
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.

            else: # Parsing function.

                # Call parsing function recursively
                r = x(tokens, False) 
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]

            if len(ss) + len(es) == len(seq):
                if not top or len(tokens) == 0:
                    return ({label:es} if len(es) > 0 else label, tokens)

