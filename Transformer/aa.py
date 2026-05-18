import torch
import math


def test_reciprocal_precision():
    """测试倒数计算的精度问题"""
    
    print("测试倒数计算的精度差异")
    print("="*70)
    
    # 测试小指数情况（这才是真正的问题所在）
    for exponent in [0.01, 0.001, 0.0001, 0.00001]:
        print(f"\n指数 = {exponent}")
        print("-"*70)
        
        # 方法1：先计算大数，再取倒数
        big_num = 10000 ** exponent
        result_pow = 1 / big_num
        
        # 方法2：直接计算负指数
        result_exp = math.exp(-exponent * math.log(10000))
        
        print(f"pow 方法：10000^{exponent} = {big_num:.10f}, 倒数 = {result_pow:.10e}")
        print(f"exp-log 方法：exp(-{exponent} × ln(10000)) = {result_exp:.10e}")
        print(f"差值：{abs(result_pow - result_exp):.2e}")


def test_extreme_d_model():
    """测试极端大的 d_model"""
    
    print("\n\n测试极端大的 d_model")
    print("="*70)
    
    # 当 d_model 非常大时
    for d_model in [10000, 50000, 100000]:
        print(f"\nd_model = {d_model}")
        print("-"*70)
        
        i = torch.arange(0, d_model, 2).float()
        exponent = 2 * i / d_model
        
        # 方法1：pow
        try:
            result_pow = 1 / (10000 ** exponent)
            print(f"✓ pow 方法：范围 [{result_pow.min():.2e}, {result_pow.max():.2e}]")
        except Exception as e:
            print(f"❌ pow 方法：异常 - {e}")
        
        # 方法2：exp-log
        try:
            result_exp = torch.exp(-exponent * math.log(10000))
            print(f"✓ exp-log 方法：范围 [{result_exp.min():.2e}, {result_exp.max():.2e}]")
        except Exception as e:
            print(f"❌ exp-log 方法：异常 - {e}")


def test_float16_stability():
    """测试 float16 下的数值稳定性"""
    
    print("\n\n测试 float16（半精度）下的数值稳定性")
    print("="*70)
    
    for d_model in [512, 1024, 2048]:
        print(f"\nd_model = {d_model}")
        print("-"*70)
        
        i = torch.arange(0, d_model, 2).float()
        exponent = 2 * i / d_model
        
        # 转换为 float16
        exponent_16 = exponent.half()
        
        # 方法1：pow (float16)
        try:
            result_pow_16 = 1 / (10000 ** exponent_16)
            has_inf = torch.isinf(result_pow_16).any()
            has_nan = torch.isnan(result_pow_16).any()
            if has_inf or has_nan:
                print(f"❌ pow 方法 (float16)：出现 inf={has_inf}, nan={has_nan}")
            else:
                print(f"✓ pow 方法 (float16)：范围 [{result_pow_16.min():.2e}, {result_pow_16.max():.2e}]")
        except Exception as e:
            print(f"❌ pow 方法 (float16)：异常 - {e}")
        
        # 方法2：exp-log (float16)
        try:
            result_exp_16 = torch.exp(-exponent_16 * math.log(10000))
            has_inf = torch.isinf(result_exp_16).any()
            has_nan = torch.isnan(result_exp_16).any()
            if has_inf or has_nan:
                print(f"❌ exp-log 方法 (float16)：出现 inf={has_inf}, nan={has_nan}")
            else:
                print(f"✓ exp-log 方法 (float16)：范围 [{result_exp_16.min():.2e}, {result_exp_16.max():.2e}]")
        except Exception as e:
            print(f"❌ exp-log 方法 (float16)：异常 - {e}")


if __name__ == "__main__":
    test_reciprocal_precision()
    test_extreme_d_model()
    test_float16_stability()
