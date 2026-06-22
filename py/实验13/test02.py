import jieba.posseg as pseg
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1.读取正文文本
with open('小说 无限轮回.md','r',encoding='utf-8') as f:
    text = f.read()

# 自定义基础停用词（过滤无意义高频词）
stop_words = {"的", "了", "是", "在", "我", "他", "她", "就", "都", "而", "和", "有", "不", "一个", "这", "那"}

# 2.词性标注分词
words_tag = pseg.cut(text)
# 分三类空列表存放词汇
n_list = []  # 名词 n
v_list = []  # 动词 v
a_list = []  # 形容词 a

for word, tag in words_tag:
    w = word.strip()
    # 过滤单字、停用词
    if len(w) <= 1 or w in stop_words:
        continue
    # 按词性分类
    if tag.startswith('n'):  # 所有名词：nr人名、ns地名、nz专有名词等全部归入名词
        n_list.append(w)
    elif tag.startswith('v'): # 所有动词
        v_list.append(w)
    elif tag.startswith('a'): # 所有形容词
        a_list.append(w)

# 3.词频统计
count_n = Counter(n_list)
count_v = Counter(v_list)
count_a = Counter(a_list)

print("=====名词词频TOP20=====")
for k,v in count_n.most_common(20):
    print(f"{k}:{v}")
print("=====动词词频TOP20=====")
for k,v in count_v.most_common(20):
    print(f"{k}:{v}")
print("=====形容词词频TOP20=====")
for k,v in count_a.most_common(20):
    print(f"{k}:{v}")

# 4.封装词云生成函数（复用代码）
def create_wordcloud(word_list, save_name, title):
    if not word_list: # 避免空列表报错
        print(f"{title}词汇为空，跳过生成")
        return
    cloud_str = " ".join(word_list)
    wc = WordCloud(
        font_path="C:/Windows/Fonts/simhei.ttf", # Windows黑体全路径
        width=800, height=500,
        background_color="white",
        max_words=120
    )
    wc.generate(cloud_str)
    plt.figure(figsize=(10,5))
    plt.title(title, fontsize=14)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    wc.to_file(save_name)

# 分别生成三张词云
create_wordcloud(n_list, "名词词云.png", "名词词云图")
create_wordcloud(v_list, "动词词云.png", "动词词云图")
create_wordcloud(a_list, "形容词词云.png", "形容词词云图")