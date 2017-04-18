#include "notebook.h"
#include "io.h"

static const size_t ERROR_NOTE_NOT_FOUND = 2;
static const size_t ERROR_ID_NOT_FOUND = 3;
static const size_t ERROR_FIELD_NAME = 6;

static size_t get_next_id() {
    size_t result = 0;
    FILE *file = fopen(INTERNAL_DATA_FILENAME, "rb+");
    if (file != NULL) {
        fread(&result, sizeof(result), 1, file);
        ++result;
        rewind(file);
        fwrite(&result, sizeof(result), 1, file);
        fclose(file);
    } else {
        file = fopen(INTERNAL_DATA_FILENAME, "wb");
        if (file != NULL) {
            fwrite(&result, sizeof(result), 1, file);
            fclose(file);
        } else {
            exit_with_error("Can't create file internal_data.dat",
                            ERROR_CANT_CREATE_FILE);
        }
    }

    return result;
}

static size_t get_file_size(FILE* const file_ptr) {
    const size_t current_position = ftell(file_ptr);
    fseek(file_ptr, 0, SEEK_END);
    const size_t file_size = ftell(file_ptr);
    fseek(file_ptr, current_position, SEEK_SET);

    return file_size;
}

static size_t get_note(const size_t id, NoteEntry* const entry, FILE* const file_ptr) {
    fread(entry, sizeof(NoteEntry), 1, file_ptr);

    for (size_t position = 0; !feof(file_ptr); ++position) {
        if (entry->id == id) {
            return position;
        }
        fread(entry, sizeof(NoteEntry), 1, file_ptr);
    }

    exit_with_error("Note does not exist.", ERROR_NOTE_NOT_FOUND);
    return -1;
}


void add_note(FILE* const file_ptr) {
    NoteEntry entry = { 0 };

    entry.id = get_next_id();
    edit_promt(&entry);

    fwrite(&entry, sizeof(entry), 1, file_ptr);
}

void edit_note(const size_t id, FILE* const file_ptr) {
    NoteEntry entry = { 0 };
    size_t position = get_note(id, &entry, file_ptr);
    edit_promt(&entry);
    fseek(file_ptr, position * sizeof(entry), SEEK_SET);
    fwrite(&entry, sizeof(entry), 1, file_ptr);
}

void find_note(const char* const field,
               const char* const search_text,
               FILE* const file_ptr) {
    NoteEntry entry = { 0 };
    char* target_field = 0;

    if (strcmp(field, FIELD_AUTHOR_NAME) == 0) {
        target_field = entry.author;
    } else if (strcmp(field, FIELD_TITLE_NAME) == 0) {
        target_field = entry.title;
    } else if (strcmp(field, FIELD_NOTE_NAME) == 0) {
        target_field = entry.note;
    } else {
        exit_with_error("Wrong field name", ERROR_FIELD_NAME);
    }

    fread(&entry, sizeof(entry), 1, file_ptr);
    while (!feof(file_ptr)) {
        if (strstr(target_field, search_text) != NULL) {
            print_note(&entry);
        }
        fread(&entry, sizeof(entry), 1, file_ptr);
    }
}

void delete_note(const size_t id, FILE* const file_ptr) {
    NoteEntry entry = { 0 };

    fread(&entry, sizeof(entry), 1, file_ptr);
    while (!feof(file_ptr) && id != entry.id) {
        fread(&entry, sizeof(entry), 1, file_ptr);
    }

    if (feof(file_ptr) && id != entry.id) {
        exit_with_error("Id not found", ERROR_ID_NOT_FOUND);
    }

    fread(&entry, sizeof(entry), 1, file_ptr);
    while (!feof(file_ptr)) {
        fseek(file_ptr, -2 * sizeof(entry), SEEK_CUR);
        fwrite(&entry, sizeof(entry), 1, file_ptr);
        fseek(file_ptr, sizeof(entry), SEEK_CUR);
        fread(&entry, sizeof(entry), 1, file_ptr);
    }
    truncate(STORAGE_FILENAME, get_file_size(file_ptr) - sizeof(entry));
}

void print_all_notes(FILE* const file_ptr) {
    NoteEntry entry = { 0 };

    fread(&entry, sizeof(entry), 1, file_ptr);
    while (!feof(file_ptr)) {
        print_note(&entry);
        fread(&entry, sizeof(entry), 1, file_ptr);
    }
}
