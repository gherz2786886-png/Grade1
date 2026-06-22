import jieba 
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt 

with open('小说 无限轮回.md','r',encoding='utf-8') as f:
    text = f.read()
    stop_words = set(f.read().splitlines())

words = jieba.lcut(text)
filter_words = [w for w in words if len(w) > 1 and w not in stop_words]

word_count = Counter(filter_words)
print("词频统计结果：")
for word, cnt in word_count.most_common(): 
    print(f"{word}: {cnt}次")

cloud_text = " ".join(filter_words)
wc = WordCloud(
    font_path="simhei.ttf",
    width=800, height=500,
    background_color="white",
    max_words=100
)

wc.generate(cloud_text)
plt.figure(figsize=(10,6))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")  
plt.show()
wc.to_file("词云图.png")