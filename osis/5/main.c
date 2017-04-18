#include <stdio.h>
#include "argparse.h"
#include "io.h"

int main(int argc, char** argv) {
    ParsedInput input = { 0 };
    parse_args(argc, argv, &input);

    FILE *file_ptr = fopen(STORAGE_FILENAME, input.file_open_type);
    if (file_ptr != NULL) {
        input.action(file_ptr, input.id, input.field, input.search_text);
        fclose(file_ptr);
    } else {
        exit_with_error("Can't create storage", ERROR_CANT_CREATE_FILE);
    }

    return 0;
}
