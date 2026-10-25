#include <stdio.h>

int isArmstrong(int number) {
    int original = number;
    int sum = 0;
    int digits = 0;
    int temp = number;

    while (temp != 0) {
        digits++;
        temp /= 10;
    }

    temp = number;

    while (temp > 0) {
        int digit = temp % 10;
        int power = 1;

        for (int i = 0; i < digits; i++) {
            power *= digit;
        }

        sum += power;
        temp /= 10;
    }

    // Bug: compares against the modified value
    return sum == temp;
}

int main() {
    int number;

    printf("Enter a number: ");
    scanf("%d", &number);

    if (isArmstrong(number)) {
        printf("Armstrong number\n");
    } else {
        printf("Not an Armstrong number\n");
    }

    return 0;
}
