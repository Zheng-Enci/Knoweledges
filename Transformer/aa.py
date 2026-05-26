import torch.nn as nn

d_model = 512                                           # 模型维度

# 带偏置的 QKV 投影
qkv_with_bias = nn.Linear(d_model, 3 * d_model, bias=True)   # 参数量：512×1536 + 1536 = 787,968
print(f"带偏置参数量: {qkv_with_bias.weight.numel() + qkv_with_bias.bias.numel()}")  # 打印总参数量

# 无偏置的 QKV 投影
qkv_without_bias = nn.Linear(d_model, 3 * d_model, bias=False)  # 参数量：512×1536 = 786,432
print(f"无偏置参数量: {qkv_without_bias.weight.numel()}")        # 打印总参数量

# 节省的参数量
saved_params = qkv_with_bias.bias.numel()                      # 节省：1536 个参数
print(f"节省参数量: {saved_params}")                           # 打印节省的参数