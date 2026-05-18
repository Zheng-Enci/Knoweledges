import torch
import math
import time


def compare_methods(d_model=512, num_runs=1000):
    """
    对比 pow 和 exp-log 两种方法的性能和稳定性
    
    参数:
        d_model: 模型维度
        num_runs: 重复次数（用于性能测试）
    """
    print(f"{'='*70}")
    print(f"对比测试：d_model = {d_model}, 重复 {num_runs} 次")
    print(f"{'='*70}")
    
    # 准备数据
    i = torch.arange(0, d_model, 2).float()
    
    # ========== 方法1：直接 pow ==========
    start_time = time.time()
    for _ in range(num_runs):
        result_pow = 1 / (10000 ** (i / d_model))
    time_pow = time.time() - start_time
    
    # 检查结果
    has_nan_pow = torch.isnan(result_pow).any()
    has_inf_pow = torch.isinf(result_pow).any()
    
    print(f"\n方法1：直接 pow")
    print(f"  耗时: {time_pow:.4f} 秒")
    print(f"  结果范围: [{result_pow.min():.6e}, {result_pow.max():.6e}]")
    print(f"  包含 NaN: {has_nan_pow}")
    print(f"  包含 Inf: {has_inf_pow}")
    
    # ========== 方法2：exp-log 转换 ==========
    start_time = time.time()
    for _ in range(num_runs):
        result_exp = torch.exp(i * (-math.log(10000.0) / d_model))
    time_exp = time.time() - start_time
    
    # 检查结果
    has_nan_exp = torch.isnan(result_exp).any()
    has_inf_exp = torch.isinf(result_exp).any()
    
    print(f"\n方法2：exp-log 转换")
    print(f"  耗时: {time_exp:.4f} 秒")
    print(f"  结果范围: [{result_exp.min():.6e}, {result_exp.max():.6e}]")
    print(f"  包含 NaN: {has_nan_exp}")
    print(f"  包含 Inf: {has_inf_exp}")
    
    # ========== 结果对比 ==========
    print(f"\n{'='*70}")
    print(f"结果对比")
    print(f"{'='*70}")
    
    diff = torch.abs(result_pow - result_exp)
    max_diff = diff.max()
    
    print(f"  最大差值: {max_diff:.6e}")
    print(f"  结果一致: {torch.allclose(result_pow, result_exp, rtol=1e-5)}")
    print(f"  速度比: {time_pow/time_exp:.2f}x")
    
    return result_pow, result_exp


def test_extreme_cases():
    """测试极端情况"""
    print(f"\n{'='*70}")
    print(f"极端情况测试")
    print(f"{'='*70}")
    
    # 测试超大 d_model
    for d_model in [8192, 16384, 32768]:
        print(f"\nd_model = {d_model}")
        
        i = torch.arange(0, d_model, 2).float()
        
        # pow 方法
        try:
            result_pow = 1 / (10000 ** (i / d_model))
            if torch.isinf(result_pow).any():
                print(f"  ❌ pow: 溢出 (inf)")
            elif torch.isnan(result_pow).any():
                print(f"  ❌ pow: NaN")
            else:
                print(f"  ✓ pow: 范围 [{result_pow.min():.2e}, {result_pow.max():.2e}]")
        except Exception as e:
            print(f"  ❌ pow: 异常 - {e}")
        
        # exp-log 方法
        try:
            result_exp = torch.exp(i * (-math.log(10000.0) / d_model))
            if torch.isinf(result_exp).any():
                print(f"  ❌ exp-log: 溢出 (inf)")
            elif torch.isnan(result_exp).any():
                print(f"  ❌ exp-log: NaN")
            else:
                print(f"  ✓ exp-log: 范围 [{result_exp.min():.2e}, {result_exp.max():.2e}]")
        except Exception as e:
            print(f"  ❌ exp-log: 异常 - {e}")


if __name__ == "__main__":
    # 标准测试
    compare_methods(d_model=512, num_runs=1000)
    
    # 极端情况测试
    test_extreme_cases()
