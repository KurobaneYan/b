#ifndef NOTEBOOK_H
#define NOTEBOOK_H

#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define FIELD_AUTHOR_SIZE 64
#define FIELD_TITLE_SIZE 64
#define FIELD_NOTE_SIZE 256
#define FIELD_AUTHOR_NAME "author"
#define FIELD_TITLE_NAME "title"
#define FIELD_NOTE_NAME "note"

#define INTERNAL_DATA_FILENAME "internal_data.dat"
#define STORAGE_FILENAME "storage.dat"

typedef struct {
    size_t id;
    char author[FIELD_AUTHOR_SIZE];
    char title[FIELD_TITLE_SIZE];
    char note[FIELD_NOTE_SIZE];
} NoteEntry;

void add_note(FILE* const file_ptr);

void edit_note(const size_t id, FILE* const file_ptr);

void find_note(const char* const field,
               const char* const search_text,
               FILE* const file_ptr);

void delete_note(const size_t id, FILE* const file_ptr);

void print_all_notes(FILE*const file_ptr);

#endif // NOTEBOOK_H
