#include "argparse.h"
#include "notebook.h"
#include "io.h"

static void add(FILE* const file_ptr,
                const size_t ignored1,
                const char* ignored2,
                const char* ignored3) {
    add_note(file_ptr);
}

static void print_all(FILE* const file_ptr,
                      const size_t ignored1,
                      const char* ignored2,
                      const char* ignored3) {
    print_all_notes(file_ptr);
}

static void delete(FILE* const file_ptr,
                   const size_t id,
                   const char* ignored1,
                   const char* ignored2) {
    delete_note(id, file_ptr);
}

static void edit(FILE* const file_ptr,
                 const size_t id,
                 const char* ignored1,
                 const char* ignored2) {
    edit_note(id, file_ptr);
}

static void find(FILE* const file_ptr,
                 const size_t ignored,
                 const char* field,
                 const char* search_text) {
    find_note(field, search_text, file_ptr);
}

void parse_args(const int argc, char** const argv, ParsedInput* const input) {
    if (argc == 2) {
        input->file_open_type = "ab+";
        if (strcmp(argv[1], "--add") == 0) {
            input->action = add;
            return;
        } else if (strcmp(argv[1], "--print_all") == 0)  {
            input->action = print_all;
            return;
        }
    } else if (argc == 3) {
        input->file_open_type = "rb+";
        if (sscanf(argv[2], "%zu", &input->id) == 0) {
            exit_with_error("Parse error", ERROR_PARSE);
        }

        if (strcmp(argv[1], "--delete") == 0) {
            input->action = delete;
            return;
        } else if (strcmp(argv[1], "--edit") == 0) {
            input->action = edit;
            return;
        }
    } else if (argc == 4) {
        if (strcmp(argv[1], "--find") == 0) {
            input->action = find;
            input->file_open_type = "ab+";
            input->field = argv[2];
            input->search_text = argv[3];
            return;
        }
    }

    exit_with_error("Note book. Usage:\n\
app --add\n\
app --delete id\n\
app --edit id\n\
app --find field search_text\n\
app --print_all\n", 0);
}
