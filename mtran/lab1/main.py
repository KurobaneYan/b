#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse, sys, re

WHITESPACES = 'Whitespaces'
OPERATOR = 'Operator'
KEYWORD = 'Keyword'
INTEGER_LITERAL = 'Integer literal'
FLOATING_POINT_LITERAL = 'Floating point literal'
STRING = 'Stirng literal'
IDENTIFIER = 'Identifier'
INVALID_IDENTIFIER = 'Invalid identifier'
SEPARATOR = 'Separator'
COMMENT = 'Comment'
JAVA_DOC = 'JavaDoc'

token_exprs = [
    (r'[ \t]+', None),

    # comments
    (r'//[^\n]*', COMMENT),
    (r'/\*[\s\S]*\*/', COMMENT),
    (r'/\*\*[\s\S]*\*/', JAVA_DOC),

    # identifiers
    (r'[0-9]+[a-zA-Z_\$][\w\$]*', INVALID_IDENTIFIER), 
    (r'[a-zA-Z_\$][\w\$]*', IDENTIFIER),

    # literals
    (r'\"([^\"]+)\"', STRING),
    (r'\'([^\"]+)\'', STRING),
    (r'\d+\.\d+', FLOATING_POINT_LITERAL),
    (r'\d+\.\d+[eE]\d+', FLOATING_POINT_LITERAL),
    (r'0b1[0-1]*', INTEGER_LITERAL),
    (r'0x[0-9a-f]+', INTEGER_LITERAL),
    (r'\d+', INTEGER_LITERAL),

    # keywords
    (r'abstract', KEYWORD),
    (r'assert', KEYWORD),
    (r'boolean', KEYWORD),
    (r'break', KEYWORD),
    (r'byte', KEYWORD),
    (r'case', KEYWORD),
    (r'catch', KEYWORD),
    (r'char', KEYWORD),
    (r'class', KEYWORD),
    (r'const', KEYWORD),
    (r'continue', KEYWORD),
    (r'default', KEYWORD),
    (r'do', KEYWORD),
    (r'double', KEYWORD),
    (r'else', KEYWORD),
    (r'enum', KEYWORD),
    (r'extends', KEYWORD),
    (r'final', KEYWORD),
    (r'finally', KEYWORD),
    (r'float', KEYWORD),
    (r'for', KEYWORD),
    (r'goto', KEYWORD),
    (r'if', KEYWORD),
    (r'implements', KEYWORD),
    (r'import', KEYWORD),
    (r'instanceof', KEYWORD),
    (r'int', KEYWORD),
    (r'interface', KEYWORD),
    (r'long', KEYWORD),
    (r'native', KEYWORD),
    (r'new', KEYWORD),
    (r'package', KEYWORD),
    (r'private', KEYWORD),
    (r'protected', KEYWORD),
    (r'public', KEYWORD),
    (r'return', KEYWORD),
    (r'short', KEYWORD),
    (r'static', KEYWORD),
    (r'strictfp', KEYWORD),
    (r'strictfp', KEYWORD),
    (r'switch', KEYWORD),
    (r'synchronized', KEYWORD),
    (r'this', KEYWORD),
    (r'throw', KEYWORD),
    (r'throws', KEYWORD),
    (r'transient', KEYWORD),
    (r'try', KEYWORD),
    (r'void', KEYWORD),
    (r'volatile', KEYWORD),
    (r'while', KEYWORD),

    # operators
    (r'=', OPERATOR),
    (r'\+', OPERATOR),
    (r'-', OPERATOR),
    (r'\*', OPERATOR),
    (r'%', OPERATOR),
    (r'/', OPERATOR),
    (r'<<', OPERATOR),
    (r'>>', OPERATOR),
    (r'>>>', OPERATOR),
    (r'&', OPERATOR),
    (r'\^', OPERATOR),
    (r'\|', OPERATOR),
    (r'\|\|', OPERATOR),
    (r'&&', OPERATOR),
    (r'==', OPERATOR),
    (r'<=', OPERATOR),
    (r'<', OPERATOR),
    (r'>=', OPERATOR),
    (r'>', OPERATOR),
    (r'!=', OPERATOR),

    # separators
    (r'\:', SEPARATOR),
    (r'\[', SEPARATOR),
    (r'\]', SEPARATOR),
    (r'\{', SEPARATOR),
    (r'\}', SEPARATOR),
    (r'\.', SEPARATOR),
    (r'\,', SEPARATOR),
    (r'\(', SEPARATOR),
    (r'\)', SEPARATOR),
    (r';', SEPARATOR),
]

def lex_line(characters, token_exprs, i):
    pos = 0
    tokens = []
    errors = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag is not None:
                    if tag is not INVALID_IDENTIFIER:
                        token = (text, tag)
                        tokens.append(token)
                    else:
                        errors.append([i, pos, text])
                break
        if not match:
            errors.append([i, pos, characters[pos]])
            pos+=1
        else:
            pos = match.end(0)
    return [tokens, errors]

def lex(text, token_exprs):
    tokens = []
    errors = []
    lines = text.split('\n')
    for i in range(len(lines)):
        if lines[i] is not '':
            temp = lex_line(lines[i], token_exprs, i+1)
            tokens.extend(temp[0])
            errors.extend(temp[1])
    if errors:
        print(len(errors), 'errors:')
        for error in errors:
            print('Line', error[0], 'position', error[1], ':', error[2])
    return tokens

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="files to parse")
    parser.add_argument("-c", "--code", help="show code", action="store_true")
    parser.add_argument("-t", "--tokens", help="show tokens", action="store_true")
    args = parser.parse_args()

    tokens = []

    for filename in args.files:
        with open(filename, 'r') as f:
            data = f.read()
            if args.code:
                print(data)
            tokens.extend(lex(data, token_exprs))
            if args.tokens:
                for token in tokens:
                    print('{0:20} == {1:20}'.format(token[0], token[1]))

