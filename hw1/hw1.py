# Hwa-seung Erstling
# CS 320, Fall 2015
# HW1

import re

# 1a
def regexp(tokens):
    x = [re.escape(a) for a in tokens]
    return "|".join([str(c) for c in x])

# 1b
def tokenize(terminals,s):
    tokens = [t for t in re.split(r"(\s+|"+regexp(terminals)+")" ,s)]
    return [t for t in tokens if not t.isspace() and not t == ""]
    
# 1c
def tree(tokens):
    if tokens[0] == 'two' and tokens[1] == 'children' and tokens[2] == 'start':
        (e1, tokens) = tree(tokens[3:])
        if tokens[0] == ';':
            (e2, tokens) = tree(tokens[1:])
            if tokens[0] == 'end':
                return ({'Two':[e1,e2]}, tokens[1:])

    if tokens[0] == 'one' and tokens[1] == 'child' and tokens[2] == 'start':
        (e3, tokens) = tree(tokens[3:])
        if tokens[0] == 'end':
          return ({'One':[e3]}, tokens[1:])

    if tokens[0] == 'zero' and tokens[1] == 'children':
        return ('Zero', tokens[2:])

# Taken from Lapets' notes and modified
def number(tokens, top = True):
    if re.match(r"^((0|([1-9][0-9]*))|(-?([1-9][0-9]*)))$", tokens[0]):
        return (int(tokens[0]), tokens[1:])

# 2a
def variable(tokens, top = True):
    if re.match(r"^(([A-Z]|[a-z])+)$", tokens[0]):
        return (tokens[0], tokens[1:])

# Used when variable is not called from term
def variableWithLabel(tokens, top = True):
    if re.match(r"^(([A-Z]|[a-z])+)$", tokens[0]):
        return ({'Variable':[tokens[0]]}, tokens[1:])
# 2b
# Taken from Lapets' notes and modified
def term(tmp, top = True):
    seqs = [\
        ('Number', ['#', number]), \
        ('Variable', ['$', variable]), \
        ('Plus', ['plus', '(', term, ',', term, ')']), \
        ('Max', ['max', '(', term, ',', term, ')']), \
        ('If', ['if','(', formula, ',', term, ',', term, ')']), \
        ('Plus', ['(', term, '+', term, ')']), \
        ('Max', ['(', term, 'max', term, ')']), \
        ('If', ['(', formula, '?', term, ':', term, ')']) \
        ]

    # Try each choice sequence.
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect parse trees from recursive calls.
        
        # Walk through the sequence and either
        # match terminals to tokens or make
        # recursive calls depending on whether
        # the sequence entry is a terminal or
        # parsing function.
        for x in seq:
            if type(x) == type(""): # Terminal.

                if tokens[0] == x: # Does terminal match token?
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

        # Check that we got either a matched token
        # or a parse tree for each sequence entry.
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:            
                return ({label:es} if len(es) > 0 else label, tokens)

# 2c
# Taken from Lapets' notes and modified
def formula(tmp, top = True):
    seqs = [\
        ('True', ['true']), \
        ('False', ['false']), \
        ('Not', ['not', '(', formula, ')']), \
        ('Xor', ['xor', '(', formula, ',', formula, ')']), \
        ('Equal', ['equal', '(', term, ',', term, ')']), \
        ('Less', ['less', '(', term, ',', term, ')']), \
        ('Greater', ['greater', '(', term, ',', term, ')']), \
        ('Xor', ['(', formula, 'xor', formula, ')']), \
        ('Equal', ['(', term, '==', term, ')']), \
        ('Less', ['(', term, '<', term, ')']), \
        ('Greater', ['(', term, '>', term, ')']) \
        ]

    # Try each choice sequence.
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect parse trees from recursive calls.
        
        # Walk through the sequence and either
        # match terminals to tokens or make
        # recursive calls depending on whether
        # the sequence entry is a terminal or
        # parsing function.
        for x in seq:
            if type(x) == type(""): # Terminal.

                if tokens[0] == x: # Does terminal match token?
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

        # Check that we got either a matched token
        # or a parse tree for each sequence entry.
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)

# 2d, 3
# Taken from Lapets' notes and modified
def program(tmp, top = True):
    seqs = [\
        ('Print', ['print', term, ';', program]), \
        ('Input', ['input', '$', variableWithLabel, ';', program]), \
        ('Assign', ['assign', '$', variableWithLabel, ':=', term, ';', program]), \
        ('End', ['end', ';']), \
        ]

    # Try each choice sequence.
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect parse trees from recursive calls.
        
        # Walk through the sequence and either
        # match terminals to tokens or make
        # recursive calls depending on whether
        # the sequence entry is a terminal or
        # parsing function.
        for x in seq:
            if type(x) == type(""): # Terminal.

                if tokens[0] == x: # Does terminal match token?
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

        # Check that we got either a matched token
        # or a parse tree for each sequence entry.
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:              
                return ({label:es} if len(es) > 0 else label, tokens)

# 2e, 3
def parse(s):
    t = tokenize(['print',';','input','$','assign',':=','end','true','false', \
                  'not','xor','equal','(',')',',','less','greater','#', \
                  'plus','max','if','==','<','>','+','?',':'],s)
    r = program(t)
    if not r is None:
        return r[0]


