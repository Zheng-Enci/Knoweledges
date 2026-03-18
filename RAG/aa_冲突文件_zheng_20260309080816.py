from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba

# 准备文档集合
documents = [
    "机器学习是人工智能的重要分支",
    "深度学习是机器学习的一种",
    "人工智能和机器学习发展迅速"
]

# 使用jieba进行中文分词
def chinese_tokenizer(text):
    return list(jieba.cut(text))

# 创建TfidfVectorizer对象，使用自定义分词器
vectorizer = TfidfVectorizer(tokenizer=chinese_tokenizer)

# 计算TF-IDF矩阵
tfidf_matrix = vectorizer.fit_transform(documents)

# 用户查询
query = "机器学习算法"

# 计算查询的TF-IDF向量
query_vector = vectorizer.transform([query])

# 计算查询与文档的相似度
similarities = cosine_similarity(query_vector, tfidf_matrix)

# 打印相似度结果
for i, similarity in enumerate(similarities[0]):
    print(f"文档{i+1}的相似度：{similarity:.4f}")