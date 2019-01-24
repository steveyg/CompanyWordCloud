from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time
def draw(f,filename):
    wordcloud = WordCloud(
        background_color="white",
        font_path="simhei.ttf",
        width=1280,
        height=720,
        margin=10,
        collocations=False
    ).generate(f)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    wordcloud.to_file('result/'+filename+'-'+str(int(time.time()))+'.png')
