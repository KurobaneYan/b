/*
kill -SIGHUP `cat /home/yan/b/osis/6/exampled.lock`
kill `cat /home/yan/b/osis/6/exampled.lock`
*/

#include <stdio.h>
#include <fcntl.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>

#define RUNNING_DIR	"/home/yan/b/osis/6"
#define LOCK_FILE	"exampled.lock"
#define LOG_FILE	"exampled.txt"
#define CONFIG_FILE	"config.txt"

int count = 0;

void log_message(filename)
char *filename;
{
	FILE *logfile;
	FILE *fp;
	logfile=fopen(filename,"a");
	if(!logfile) return;
	char *estr;
	char str[100];
	long int ttime;
	if ((fp = fopen(CONFIG_FILE, "r")) != NULL) {
		while ((estr = fgets (str, sizeof(str),fp)) != NULL)  {
   			ttime = time (NULL);
			fprintf(logfile,"%d",count);
			fprintf(logfile,"%s",str);
   			fprintf(logfile,"%s\n",ctime(&ttime));
			count++;
		}
 	}
	fclose(logfile);
}

void signal_handler(sig)
int sig;
{
	switch(sig) {
		case SIGHUP:
			log_message(LOG_FILE);
			break;
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
	lfp=open(LOCK_FILE,O_RDWR|O_CREAT);
	if (lfp<0) exit(1);

	sprintf(str,"%d\n",getpid());
	write(lfp,str,strlen(str));
	signal(SIGCHLD,SIG_IGN);
	signal(SIGTSTP,SIG_IGN);
	signal(SIGTTOU,SIG_IGN);
	signal(SIGTTIN,SIG_IGN);
	signal(SIGHUP,signal_handler);
	signal(SIGTERM,signal_handler);
	log_message(LOG_FILE);
}

int main()
{
	daemonize();
	while(1) sleep(1);
}
