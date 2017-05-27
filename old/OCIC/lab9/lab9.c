#include <sys/types.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#define RUNNING_DIR	"/home/kresik/OCIC/lab9"

void server();
void morz9nka();
char* tablemorz(char symbol);

void signal_handler(sig)
int sig;
{
	switch(sig) {
		case SIGTERM:
			exit(0);
			break;
	}
}

void daemonize()
{
	int i,lfp;
	char str[10];
	i=fork();
	if (i<0) exit(1);
	if (i>0) exit(0);

	setsid();
	
	chdir(RUNNING_DIR);

	signal(SIGCHLD,SIG_IGN);
	signal(SIGTSTP,SIG_IGN);
	signal(SIGTTOU,SIG_IGN);
	signal(SIGTTIN,SIG_IGN);
	signal(SIGHUP,SIG_IGN);
	signal(SIGTERM,signal_handler);
}

int main()
{
	daemonize();
    server();
}

void server()
{
    int err=-1;
    int server_sockfd, client_sockfd;
    int server_len, client_len;
    struct sockaddr_in server_address;
    struct sockaddr_in client_address;
    
    server_sockfd = socket(AF_INET, SOCK_STREAM, 0);
    
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);
    server_address.sin_port = htons(8052);
    server_len = sizeof(server_address);
 
    err=(bind(server_sockfd, (struct sockaddr *) &server_address, server_len));
 
    if(err!=0) printf("bind error!\n");
    err=-1;
    
    err=(listen(server_sockfd, 5));
    if(err!=0) printf("listen error!\n");
    for (int i = 0; i < 2; ++i)
    {
        char lenbuf[256];
 
        client_len = sizeof(client_address);
        client_sockfd = accept(server_sockfd, (struct sockaddr *) &client_address, &client_len);
 
        read(client_sockfd, lenbuf, sizeof(lenbuf));
        
        morz9nka(lenbuf);

        close(client_sockfd);
    }
}

void morz9nka(char *path)
{
	FILE *fp;
	FILE *fr;
	char c;
	fp = fopen(path, "r");
	fr = fopen("/home/kresik/OCIC/lab9/output.txt", "w");
	if (fp != NULL && fr != NULL) {
		while ((c = fgetc(fp)) != EOF) {
            fprintf(fr, "%s", tablemorz(c));
            fprintf(fr, "%s", " ");
        }
 	} else {
 		return;
 	}
	fclose(fr);
	fclose(fp);
	return;
}

char* tablemorz(char symbol)
{
	switch ( symbol ) {
        case 'a':       
            return "._";
 		case 'b':       
            return "_...";
        case 'c':       
            return "_._.";
        case 'd':       
            return "_..";
        case 'e':       
            return ".";
        case 'f':       
            return ".._.";
        case 'g':       
            return "__.";
        case 'h':       
            return "....";
        case 'i':       
            return "..";
        case 'j':       
            return ".___";
        case 'k':       
            return "_._";
        case 'l':       
            return "._..";
        case 'm':       
            return "__";
        case 'n':       
            return "_.";
        case 'o':       
            return "___";
        case 'p':       
            return ".__.";
        case 'q':       
            return "__._";
        case 'r':       
            return "._.";
        case 's':       
            return "...";
        case 't':       
            return "_";
        case 'u':       
            return ".._";
        case 'v':       
            return "..._";
        case 'w':       
            return ".__";
        case 'x':       
            return "_.._";
        case 'y':       
            return "_.__";
        case 'z':       
            return "__..";
        case '1':       
            return ".____";
        case '2':       
            return "..___";
        case '3':       
            return "...__";
        case '4':       
            return "...._";
        case '5':       
            return ".....";
        case '6':       
            return "_....";
        case '7':       
            return "__...";
        case '8':       
            return "___..";
        case '9':       
            return "____.";
        case '0':       
            return "_____";
        default:
            return " ";
    }
}