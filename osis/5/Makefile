CC=gcc
CFLAGS=-Wall -pedantic
LDFLAGS=
SOURCES=main.c argparse.c notebook.c io.c
OBJECTS=$(SOURCES:.c=.o)
TARGET=notebook

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf *.o $(TARGET)
