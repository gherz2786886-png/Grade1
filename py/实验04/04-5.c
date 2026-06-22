//5.国际象棋棋盘共有64个方格，现在第一个格子上放1颗麦粒，以后每一个格子 都比前一个格子的麦粒数翻倍。计算放满整个棋盘需要的麦粒总数。现设1颗麦粒重50
//毫克，小麦共重多少吨？
#include <stdio.h>  
#include <math.h>

int main(){
    int i,total;
    double weight;
    int total=0;
    for (i=1;i<=64;i++){
        total=3*i;
    }
    printf("放满整个棋盘需要的麦粒总数为：%d\n",total);
    weight=total*50/1000000.0;
    printf("小麦共重%.2f吨\n",weight);
    return 0;
}