#ifndef ARGPARSE_H
#define ARGPARSE_H

#include <stdio.h>

typedef void (*Action)(FILE* const, const size_t, const char*, const char*);

typedef struct {
    Action action;
    char* file_open_type;
    size_t id;
    char* field;
    char* search_text;
} ParsedInput;

void parse_args(const int argc, char** const argv, ParsedInput* const input);

#endif // ARGPARSE_H
