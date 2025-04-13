# coding: utf-8
from common.config import GPU

if GPU:
    import cupy as np
    import cupyx
    print('GPU available')

    np.cuda.set_allocator(np.cuda.MemoryPool().malloc)
    print('\033[92m' + '-' * 60 + '\033[0m')
    print(' ' * 23 + '\033[92mGPU Mode (cupy)\033[0m')
    print('\033[92m' + '-' * 60 + '\033[0m\n')
else:
    import numpy as np
    import numpy as cupyx  # 在CPU模式下，cupyx使用numpy
    print('Use numpy')
    print('\033[92m' + '-' * 60 + '\033[0m')
    print(' ' * 23 + '\033[92mCPU Mode (numpy)\033[0m')
    print('\033[92m' + '-' * 60 + '\033[0m\n')
