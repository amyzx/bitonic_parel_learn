import torch 
import sys
import os 
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../../')))
import crypten
import crypten.mpc as mpc
import crypten.communicator as comm 
from crypten.mpc import MPCTensor
from common import build_fpath
from ops_enc import bitonic_sort

# 专门负责多进程启动多个不同的crypten

@mpc.run_multiprocess(world_size=2)
def bitonic_parel(tid, userdata):
    rank = comm.get().get_rank() 
    crypto_data = MPCTensor.from_shares(userdata[rank]) 
    length = len(crypto_data)
    bitonic_sort(crypto_data, 0, length, None, True)
    result = crypto_data.get_plain_text()
    if rank == 0:
        torch.save(result, build_fpath(tid, None, "user"))

tid = int(sys.argv[1])                          
userdata = [torch.load(build_fpath(tid, 0)), torch.load(build_fpath(tid, 1))] 
 
crypten.init()                                  # initialize crypten for each instance
bitonic_parel(tid, userdata)
crypten.uninit()
