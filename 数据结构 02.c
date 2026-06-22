/*二、实验项目 1--线性表实现及应用
【实验目标】
掌握顺序表的类型定义和基本运算;掌握单链表的类型定义和基本运算;能够用线性表求解实际问题。
【实验任务】
结构进行实现。
【实验重点难点】
重点：基于顺序表或链式表的算法实现。
难点：循环链表的建立和删除操作。
【提交要求】
每位同学按要求完成实验任务，提交 (1) 基础性实验报告单 (docx 文档);(2) 实验相关的所有程序文件。
第 2 页共 11 页*/
#include <stdio.h>
#include <stdlib.h> 
#define MAXSIZE 100
typedef struct {
    int data [MAXSIZE];
    int length;
} SqList;
void initlist(SqList *L){
    L->length=0;    
} 
int listinsert(SqList *L,int i,int e){
    if (i<1 || i>L->length+1 || L->length==MAXSIZE) return 0;
    for (int j=L->length;j>=i;j--){     
        L->data[j]=L->data[j-1];
    }       
    L->data[i-1]=e;
    L->length++;            
    return 1;
}