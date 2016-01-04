#####################################################################
# Hwa-seung Erstling
# CAS CS 320, Fall 2015
# Midterm
# parse.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #1. ***************
#  ****************************************************************
#

import re

def number(tokens, top = True):
    if re.compile(r"(-(0|[1-9][0-9]*)|(0|[1-9][0-9]*))").match(tokens[0]):
        return (int(tokens[0]), tokens[1:])

def variable(tokens, top = True):
    if re.compile(r"[a-z][A-Za-z0-9]*").match(tokens[0]):
        return (str(tokens[0]), tokens[1:])

def numberWrapped(tokens, top = True):
    if re.compile(r"(-(0|[1-9][0-9]*)|(0|[1-9][0-9]*))").match(tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])

def variableWrapped(tokens, top = True):
    if re.compile(r"[a-z][A-Za-z0-9]*").match(tokens[0]):
        return ({"Variable": [tokens[0]]}, tokens[1:])

def expression(tmp, top = True):
    seqs = [\
        ('Plus', [left, '+', expression]), \
        ('SKIP', [left]) ]

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

def left(tmp, top = True):
    seqs = [\
        ('True', ['true']), \
        ('False', ['false']), \
        ('Number', [number]), \
        ('Variable', ['$', variable]), \
        ('Element', ['@', variableWrapped, '[', expression, ']']) \
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
                
def program(tmp, top = True):
    seqs = [\
        ('Assign', ['@', variableWrapped, ':=','[', expression, ',', expression, ',', expression, ']',';', program]), \
        ('Print', ['print', expression, ';', program]), \
        ('Loop', ['loop', '$', variableWrapped, 'from', numberWrapped, '{', program, '}', program]) \
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

def tokenizeAndParse(s):
    tokens = re.split(r"(\s+|:=|print|true|false|\+|loop|from|{|}|;|\[|\]|,|@|\$)", s)
    tokens = [t for t in tokens if not t.isspace() and not t == ""]
    (p, tokens) = program(tokens)
    return p

#eof
