# coding: utf-8
import sys
import os
import time
import matplotlib.pyplot as plt
import numpy

sys.path.append('..')
from common import config
# GPUで実行する場合は下記のコメントアウトを消去（要cupy）
# ==============================================
config.GPU = True  # 设置为True使用GPU，False使用CPU
# ==============================================

from common.np import *  # 在设置config.GPU之后导入np
from common.util import to_gpu, eval_perplexity, clip_grads
from common.optimizer import SGD
from common.trainer import RnnlmTrainer
from dataset import ptb
from better_rnnlm import BetterRnnlm

# 根据平台类型创建结果目录
result_dir = 'results/gpu' if config.GPU else 'results/cpu'
os.makedirs(result_dir, exist_ok=True)

# ハイパーパラメータの設定
batch_size = 20
wordvec_size = 650
hidden_size = 650
time_size = 35
lr = 20.0
max_epoch = 1
max_grad = 0.25
dropout = 0.5

# 学習データの読み込み
corpus, word_to_id, id_to_word = ptb.load_data('train')
corpus_val, _, _ = ptb.load_data('val')
corpus_test, _, _ = ptb.load_data('test')

if config.GPU:
    corpus = to_gpu(corpus)
    corpus_val = to_gpu(corpus_val)
    corpus_test = to_gpu(corpus_test)

vocab_size = len(word_to_id)
xs = corpus[:-1]
ts = corpus[1:]

model = BetterRnnlm(vocab_size, wordvec_size, hidden_size, dropout)
optimizer = SGD(lr)
trainer = RnnlmTrainer(model, optimizer)

# 用于记录训练过程中的指标
train_losses = []
valid_ppls = []
best_ppl = float('inf')

print('Start training...')
start_time = time.time()

# 计算总迭代次数
data_size = len(xs)
max_iters = data_size // (batch_size * time_size)

for epoch in range(max_epoch):
    epoch_start_time = time.time()
    epoch_losses = []
    
    # 训练一个epoch
    for iter in range(max_iters):
        # 获取当前批次的数据
        batch_x = xs[iter*batch_size*time_size : (iter+1)*batch_size*time_size]
        batch_t = ts[iter*batch_size*time_size : (iter+1)*batch_size*time_size]
        batch_x = batch_x.reshape(batch_size, time_size)
        batch_t = batch_t.reshape(batch_size, time_size)
        
        # 计算损失
        loss = model.forward(batch_x, batch_t)
        model.backward()
        params, grads = model.params, model.grads
        if max_grad is not None:
            clip_grads(grads, max_grad)
        optimizer.update(params, grads)
        
        # 记录损失
        loss_value = float(loss)  # 转换为Python标量
        train_losses.append(loss_value)
        epoch_losses.append(loss_value)
        
        # 每20次迭代显示一次进度
        if (iter + 1) % 20 == 0:
            elapsed_time = time.time() - epoch_start_time
            avg_loss = sum(epoch_losses[-20:]) / len(epoch_losses[-20:])  # 使用Python内置函数计算平均值
            perplexity = np.exp(avg_loss)
            print(f'| epoch {epoch+1} | iter {iter+1:4d} / {max_iters} | time {int(elapsed_time)}[s] | loss {avg_loss:.3f} | perplexity {perplexity:.2f}')
    
    # 评估验证集
    model.reset_state()
    ppl = eval_perplexity(model, corpus_val)
    valid_ppls.append(float(ppl))  # 确保存储为Python标量
    print(f'Valid perplexity: {ppl:.2f}')
    
    # 保存最佳模型
    if best_ppl > ppl:
        best_ppl = ppl
        model.save_params()
        print('Best model saved!')
    else:
        lr /= 4.0
        optimizer.lr = lr
        print(f'Learning rate reduced to {lr:.2f}')
    
    model.reset_state()
    print('-' * 50)

# 计算总训练时间
training_time = time.time() - start_time
print(f'\nTraining completed in {training_time:.2f} seconds')

# 测试集评估
model.reset_state()
ppl_test = eval_perplexity(model, corpus_test)
print(f'Test perplexity: {ppl_test:.2f}')

# 将数据转换为绘图用的数组
if config.GPU:
    # GPU模式下需要转换为NumPy数组
    train_losses_np = numpy.array(train_losses)
    valid_ppls_np = numpy.array(valid_ppls)
else:
    # CPU模式下直接使用
    train_losses_np = train_losses
    valid_ppls_np = valid_ppls

# 打印数据统计信息用于调试
print("\nData statistics for plotting:")
print(f"Training losses: min={min(train_losses_np):.3f}, max={max(train_losses_np):.3f}, len={len(train_losses_np)}")
print(f"Validation perplexities: min={min(valid_ppls_np):.3f}, max={max(valid_ppls_np):.3f}, len={len(valid_ppls_np)}")

# 绘制训练曲线
plt.figure(figsize=(15, 5))

# 绘制训练损失
plt.subplot(1, 2, 1)
x_train = numpy.arange(len(train_losses_np))
plt.plot(x_train, train_losses_np, 'b-', label='Training Loss')
plt.title('Training Loss Over Time')
plt.xlabel('Iterations')
plt.ylabel('Loss')
plt.grid(True)
plt.legend()

# 绘制验证集困惑度
plt.subplot(1, 2, 2)
x_valid = numpy.arange(len(valid_ppls_np))
plt.plot(x_valid, valid_ppls_np, 'r-', label='Validation PPL', linewidth=2, marker='o')
plt.title('Validation Perplexity Over Time')
plt.xlabel('Epochs')
plt.ylabel('Perplexity')
plt.grid(True)
plt.legend()

# 调整布局并保存
plt.tight_layout()
plt.savefig(os.path.join(result_dir, 'training_curves.png'), dpi=300, bbox_inches='tight')
print(f'Training curves saved to {os.path.join(result_dir, "training_curves.png")}')

# 同时保存训练数据到文本文件以便后续分析
with open(os.path.join(result_dir, 'training_data.txt'), 'w') as f:
    f.write('Iteration\tTraining Loss\n')
    for i, loss in enumerate(train_losses_np):
        f.write(f'{i}\t{loss}\n')
    f.write('\nEpoch\tValidation Perplexity\n')
    for i, ppl in enumerate(valid_ppls_np):
        f.write(f'{i}\t{ppl}\n')

# 保存训练结果到文件
with open(os.path.join(result_dir, 'training_results.txt'), 'w') as f:
    f.write(f'Training Configuration:\n')
    f.write(f'Platform: {"GPU" if config.GPU else "CPU"}\n')
    f.write(f'Batch size: {batch_size}\n')
    f.write(f'Word vector size: {wordvec_size}\n')
    f.write(f'Hidden size: {hidden_size}\n')
    f.write(f'Learning rate: {lr}\n')
    f.write(f'Dropout: {dropout}\n')
    f.write(f'Max gradient: {max_grad}\n')
    f.write(f'\nResults:\n')
    f.write(f'Best validation perplexity: {best_ppl:.2f}\n')
    f.write(f'Test perplexity: {ppl_test:.2f}\n')
    f.write(f'Training time: {training_time:.2f} seconds\n')

print(f'Training results saved to {os.path.join(result_dir, "training_results.txt")}')
