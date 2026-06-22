//输入三个整数，利用if语句配合数据交换实现从大到小的顺序输出（不能用sort排序）
#include <stdio.h>

int main() {
   int a, b , c, temp;
   printf("请输入三个整数，以空格分隔：");
   scanf("%d %d %d", &a, &b, &c);
   
     if (a < b) {
        temp = a;
        a = b;
        b = temp;   }
    if (a < c) {
        temp = a;   
        a = c;
        c = temp;   }   
    if (b < c) {
        temp = b;
        b = c;
        c = temp;   }
    printf("从大到小的顺序输出：%d %d %d\n", a, b, c);      
    


    
}