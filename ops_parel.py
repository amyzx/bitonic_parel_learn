#!/usr/bin/python3
import multiprocessing
import sys
import os 
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../../')))
import time
from multiprocessing import Pool
import torch
import math
from itertools import chain
from common import build_fpath
import sys
import os 
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../../')))
import crypten
import crypten.mpc as mpc
import crypten.communicator as comm 

# 启动多进程
def wrapper(tid):
    cmd = 'python3 ops_enc_wrapper.py %s ' % (str(tid)) 
    os.system(cmd)

# 进程池
def parallel(num_thread):
    with Pool(processes=num_thread) as pool:
        for tid in range(num_thread): 
            pool.apply_async(wrapper, (tid,))
        pool.close()
        pool.join()
  
# 密文排序入口
@mpc.run_multiprocess(world_size=2)
def bitonic_sort(arr1, arr2 = None, isAsc = True):  
    arr1 = crypten.cryptensor(arr1) 
    num_thread = multiprocessing.cpu_count()
    num_paras = len(arr1[0])
    if num_paras < num_thread:
        num_thread = num_paras
 
    num_each_part = int(num_paras / num_thread) 
    
    for tid in range(num_thread):   
        # 划分每一部分
        if tid < num_thread - 1:
            part_data = arr1[:, tid * num_each_part : (tid + 1)* num_each_part]
        else: 
            part_data = arr1[:, tid * num_each_part : ]
        
        split_array = torch.stack(list(chain.from_iterable(part_data._tensor._tensor)))
    
        torch.save(split_array, build_fpath(tid, comm.get().get_rank()))
    
 

def run_test(func, runtimes):
    times = []
    final = 0
    for i in range(runtimes):
        start = time.time()
        func()
        end = time.time()
        times.append(end - start)
    for t in times:
        final += t
    final /= float(runtimes)
    print("Run Time: %f" % (final))


if __name__ == '__main__': 
    data = torch.rand(4, 10) 
    print(data)
    print(torch.sort(data, dim=0)[0])
    bitonic_sort(data)
    parallel(10)
    result = []
    for tid in range(10):
        result.append(torch.load(build_fpath(tid, None, "user")))
    result = torch.stack(result, dim = 1)
    print("enc ", result)
