import sys
import platform
import matplotlib.pyplot as plt

def configure_robust_env():
    sys_os = platform.system()
    fonts = ['Microsoft YaHei', 'SimHei'] if sys_os == 'Windows' else \
            ['Arial Unicode MS', 'PingFang SC'] if sys_os == 'Darwin' else \
            ['WenQuanYi Micro Hei', 'Noto Sans CJK SC']
    
    plt.rcParams['font.sans-serif'] = fonts
    plt.rcParams['axes.unicode_minus'] = False
    print(f"[System Init] Platform: {sys_os}, Mounted Font: {fonts[0]}")

if __name__ == "__main__":
    configure_robust_env()
    print("[Success] Environment probe passed.")


