#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
 
void client();
 
int main()
{
    client();
    return 0;
}
 
void client()
{
    int sockfd;
    int len = 0;
    struct sockaddr_in address;
    int result;
 
    sockfd = socket (AF_INET, SOCK_STREAM, 0);
    
    address.sin_family = AF_INET;
    address.sin_addr.s_addr= inet_addr("127.0.0.1");
    address.sin_port = htons(8052);
    len = sizeof(address);
    
    result = connect(sockfd, (struct sockaddr *) &address, len);
    
    if(result == -1)
    {
        printf("Don't connect\n");
        return;
    }
    
    char lenbuf[256] = "/home/yan/b/osis/9/input.txt";
    write(sockfd, lenbuf, 100);

    close(sockfd);
}
