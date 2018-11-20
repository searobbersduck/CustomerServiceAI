import jieba
from gensim import corpora, models, similarities
import pickle

q = ["你好，在吗？",
     "可以货到付款吗?",
     "包邮吗？",
     "产品什么材质面料，组成成分?",
     "我身高XX ，体重XX 的，应该穿什么尺码？",
     "发什么快递？",
     "可以发顺丰或邮政吗？",
     "我怎么补邮费呢？",
     "可以发其他快递吗？",
     "你们的产品有色差吗？",
     "如果不满意，可以退货吗？",
     "退换货邮费谁负责？",
     "能不能便宜一点或者送礼品?",
     "什么时候发货？",
     "几天能到？",
     "么么哒"
     ]
a = ["在的，亲，欢迎您光临“XX官方旗舰店”，我是售前客服小智，请问有什么可以帮助您？",
     "亲，不好意思，，本店暂时还没有开货到付款的服务。但是亲不用担心的，现在京东支付方式是非常很多的，而且支付也很方便安全的。现有支付方式：信用卡，网银，快捷支付都是行的。",
     "亲，您好，我们全国大部分地区是包邮的，但是部分偏远地区(新疆、西藏、青海、甘肃、内蒙等) 是不包邮, 不知亲是哪个地方的？",
     "亲，本产品是由30%的亚麻，48%的粘胶 12%的聚酯纤维组成。亚麻面料 夏季清凉，聚酯纤维亲肤透气，韩版修身，穿这款衣服既帅气又舒适。",
     "an01",
     "我们是默认发汇通和中通的哦。",
     "可以的，但是由于顺丰/邮政收费比普通快递要高，您如果要发顺丰/邮政 要补一定的快递费用的。",
     "请您稍等一下，我把补邮链接发给你http://item.jd.com/1037266211.html（补邮链接金额为1元，也就是说你这边要补多少元，数量选择多少个就行）。",
     "你好，亲这边目前收什么快递方便呢？我帮您看一下我们是否可以发。",
     "亲，请您放心，我们是官方正品，没有什么色差的哦，我们有针对200位客户做过售后调查, 根据收到货的客户反映都是可以接受的，不会影响您的穿着，请您放心选购，按照你喜欢的颜色进行选购就可以了。",
     "只要不影响我们二次销售的情况下 我们都是支持七天无理由退换货的 所以请你放心购买。",
     "亲，如果是产品质量问题我们承担来回邮费。如果不是产品质量问题（如尺码，颜色不合适等因客户个人喜好的问题造成的退换货）运费需要客户自己承担的。",
     "亲，不好意思，产品微利已近成本价销售，是不送小礼品/不议价的哦，请您谅解。",
     "您好，我们是根据店铺订单量的多少来确定的。正常情况16：00之前付款的，当天都可以发货的。订单量多或者其他特殊情况则是次日发货的。",
     "亲，发货后江浙沪1-2天左右到货，其他地区3-5天左右到货的。",
     "啪啪啪"]

qcut = []
for i in q:
    data1 = ""
    this_data = jieba.cut(i)
    for item in this_data:
        data1 += item + " "
    qcut.append(data1)

docs = qcut

# w1_list = []
# for doc in docs:
#      for w1 in doc.split():
#           print(w1)
#      w1_list.append([w1 for w1 in doc.split()])

tall = [[w1 for w1 in doc.split()] for doc in docs]

# corpora.Dictionary()
# 将二维数组转为字典
dictionary = corpora.Dictionary(tall)
# print(dictionary)
# for dic in dictionary:
#      print(dictionary[dic])

# gensim的doc2bow实现词袋模型
corpus = [dictionary.doc2bow(text) for text in tall]
# print(corpus)

# corpus是一个返回bow向量的迭代器。下面代码将完成对corpus中出现的每一个特征的IDF值的统计工作
tfidf = models.TfidfModel(corpus)
print(tfidf)

# 通过token2id得到特征数
num = len(dictionary.token2id.keys())
#稀疏矩阵相似度，从而建立索引
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=num)

'''
pickle提供了一个简单的持久化功能。可以将对象以文件的形式存放在磁盘上。
pickle模块只能在python中使用，python中几乎所有的数据类型（列表，字典，集合，类等）都可以用pickle来序列化，
pickle序列化后的数据，可读性差，人一般无法识别。
pickle.dump(obj, file, protocol)
序列化对象，并将结果数据流写入到文件对象中。参数protocol是序列化模式，默认值为0，表示以文本的形式序列化。protocol的值还可以是1或2，表示以二进制的形式序列化。
pickle.load(file)
反序列化对象。将文件中的数据解析为一个Python对象。
'''

fh = open("dictionary.pk", "wb")
pickle.dump(dictionary, fh)
fh.close()

fh = open("tfidf.pk", "wb")
pickle.dump(tfidf, fh)
fh.close()

fh = open("index.pk", "wb")
pickle.dump(index, fh)
fh.close()

fh = open("a.pk", "wb")
pickle.dump(a, fh)
fh.close()
