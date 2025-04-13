# 改进的RNNLM训练项目

## 系统环境
### 硬件配置
- GPU: NVIDIA RTX 4070 8GB
- CPU: AMD Ryzen 9 7945HX (16核32线程)

### 软件环境
- 操作系统：Windows 11 专业版 24H2
- CUDA版本：12.8
- CUDNN：已安装
- Python环境：Python3.12
- 工作目录：D:/t

## 依赖包
必需的Python包：
```bash
numpy>=1.21.0
matplotlib>=3.5.0
cupy>=12.0.0  # 适配CUDA 12.8版本
cudnn>=8.9.0  # 用于GPU加速
```

## 环境配置
1. 创建虚拟环境（推荐）：
```bash
# 使用venv
python -m venv .venv
.venv\Scripts\activate
注意项目不能包含任何中文路径

# 或使用conda
conda create -n rnnlm python=3.9
conda activate rnnlm
```

2. 安装依赖：
```bash
# 安装基本依赖
pip install -r requirements.txt

# 如果使用GPU，还需要安装CUDA工具包
# 请确保已安装对应版本的CUDA和cuDNN
```

### CUDA和cuDNN安装指南

1. CUDA安装：
   - 访问 [NVIDIA CUDA下载页面](https://developer.nvidia.com/cuda-downloads)
   - 选择Windows 11系统
   - 下载并安装CUDA 12.8版本
   - 安装时选择"自定义安装"，确保勾选以下组件：
     - CUDA Runtime
     - CUDA Development
     - CUDA Visual Studio Integration
     - CUDA Samples

2. cuDNN安装：
   - 访问 [NVIDIA cuDNN下载页面](https://developer.nvidia.com/cudnn)
   - 需要注册NVIDIA开发者账号
   - 下载与CUDA 12.8兼容的cuDNN 8.9.0版本
   - 解压下载的文件，将以下文件复制到CUDA安装目录：
     - `cudnn/bin/cudnn*.dll` → `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\bin`
     - `cudnn/include/cudnn*.h` → `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\include`
     - `cudnn/lib/cudnn*.lib` → `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\lib\x64`

3. 环境变量配置：
   - 确保以下路径已添加到系统环境变量PATH中：
     ```
     C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\bin
     C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\libnvvp
     ```

4. 验证安装：
   ```bash
   # 检查CUDA版本
   nvidia-smi
   nvcc --version
   
   # 检查GPU是否可用
   python -c "import cupy; print('GPU可用:', cupy.cuda.is_available())"
   ```

5. 常见问题解决：
   - 如果遇到"找不到cudnn64_8.dll"错误，检查cuDNN文件是否正确复制到CUDA目录
   - 如果GPU不可用，检查CUDA和cuDNN版本是否匹配
   - 确保NVIDIA显卡驱动是最新版本

3. 验证安装：
```python
python -c "import numpy; import cupy; import matplotlib; print('环境配置成功！')"
```

## 推荐配置
- NVIDIA GPU显存 >= 8GB
- CPU内存 >= 16GB
- 磁盘空间 >= 10GB（用于存储模型和训练结果）

## 项目结构
```
.
├── results/
│   ├── cpu/  # CPU训练结果
│   └── gpu/  # GPU训练结果
├── common/
│   ├── np.py
│   ├── util.py
│   ├── layers.py
│   └── time_layers.py
└── ch06/
    ├── train_better_rnnlm.py
    └── better_rnnlm.py
```

## 主要特性和改进

### 1. 平台特定输出
- 自动检测GPU/CPU平台
- 根据平台分别保存结果：
  - GPU结果：`results/gpu/`
  - CPU结果：`results/cpu/`

### 2. 训练可视化
- 实时训练进度显示：
  ```
  | epoch 1 | iter 20 / 1327 | time 2[s] | loss 6.753 | perplexity 856.32
  ```
- 生成训练曲线：
  - 训练损失随迭代变化
  - 验证困惑度随轮次变化

### 3. 数据管理
- CPU和GPU之间的自动数据类型转换
- 保存完整的训练数据：
  - `training_curves.png`：训练过程可视化图表
  - `training_data.txt`：原始训练指标
  - `training_results.txt`：配置和最终结果

### 4. 模型配置
```python
# 超参数设置
batch_size = 20      # 批次大小
wordvec_size = 650   # 词向量维度
hidden_size = 650    # 隐藏层大小
time_size = 35       # 时间步长
learning_rate = 20.0 # 学习率
max_epoch = 40       # 最大训练轮次
max_grad = 0.25      # 梯度裁剪阈值
dropout = 0.5        # dropout比率
```

## 使用方法

1. 在`train_better_rnnlm.py`中设置GPU/CPU模式：
```python
config.GPU = True   # 使用GPU训练
config.GPU = False  # 使用CPU训练
```

2. 运行训练：
```bash
python ch06/train_better_rnnlm.py
```

3. 结果保存位置：
- GPU模式：`results/gpu/`
- CPU模式：`results/cpu/`

## 输出文件说明

### 训练曲线 (`training_curves.png`)
- 左图：训练损失随迭代次数的变化
- 右图：验证集困惑度随训练轮次的变化

### 训练数据 (`training_data.txt`)
```
迭代次数    训练损失
1          7.324
2          6.892
...

训练轮次    验证集困惑度
1          856.32
2          543.21
...
```

### 训练结果 (`training_results.txt`)
```
训练配置：
运行平台：GPU/CPU
批次大小：20
词向量维度：650
隐藏层大小：650
学习率：20.0
Dropout比率：0.5
梯度裁剪阈值：0.25

训练结果：
最佳验证集困惑度：XXX.XX
测试集困惑度：XXX.XX
训练时间：XXX.XX秒
```

## 性能监控
- 实时跟踪损失值和困惑度
- 自动调整学习率
- 保存最佳模型检查点
- 训练时间测量

## 注意事项
- GPU训练需要安装CUDA和CuPy
- CPU训练只需要NumPy
- 每20次迭代保存一次训练进度
- 当验证性能下降时，学习率自动降为原来的1/4
- 所有结果会根据运行平台自动保存到对应目录

## 更新日志
- 添加了GPU/CPU平台自动检测
- 实现了训练过程的实时可视化
- 优化了数据类型转换逻辑
- 改进了结果保存和组织方式
- 增加了详细的训练状态监控 