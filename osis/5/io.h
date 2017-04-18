#ifndef IO_H
#define IO_H

#include "notebook.h"

#define ERROR_CANT_CREATE_FILE 1
#define ERROR_PARSE 5

void print_note(const NoteEntry* const note);

void read_line(char* buffer, size_t length);

void edit_promt(NoteEntry* const entry);

void exit_with_error(const char* const error, const size_t error_code);


#endif // IO_H
