#define MAXV 100
typedef struct {
    int vexs[MAXV];       
    int edges[MAXV][MAXV];
    int n, e;            
} MGraph;

void InsertVex(MGraph *G, int v) {
    if (G->n >= MAXV) return;
    G->vexs[G->n] = v;   
    for (int i = 0; i <= G->n; i++) {
        G->edges[G->n][i] = 0; 
        G->edges[i][G->n] = 0; 
    }
    G->n++; 
}