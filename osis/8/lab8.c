#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <string.h>

#define SHARED_MEMORY_OBJECT_SIZE 50

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
char b_f[3] = "pf";
char b_s[3] = "rf";
int len = 0;

void first_thread(void *p) {
    FILE *pf;
    int shm;
    if ((pf = fopen("file_first.txt", "r")) < 0) {
        printf("Error open f1\n");
        return;
    }
    for (;;) {
        len = 0;
        char *addr_first;
        char c;
        char buf[SHARED_MEMORY_OBJECT_SIZE];
        for (int i = 0; i < SHARED_MEMORY_OBJECT_SIZE; ++i) {
            if ((c = fgetc(pf)) != EOF) {
                buf[i] = c;
                len++;
            }
        }
        pthread_mutex_lock(&mutex);
        if ((shm = shm_open(b_f, O_CREAT|O_RDWR, 0777)) == -1) {
            printf("Error shm_open first\n");
            return;
        }
        if (ftruncate(shm, len) == -1) {
            printf("Error ftruncate first\n");
            return;
        }
        addr_first = mmap(0, len, PROT_WRITE, MAP_SHARED, shm, 0);
        memcpy(addr_first, buf, len);
        munmap(addr_first, len);
        close(shm);
        char chr = b_f[0];
        b_f[0] = b_s[0];
        b_s[0] = chr;
        chr = b_f[1];
        b_f[1] = b_s[1];
        b_s[1] = chr;
        pthread_mutex_unlock(&mutex);
        sleep(1);
        if (len != SHARED_MEMORY_OBJECT_SIZE) {
            break;
        }
    }
    fclose(pf);
    shm_unlink(b_f);
    shm_unlink(b_s);
}

void second_thread(void *p) {
    FILE *rf;
    int shm;
    if ((rf = fopen("file_second.txt", "w")) < 0) {
        printf("Error open f2\n");
    }
    for (;;) {
        char *addr_second;
        pthread_mutex_lock(&mutex);
        if ((shm = shm_open(b_s, O_RDWR, 0777)) == -1) {
            printf("Error shm_open second\n");
            return;
        }
        addr_second = mmap(0, len, PROT_READ, MAP_SHARED, shm, 0);
        fprintf(rf, "%s", addr_second);
        munmap(addr_second, len);
        close(shm);
        char chr = b_f[0];
        b_f[0] = b_s[0];
        b_s[0] = chr;
        chr = b_f[1];
        b_f[1] = b_s[1];
        b_s[1] = chr;
        pthread_mutex_unlock(&mutex);
        if (len != SHARED_MEMORY_OBJECT_SIZE) {
            break;
        }
        sleep(1);
    }
    fclose(rf);
}

int main(int argc, char ** argv) {
    pthread_t thread_1;
    pthread_t thread_2;

    pthread_create(&thread_1, NULL, (void *)&first_thread, NULL);
    sleep(0.5);
    pthread_create(&thread_2, NULL, (void *)&second_thread, NULL);

    pthread_join(thread_1, NULL);
    pthread_join(thread_2, NULL);
    return 0;
}