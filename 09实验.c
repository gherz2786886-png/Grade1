#include <stdio.h>
#include <string.h>

void get_next(char *t, int *next) {
    int i = 0, j = -1;
    next[0] = -1; /
    int len = strlen(t);
    
    while (i < len - 1) {
        if (j == -1 || t[i] == t[j]) {
            i++;
            j++;
            next[i] = j;
        } else {
            j = next[j]; 
        }
    }
}

int KMP(char *s, char *t) {
    int i = 0, j = 0;
    int s_len = strlen(s);
    int t_len = strlen(t);
    int next[100]; 

    get_next(t, next);

    printf("模式串 t 的 next 数组为: ");
    for (int k = 0; k < t_len; k++) {
        printf("%d ", next[k] + 1); 
    }
    printf("\n");
    // ----------------------------------

    while (i < s_len && j < t_len) {
        if (j == -1 || s[i] == t[j]) {
            i++;
            j++;
        } else {
            j = next[j];
    }

    if (j == t_len) {
        return i - j + 1; 
    } else {
        return 0; 
    }
}

int main() {
    char s[] = "abcaababcabaa";
    char t[] = "abcabaa";

    printf("主串 s = %s\n", s);
    printf("模式串 t = %s\n\n", t);

    int pos = KMP(s, t);
    
    if (pos > 0) {
        printf("\n=> 匹配成功！起始位置在主串的第 %d 个字符处。\n", pos);
    } else {
        printf("\n=> 匹配失败。\n");
    }

    return 0;
}