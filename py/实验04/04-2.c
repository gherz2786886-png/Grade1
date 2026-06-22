#include <stdio.h>

int is_leap_year(int year) {
    // 满足条件返回1（是闰年），不满足返回0（不是）
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
}

int main() {
    int year;
    printf("2000年到3000年之间的闰年有：\n");
    for (year = 2000; year <= 3000; year++) {
        if (is_leap_year(year)) {
            printf("%d ", year);
        }
    }
    printf("\n");
    return 0;
}