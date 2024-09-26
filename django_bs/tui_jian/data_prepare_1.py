import pandas as pd
import numpy as np
import tensorflow as tf

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# 加载文件和查看文件
ratings_df = pd.read_csv('final_film_review1.csv')
# print(ratings_df.tail())
movies_df = pd.read_csv('unique_movies10.csv')
# print(movies_df.tail())

# 添加行号信息：因为movies表中的movieID远大于行号，如果使用movieID的最大值来构建评分表，那么评分表是一个非常大的稀疏矩阵，浪费内存，所以使用行号标志电影
ratings_df['ratingRow'] = ratings_df.index
movies_df['movieRow'] = movies_df.index
# print(movies_df.tail())

'''
创建两个矩阵
1. 创建电影评分矩阵rating：用于记录每个用户对每个电影的评分
2. 创建用户是否评分矩阵record：如果评分是1，否则为0
'''

# 首先筛选movies_df中的特征
movies_df = movies_df[['movieRow', '电影ID', '电影名称']]

# 保存该处理后的数据
movies_df.to_csv('moviesProcessed.csv', index=False, header=True, encoding='utf-8')
# print(movies_df.tail())

# 将ratings_df中的movieId替换为行号
ratings_df = pd.merge(ratings_df, movies_df, on='电影ID')
# print(ratings_df.head())

# 筛选需要用到的特征
ratings_df = ratings_df[['movieRow', 'ratingRow', '评分']]
ratings_df.to_csv('ratingsProcessed.csv', index=False, header=True, encoding='utf-8')
# print(ratings_df.head())

# 1. 创建电影评分矩阵rating：用于记录每个用户对每个电影的评分
# 获取用户最大编号：作为rating矩阵中的列
userNo = ratings_df['ratingRow'].max()+1
# print(userNo)
# 获取电影最大编号：作为rating矩阵中的行
movieNo = ratings_df['movieRow'].max()+1

# 创建rating矩阵
# 全部初始化为0
rating = np.zeros((movieNo, userNo))
# 创建电影评分表：添入rating矩阵
flag = 0 # 记录处理进度
ratings_df_length = np.shape(ratings_df)[0] # ratings_df的样本个数

# 将ratings_df中的数据填写到rating中
for index, row in ratings_df.iterrows():
    rating[int(row['movieRow']), int(row['ratingRow'])] = row['评分'] # 将row中的评分rating，填入rating中的电影编号和用户编号
    flag += 1 # 处理完一行
    print('processed %d, %d left' % (flag, ratings_df_length-flag)) # 

# 2. 创建用户是否评分矩阵record：如果已经评分是1，否则为0
# 在电影评分表中，为0代表未评分
record = rating > 0
# 因为record中是布尔值组成的矩阵，将其转化为0和1
record = np.array(record, dtype=int)
print(record.shape)


# #################################构建模型##########################
# 对评分取值范围进行缩放
# 定义函数：接受两个参数：电影评分表，评分记录表
def normalizeRating (rating, record):
    m, n = rating.shape # m电影数，n用户数
    # 每个电影每个用户的评分平均值
    rating_mean = np.zeros((m, 1)) # 所有电影平均评分初始化为0
    # rating_norm = np.zeros((m, n)) # 保存处理之后的数据
    rating_norm = np.copy(rating)  # 初始化为原始评分数据的拷贝
    for i in range(m): # 将原始评分减去平均评分，将结果和平均评分返回
        idx = record[i, :] != 0 # 已评分的电影对应的用户下标
        rating_mean[i] = np.mean(rating[i, idx]) # 记录这些评分的平均值，第i部电影
        rating_norm[i, idx] -= rating_mean[i] # 原始评分减去评分的平均值
        # if i == 0:
        #     print(idx)
        #     print(rating[0, idx])
        #     print(rating_mean[0])
        #     print(rating_norm[0, idx])
    return rating_norm, rating_mean

rating_norm, rating_mean = normalizeRating(rating, record) # 结果提示有全0数据，需处理

rating_norm = np.nan_to_num(rating_norm) # 将nan数据转换为0
rating_mean = np.nan_to_num(rating_mean) # 将nan数据转换为0

# print(rating_norm[0, :])
# print(rating_mean[0])

num_features = 10 # 假设有10种类型的电影

# 初始化电影内容矩阵X，产生的每个参数都是随机数且正态分布
X_parameters = tf.Variable(tf.random.normal([movieNo, num_features], stddev=0.35))
# 初始化用户喜好矩阵Theta，产生的每个参数都是随机数且正态分布
Theta_parameters = tf.Variable(tf.random.normal([userNo, num_features], stddev=0.35))

# 创建 Adam 优化器
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)

# 定义损失函数
def compute_loss():
    pred = tf.matmul(X_parameters, Theta_parameters, transpose_b=True)
    loss = 1/2 * tf.reduce_sum(((pred - rating_norm) ** 2) * record) + 1/2 * (tf.reduce_sum(X_parameters ** 2) + tf.reduce_sum(Theta_parameters ** 2))
    return loss

# 定义训练步骤
@tf.function
def train_step():
    with tf.GradientTape() as tape:
        loss = compute_loss()
    gradients = tape.gradient(loss, [X_parameters, Theta_parameters])
    optimizer.apply_gradients(zip(gradients, [X_parameters, Theta_parameters]))
    return loss

# TensorBoard设置
log_dir = './movie_tensorboard'
summary_writer = tf.summary.create_file_writer(log_dir)

# 训练模型，训练次数5000
for epoch in range(5000):
    loss = train_step()
    with summary_writer.as_default():
        tf.summary.scalar('loss', loss, step=epoch)

    if epoch % 100 == 0:  # 每100次迭代输出一次损失
        print(f"Epoch {epoch + 1}, Loss: {loss.numpy()}")
print('模型训练成功！')

# 获取当前X和theta
Current_X_parameters = X_parameters.numpy()  # 直接获取X_parameters的numpy值
Current_Theta_parameters = Theta_parameters.numpy()  # 直接获取Theta_parameters的numpy值

# 将电影内容矩阵和用户喜好矩阵相乘，再加上每一行的均值，得到一个完整的电影评分表
# dot用于矩阵之间的乘法操作
predicts = np.dot(Current_X_parameters, Current_Theta_parameters.T) + rating_mean

print(predicts.shape)

# 计算预测值与真实值之间的算数平方根作为预测误差
errors = np.sqrt(np.sum((predicts - rating) ** 2))
print('预测误差:', errors)


# ########################################构建完整的电影推荐系统###########################
# 获取用户ID，并保存
user_id = input('您要向哪位用户进行推荐？请输入用户编号：')

# 获取对该用户电影评分的列表
# 预测出的用户对电影的评分，并从大到小排序
sortedResult = predicts[:, int(user_id)].argsort()[::-1]

# 向该用户推荐评分最高的20部电影
idx = 0 # 保存已经推荐了多少部电影
print('为该用户推荐的评分最高的20部电影是'.center(80, '='))

# 开始推荐
for i in sortedResult:
    print('评分：%.2f, 电影名：%s' % (predicts[i, int(user_id)], movies_df.iloc[i]['电影名称']))
    idx += 1 # 已经推荐的电影
    if idx == 20: break


# # 初始化电影内容矩阵X，产生的每个参数都是随机数且正态分布
# X_parameters = tf.Variable(tf.random.normal([movieNo, num_features], stddev=0.35))
# # 初始化用户喜好矩阵theta，产生的每个参数都是随机数且正态分布
# Theta_parameters = tf.Variable(tf.random.normal([userNo, num_features], stddev=0.35))
# # 定义代价函数loss：tf.reduce_sum求和，tf.matmul相乘，transpose_b=True转置b项，
# loss = 1/2 * tf.reduce_sum(((tf.matmul(X_parameters, Theta_parameters, transpose_b=True) - rating_norm) * record) ** 2) + 1/2 * (tf.reduce_sum(X_parameters ** 2) + tf.reduce_sum(Theta_parameters ** 2)) # 后面部分是正则化项，lambda为1，可以调整lambda来观察模型性能变化

# # 创建adam优化器和优化目标
# optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4) # 学习速率10^-4
# train = optimizer.minimize(loss) # 目标：最小化代价函数


# # ##########################################模型训练#####################################
# # 查看代价值随着迭代次数增加的变化情况
# # 使用tensorboard将整个训练可视化
# # tensorboard中tf.summary模块用于将tensorflow的数据导出，从而可视化

# # 由于需要可视化的loss值是标量，所以要用summary中的scalar
# tf.summary.scalar('loss', loss)

# # 将所有summary信息汇总
# summaryMerged = tf.summary.merge_all()

# # 保存信息的路径
# filename = './movie_tensorboard'
# # FileWriter用于把信息保存到文件中
# writer = tf.summary.FileWriter(filename)

# # 创建tensorflow会话
# sess = tf.Session()
# init = tf.global_variables_initializer()
# sess.run(init)

# # 训练模型，训练次数5000
# for i in range(5000):
#     _, movie_summary = sess.run([train, summaryMerged]) # 记录每次迭代的loss的变化，每次train训练的结果保存到_中
#     writer.add_summary(movie_summary, i) # 训练后保存数据，代价值随着迭代次数i的变化情况

# print('模型训练成功！')

# '''
# 查看代价值随着迭代次数的变化情况：
# 1. 打开cmd操作界面
# 2. 切换cd到保存数据的路径中
# 3. 运行：tensorboard --logdir=./
# 4. 浏览器中输入：127.0.0.1:6006
# 5. 可以看到代价值随着迭代次数的增加而减小
# '''


# # ######################################模型评估####################################
# # 测试不同的num_features的值，通过比较误差，判断哪个num_features的值最合适
# # 使用前面得到的参数，填满电影评分表

# # 获取当前X和theta
# Current_X_parameters, Current_Theta_parameters = sess.run([X_parameters, Theta_parameters])

# # 将电影内容矩阵和用户喜好矩阵相乘，再加上每一行的均值，得到一个完整的电影评分表
# # dot用于矩阵之间的乘法操作
# predicts = np.dot(Current_X_parameters, Current_Theta_parameters.T) + rating_mean

# # 计算预测值与真实值之间的算数平方根作为预测误差
# errors = np.sqrt(np.sum((predicts - rating)**2))
# errors


# # ########################################构建完整的电影推荐系统###########################
# # 获取用户ID，并保存
# user_id = input('您要向哪位用户进行推荐？请输入用户编号：')

# # 获取对该用户电影评分的列表
# # 预测出的用户对电影的评分，并从大到小排序
# sortedResult = predicts[:, int(user_id)].argsort()[::-1]

# # 向该用户推荐评分最高的20部电影
# idx = 0 # 保存已经推荐了多少部电影
# print('为该用户推荐的评分最高的20部电影是'.center(80, '='))

# # 开始推荐
# for i in sortedResult:
#     print('评分：%.2f, 电影名：%s' % (predicts[i, int(user_id)], movies_df.iloc[i]['电影名称']))
#     idx += 1 # 已经推荐的电影
#     if idx == 20: break