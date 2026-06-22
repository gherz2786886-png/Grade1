/*（1）先根帮输入的 带空树标记的先序序列建立二叉树的链式存储结构；
（2）分别求出并输出该二叉树的先序、中序和后序遍历序列；
（3）设计并实现 计算树高度的算法。*/
#include <stdio.h>
#include <stdlib.h>

typedef struct BiTNode {
    char data;
    struct BiTNode *lchild;
    struct BiTNode *rchild;
} BiTNode, *BiTree;

int index = 0;// doubao:全局变量：用于读取先序序列（带空树标记'#'

void CreateBiTree(BiTNode *T ,char pre[], char null_mark){
    char ch = pre[index++];
    if (ch == null_mark){
        *T = NULL;
    }else{
    *T = (BiTNode)malloc(sizeof(BiTNode));
    (*T)->data = ch;
    CreateBiTree(&(*T)->lchild, pre, null_mark);
    CreateBiTree(&(*T)->rchild, pre, null_mark);
    }
}

void PreOrderTraverse(BiTree T) {
    if (T) {
        printf("%c ", T->data);
        PreOrderTraverse(T->lchild);
        PreOrderTraverse(T->rchild);
    }
}

void InOrderTraverse(BiTree T){
    if (T) {
        InOrderTraverse(T->lchild);
        printf("%c ", T->data);
        InOrderTraverse(T->rchild);
    }
}

void PostOrderTraverse(BiTree T) {
    if (T) {
        PostOrderTraverse(T->lchild);
        PostOrderTraverse(T->rchild);
        printf("%c ", T->data);
    }
}

int TreeHeight(BiTree T) {
    if (T == NULL) {
        return 0; // 空树高度为0
    } else {
        // 左、右子树高度的较大值 + 1（当前结点高度）
        int leftHeight = TreeHeight(T->lchild);
        int rightHeight = TreeHeight(T->rchild);
        return (leftHeight > rightHeight ? leftHeight : rightHeight) + 1;
    }
}

int main() {
    BiTree T;
    char pre[100]; // 存储带空树标记的先序序列
    char null_mark = '#'; // 空树标记，可根据题目修改
    
    printf("请输入带空树标记的先序序列（如 AB#D##C##）：\n");
    scanf("%s", pre);
    
    // 重置索引，创建二叉树
    index = 0;
    CreateBiTree(&T, pre, null_mark);
    
    printf("\n先序遍历序列：");
    PreOrderTraverse(T);
    printf("\n");
    
    printf("中序遍历序列：");
    InOrderTraverse(T);
    printf("\n");
    
    printf("后序遍历序列：");
    PostOrderTraverse(T);
    printf("\n");
    
    printf("二叉树的高度为：%d\n", TreeHeight(T));
    
    return 0;
}


 