#include <stdio.h>
#include <stdbool.h>

// ====================== 第一部分：判断闰年的函数 ======================
bool is_leap_year(int year) {
    // 满足条件返回 true（是闰年），不满足返回 false（不是）
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
}

// ====================== 第二部分：主函数（调用 + 输出） ======================
int main() {
    printf("2000 年到 3000 年之间的闰年有：\n");

    // 循环 2000 ~ 3000
    for (int year = 2000; year <= 3000; year++) {
        // 调用函数判断
        if (is_leap_year(year)) {
            printf("%d ", year);
        }
    }
    printf("\n");  // 换行

    return 0;
}