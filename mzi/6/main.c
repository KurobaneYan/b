#include <stdio.h>
#include <string.h>

int main(void) {
    char buff[2];
    int pass = 0;

    printf("\n Enter the password : \n");
    gets(buff);

    if (strcmp(buff, "12")) {
        printf ("\n Wrong Password \n");
    } else {
        printf ("\n Correct Password \n");
        pass = 1;
    }

    if (pass==1) {
        printf ("\n Root privileges given to the user \n");
    }

    return 0;
}
