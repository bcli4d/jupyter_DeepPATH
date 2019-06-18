import os
from os.path import join
def completed_batches(intermediate_checkpoints, pretrained_checkpoints): 
    if os.listdir(pretrained_checkpoints) == []: 
        last_batch = 0 
    else: 
        last_batch = sorted([int( f.split('_')[1].split('.')[0]) for f in os.listdir(pretrained_checkpoints)])[-1] 
    with open(join(intermediate_checkpoints,'checkpoint')) as f:  
        checkpoint_path = f.readline().split('"')[1] 
    completed = str(last_batch + int(checkpoint_path.split('-')[-1])) 
    return completed 
