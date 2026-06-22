/*二、实验项目1--线性表实现及应用
【实验目标】
掌握顺序表的类型定义和基本运算;掌握单链表的类型定义和基本运算;能够用线性表求解实际问题。
【实验任务】
结构进行实现。
【实验重点难点】
重点:基于顺序表或链式表的算法实现。
难点:循环链表的建立和删除操作。
【提交要求】
每位同学按要求完成实验任务，提交(1)基础性实验报告单(docx文档);(2)实验相关的所有程序文件。
第2页共11页*/
#include <stdio.h>
#include <stdlib.h>

#define MAXSIZE 100  // 顺序表最大容量

// 1. 顺序表结构定义
typedef struct {
    int data[MAXSIZE];  // 数据存储数组
    int length;         // 当前元素个数
} SqList;

// 2. 初始化顺序表
void InitList(SqList *L) {
    L->length = 0;  // 初始长度为0
}

// 3. 插入元素（在第i个位置插入e）
int ListInsert(SqList *L, int i, int e) {
    // 合法性判断
    if (i < 1 || i > L->length + 1 || L->length >= MAXSIZE)
        return 0;  // 插入失败
    
    // 元素后移
    for (int j = L->length; j >= i; j--)
        L->data[j] = L->data[j - 1];
    
    L->data[i - 1] = e;  // 插入新元素
    L->length++;         // 长度+1
    return 1;
}

// 4. 删除元素（删除第i个元素，用e返回）
int ListDelete(SqList *L, int i, int *e) {
    if (i < 1 || i > L->length)
        return 0;  // 删除失败
    
    *e = L->data[i - 1];  // 保存被删除元素
    
    // 元素前移
    for (int j = i; j < L->length; j++)
        L->data[j - 1] = L->data[j];
    
    L->length--;
    return 1;
}

// 5. 查找元素（返回元素e的位置，不存在返回0）
int LocateElem(SqList L, int e) {
    for (int i = 0; i < L.length; i++) {
        if (L.data[i] == e)
            return i + 1;
    }
    return 0;
}

// 6. 遍历输出顺序表
void PrintList(SqList L) {
    for (int i = 0; i < L.length; i++)
        printf("%d ", L.data[i]);
    printf("\n");
}

// 测试主函数
int main() {
    SqList L;
    InitList(&L);
    
    // 插入测试
    ListInsert(&L, 1, 10);
    ListInsert(&L, 2, 20);
    ListInsert(&L, 3, 30);
    printf("插入后顺序表：");
    PrintList(L);  // 10 20 30
    
    // 删除测试
    int e;
    ListDelete(&L, 2, &e);
    printf("删除元素：%d\n", e);  // 20
    printf("删除后顺序表：");
    PrintList(L);  // 10 30
    
    // 查找测试
    int pos = LocateElem(L, 30);
    printf("元素30的位置：%d\n", pos);  // 2 
    
    return 0;
}