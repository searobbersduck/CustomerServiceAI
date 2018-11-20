# !/usr/bin/env python3

import jieba
from gensim import corpora, models, similarities

# choice_item = [
#                '不方便，在工作，稍等一会, 我不是很感兴趣, 能不能等会再打','方便, 好，可以聊一下，方便，感兴趣，挺好的，有什么事','不知道你说的啥']

choice_item = ['不方便','在工作','稍等一会','我不是很感兴趣', '能不能等会再打','方便', '好','可以聊一下','方便','感兴趣','挺好的','有什么事','不知道你说的啥']

choice_cut = []
for i in choice_item:
    data1 = ''
    this_data = jieba.cut(i)
    for item in this_data:
        data1 += item  + ' '
    choice_cut.append(data1)

docs = choice_cut

tall = [ [w1 for w1 in doc.split()] for doc in docs]

dictionary = corpora.Dictionary(tall)

corpus = [dictionary.doc2bow(text) for text in tall]

tfidf = models.TfidfModel(corpus)

print(tfidf)

num = len(dictionary.token2id.keys())

index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=num)

while True:
    choice_input = input('请问您现在方便吗?\n')
    in_data = jieba.cut(choice_input)
    new_doc = ''
    for d in in_data:
        new_doc += d + ' '
    new_vec = dictionary.doc2bow(new_doc.split())
    sim = index[tfidf[new_vec]]
    postion = sim.argsort()[-1]
    print(choice_item[postion])
    print('\n')