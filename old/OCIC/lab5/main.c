#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define INPUT_FILE 				"input.txt"
#define OUTPUT_FILE				"output.txt"
#define DICTIONARY_FILE_NAME 	"dictionary.txt"

#define CANNOT_OPEN_INPUT_FILE 			1
#define CANNOT_OPEN_OUTPUT_FILE 		2
#define CANNOT_OPEN_DICTIONARY_FILE 	3

#define INPUT_FILE_FAILURE_MESSAGE 		"Cannot open input file."
#define OUTPUT_FILE_FAILURE_MESSAGE 	"Cannot open output file."
#define DICTIONARY_FILE_FAILURE_MESSAGE "Cannot open dictionary file."

#define MAXIMUM_LINE_LENGTH 100

#define HIDDEN_WORD_MARKER '*'

int is_word_forbidden(char *, FILE *);
void hide_word(char *);

int main(void) {
	FILE *input_file, *output_file, *dictionary_file;
	char word[MAXIMUM_LINE_LENGTH];
	int is_eof_reached;

	input_file = fopen(INPUT_FILE, "r");
	if (input_file == NULL) {
		printf(INPUT_FILE_FAILURE_MESSAGE);
		return CANNOT_OPEN_INPUT_FILE;
	}
	
	output_file = fopen(OUTPUT_FILE, "w");
	if (output_file == NULL) {
		printf(OUTPUT_FILE_FAILURE_MESSAGE);
		return CANNOT_OPEN_OUTPUT_FILE;
	}
	
	dictionary_file = fopen(DICTIONARY_FILE_NAME, "r");
	if (dictionary_file == NULL) {
		printf(DICTIONARY_FILE_FAILURE_MESSAGE);
		return CANNOT_OPEN_DICTIONARY_FILE;
	}
	
	do {
		char space;
		
		is_eof_reached = fscanf(input_file, "%s", word) == EOF;
		
		if (is_word_forbidden(word, dictionary_file)) {
			hide_word(word);
		}
		fprintf(output_file, "%s", word);
		
		for (;;) {
			space = fgetc(input_file);
			
			if (isspace(space) && space != EOF) {
				fputc(space, output_file);
			} else {
				if (space == EOF) {
					is_eof_reached = 1;
				} else {
					ungetc(space, input_file);
				}
				break;
			}
		}
	} while (!is_eof_reached);
	
	fclose(dictionary_file);
	fclose(output_file);
	fclose(input_file);

	return 0;
}

int is_word_forbidden(char *word, FILE *dictionary_file) {
	char lowercase_word[MAXIMUM_LINE_LENGTH];
	char forbidden_word[MAXIMUM_LINE_LENGTH];
	int word_length = strlen(word);
	int result = 0;
		
	strncpy(lowercase_word, word, word_length);
	for (int i = 0; i < word_length; i++) {
		lowercase_word[i] = tolower(lowercase_word[i]);
	}

	while (fscanf(dictionary_file, "%s", forbidden_word) != EOF) {
		for (int i = 0; i < strlen(forbidden_word); i++) {
			forbidden_word[i] = tolower(forbidden_word[i]);
		}
		
		if (!strcmp(lowercase_word, forbidden_word)) {
			result = 1;
			break;
		}
	}
	
	rewind(dictionary_file);
	return result;
}

void hide_word(char *word) {
	int word_length = strlen(word);

	for (int i = 0; i < word_length; i++) {
		word[i] = HIDDEN_WORD_MARKER;
	}
	word[word_length] = '\0';
}