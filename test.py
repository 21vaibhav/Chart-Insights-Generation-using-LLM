import torch
import bitsandbytes as bnb

print(f"CUDA Available: {torch.cuda.is_available()}")
# Check if bitsandbytes can find the GPU libraries
from bitsandbytes.cextension import COMPILED_WITH_CUDA
print(f"BNB Compiled with CUDA: {COMPILED_WITH_CUDA}")