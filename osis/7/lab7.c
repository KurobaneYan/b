#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <time.h>

#define BUFSIZE 50
#define FIFO "/media/AddDrive/STUD/3stage/sem2/osis/OCIC/lab7/fifo"

int main(int argc, char **argv)
{
	int readfd, writefd;
	pid_t childpid;
	int fd;
	int flag = mkfifo(FIFO, 0777);
	if (flag == 0) {
		if ( (fd = open(FIFO, O_WRONLY)) <= 0 ) {
			printf("Error open for write");
        	return 0;
    	}
    	long int ttime;
    	char buf[BUFSIZE];
    	for (int i = 0; i < 4; ++i) {
    		ttime = time (NULL);
    		sprintf( buf, "%s", ctime(&ttime));
	    	write(fd, buf, BUFSIZE - 1);
	    	sleep(1);
	    }
	    printf("Server end\n");
	    remove(FIFO);
	} else {
		if (errno == EEXIST) {
			if ( (fd = open(FIFO, O_RDONLY)) <= 0 ) {
				printf("Error open for read");
	        	return 0;
	    	}
	    	char buf[BUFSIZE];
	    	for (int i = 0; i < 4; ++i) {
		    	read(fd, buf, BUFSIZE-1);
		    	printf("Time : %s", buf);
		    	sleep(1);
		    }
		printf("Client end\n");
		} else {
			printf("Error fifo file\n");
		}
	}
	close(fd);
	return 0;
}
