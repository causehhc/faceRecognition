# 输入图像大小
image_size = 160
# graph存储位置
graph_dir = '../data/graph/'
# 模型存储位置
model_dir = '../data/model/'
# 验证集所占比例
validation_set_split_ratio = 0.05
# 一个类别至少含有图片数量
min_nrof_val_images_per_class = 0.0
# 数据存放位置
data_dir = '../data/dataSet/CASIA-WebFace'

# TODO
# batch_size = 90
batch_size = 45
# dropout的保留率
keep_probability = 0.8
# 网络输出层维度
embedding_size = 512
# l2权值正则
weight_decay = 5e-4
# center_loss的center更新参数
center_loss_alfa = 0.6
# center_loss占比
center_loss_factor = 1e-2
# 初始学习率
learning_rate = 0.01
# 学习率衰减epoch数
# 学习率减少的迭代次数
LR_EPOCH = [10, 20, 40]
# 学习率衰减率
learning_rate_decay_factor = 0.98
# 指数衰减参数
moving_average_decay = 0.999
# 训练最大epoch
max_nrof_epochs = 150
