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
    (r'[ \n\t]+', WHITESPACES),
    (r'//[^\n]*', COMMENT),
    (r'/\*[\s\S]*\*/', COMMENT),
    (r'/\*\*[\s\S]*\*/', JAVA_DOC),

    (r'[0-9]+[a-zA-Z_]+[0-9]*', INVALID_IDENTIFIER), 
    (r'[a-zA-Z_\$]\w*', IDENTIFIER),

    (r'\"([^\"]+)\"', STRING),
    (r'\'([^\"]+)\'', STRING),
    (r'\d+\.\d+', FLOATING_POINT_LITERAL),
    (r'\d+\.\d+[eE]\d+', FLOATING_POINT_LITERAL),
    (r'0b1[0-1]*', INTEGER_LITERAL),
    (r'0x[0-9a-f]+', INTEGER_LITERAL),
    (r'\d+', INTEGER_LITERAL),

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

def lex(characters, token_exprs):
    pos = 0
    tokens = []
    errors = 0
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag is not INVALID_IDENTIFIER:
                    token = (text, tag)
                    tokens.append(token)
                else:
                    errors+=1
                    sys.stderr.write('Invalid identifier at position %s : %s\n' % (pos, text))
                break
        if not match:
            errors+=1
            sys.stderr.write('Illegal character at position %s : %s\n' % (pos, characters[pos]))
            pos+=1
        else:
            pos = match.end(0)
    print('Found' , errors , 'errors')
    return tokens

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="files to parse")
    parser.add_argument("-t", "--tokens", help="show tokens", action="store_true")
    args = parser.parse_args()
    
    tokens = []

    for filename in args.files:
        with open(filename, 'r') as f:
            data = f.read()
            tokens.extend(lex(data, token_exprs))

    if args.tokens:
        for token in tokens:
            print(token)
