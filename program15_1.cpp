/* program8_1.c
 * 实验八 (8） EasyX是一个C/C++下的图形函数库，用它可以在控制台下进行绘图。安装并熟悉EasyX，为后续使用做好准备。
 * 要求：① 根据官网上的教程和说明，安装EasyX，使得以下代码能够运行。将代码运行结果截图显示。
 */

#include <graphics.h>
#include <conio.h>
#include<math.h>
const double PI=3.1415926;
const double div_count=360.0;
int main() {
    int i=0;
    initgraph(800, 800);
    setorigin( 400, 400);
    setaspectratio(1, -1); //建立笛卡尔坐标系
    line(-600, 0, 600, 0);
    line(0, -600, 0, 600);
    for (i=-360; i<=360; i++)
        putpixel(i, sin((PI/180.0)*(i*1.0))*60, GREEN);
    getch();    // 按任意键退出
    closegraph();
    return 0;
}
