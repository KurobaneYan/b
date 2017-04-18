#include <stdio.h>
#include <stdlib.h>
#include "io.h"

void print_note(const NoteEntry* const note) {
    printf("ID: %zu\nTitle: %s\nAuthor: %s\nNote: %s\n\n",
           note->id,
           note->title,
           note->author,
           note->note);
}

void read_line(char* buffer, size_t length) {
    memset(buffer, 0, length);
    for (char ch; (ch = getchar()) != '\n' && ch != EOF;) {
        if (length > 1) {
            *buffer++ = ch;
            --length;
        }
    }
    *buffer = 0;
}

void edit_promt(NoteEntry* const entry) {
    printf("New title: ");
    read_line(entry->title, FIELD_TITLE_SIZE);
    printf("New author: ");
    read_line(entry->author, FIELD_AUTHOR_SIZE);
    printf("New note: ");
    read_line(entry->note, FIELD_NOTE_SIZE);
}

void exit_with_error(const char* const error, const size_t error_code) {
    printf("%s\n", error);
    exit(error_code);
}
