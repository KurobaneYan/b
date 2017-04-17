#include <stdio.h>

long calc_factorial(int n) {
    if (n < 0) {
        return -1;
    } else if (n == 0) {
        return 1;
    }

    return n * calc_factorial(n - 1);
}

int main() {
    int n = 0;
    int n;
    int t;
    char *c;

    setlinebuf(stdout);

    printf("how many times caculate factorial?");
    scanf("%d", &n);

    while(n) {
        printf("enter number\n");
        scanf("%d", &t);

        if (t > 18) {
            printf("factorial of %d is too big\n", t);
        } else {
            printf("factorial of %d is %ld\n", t, calc_factorial(t));
        }
        n--;
    }
    return 0;
}
