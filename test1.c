#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAXSIZE 100

typedef struct {
    char data[MAXSIZE]
    int top;
}Opstack;

void initStack(Opstack *s) {
    s->top=-1;
}

void initNumberStack(Opstack *s){
    s->top=-1;
}

void OpstackEmpty(Opstack *s){
    return s->top==-1;
}

void NumberStackEmpty(Opstack *s){
    return s->top==-1
}

void PushOp(Opstack *s, char c){
    s->data[++s->top] =  c;
}

char PopOp(Opstack *s){
    return s->data[s->top--];
}

char GetTopOp(Opstack *s){
    return s->data[s->top];
}

void PushNum(NumStack *s, int num) {
    s->data[++s->top] = num;
}

int PopNum(NumStack *s) {
    return s->data[s->top--];
}

int GetTopNum(NumStack *s) {
    return s->data[s->top];
}

int IsOperator(char c) {
    return c == '+' || c == '-' || c == '*' || c == '/' || c == '(' || c == ')' || c == '#';
}

int Priority(char op) {
    switch (op) {
        case '#': return 0;
        case '(': return 1;
        case '+':
        case '-': return 2;
        case '*':
        case '/': return 3;
        case ')': return 4;
        default: return -1;
    }
}

int ComparePriority(char op1, char op2) {
    int p1 = Priority(op1);
    int p2 = Priority(op2);
    if (p1 > p2) return 1;
    else if (p1 == p2) return 0;
    else return -1;
}

int Calculate(int a, char op, int b) {
    switch (op) {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        case '/': 
            if (b == 0) {
                printf("\n错误：除数不能为0！\n");
                exit(1);
            }
            return a / b;
        default: return 0;
    }
}

void PrintStack(OpStack *opStack, NumStack *numStack, char currChar, char *operation) {
    printf("当前字符: %c\t操作: %s\n", currChar, operation);
    printf("运算符栈: ");
    for (int i = 0; i <= opStack->top; i++) {
        printf("%c ", opStack->data[i]);
    }
    printf("\n运算数栈: ");
    for (int i = 0; i <= numStack->top; i++) {
        printf("%d ", numStack->data[i]);
    }
    printf("\n----------------------------------------\n");
}

int ExpressionEvaluate(char *exp) {
    OpStack opStack;  // 运算符栈
    NumStack numStack;// 运算数栈
    InitOpStack(&opStack);
    InitNumStack(&numStack);
    
    PushOp(&opStack, '#');  // 栈底放入#作为结束标志
    PrintStack(&opStack, &numStack, '#', "初始化栈，压入#");
    
    int i = 0;
    int len = strlen(exp);
    while (i < len || GetTopOp(&opStack) != '#') {
        char c = exp[i];
        
        if (c == ' ') {
            i++;
            continue;
        }
        
        if (isdigit(c)) {
            int num = 0;
            while (i < len && isdigit(exp[i])) {
                num = num * 10 + (exp[i] - '0');
                i++;
            }
            PushNum(&numStack, num);
            PrintStack(&opStack, &numStack, num + '0', "数字入数栈");
            continue;
        }
        

        if (IsOperator(c)) {
            char topOp = GetTopOp(&opStack);
            int cmp = ComparePriority(topOp, c);
            
            if (cmp < 0 || c == '(') { 
                PushOp(&opStack, c);
                PrintStack(&opStack, &numStack, c, "运算符入栈");
                i++;
            } else if (cmp == 0) { 
                PopOp(&opStack);
                PrintStack(&opStack, &numStack, c, "弹出左括号");
                i++;
            } else { 
                char op = PopOp(&opStack);
                int b = PopNum(&numStack);
                int a = PopNum(&numStack);
                int res = Calculate(a, op, b);
                PushNum(&numStack, res);
                PrintStack(&opStack, &numStack, op, "计算并将结果入数栈");
            }
        }
    }
    
    int result = GetTopNum(&numStack);
    printf("\n表达式计算结果: %d\n", result);
    return result;
}

int main() {
    char exp[MAXSIZE];
    printf("========================================\n");
    printf("      算术表达式求值演示（算符优先法）\n");
    printf("========================================\n");
    printf("请输入一个整型算术表达式(不含变量): ");
    fgets(exp, MAXSIZE, stdin);  
    exp[strcspn(exp, "\n")] = 0;
    
    printf("\n======= 计算过程演示 =======\n");
    ExpressionEvaluate(exp);
    
    return 0;
}