import numpy as np

class SimpleRNN:
    def __init__(self, input_size, hidden_size, output_size):
        """
        初始化 RNN 参数
        
        Args:
            input_size: 输入维度（如词向量维度）
            hidden_size: 隐藏层维度
            output_size: 输出维度
        """
        # 初始化权重矩阵（使用 Xavier 初始化）
        self.W_xh = np.random.randn(hidden_size, input_size) * 0.01
        self.W_hh = np.random.randn(hidden_size, hidden_size) * 0.01
        self.W_hy = np.random.randn(output_size, hidden_size) * 0.01
        
        # 初始化偏置
        self.b_h = np.zeros((hidden_size, 1))
        self.b_y = np.zeros((output_size, 1))
        
        self.hidden_size = hidden_size
    
    def forward(self, inputs):
        """
        前向传播
        
        Args:
            inputs: 输入序列，形状为 (seq_len, input_size)
        
        Returns:
            outputs: 输出序列，形状为 (seq_len, output_size)
            hidden_states: 隐藏状态序列，形状为 (seq_len, hidden_size)
        """
        seq_len = len(inputs)
        h = np.zeros((self.hidden_size, 1))  # 初始化隐藏状态
        
        outputs = []
        hidden_states = []
        
        for t in range(seq_len):
            x_t = inputs[t].reshape(-1, 1)  # 当前输入，转为列向量
            
            # 计算隐藏状态：h_t = tanh(W_xh·x_t + W_hh·h + b_h)
            h = np.tanh(self.W_xh @ x_t + self.W_hh @ h + self.b_h)
            
            # 计算输出：y_t = W_hy·h + b_y
            y = self.W_hy @ h + self.b_y
            
            outputs.append(y.flatten())
            hidden_states.append(h.flatten())
        
        return np.array(outputs), np.array(hidden_states)


# 使用示例
if __name__ == "__main__":
    # 参数设置
    input_size = 100   # 输入维度（词向量维度）
    hidden_size = 128  # 隐藏层维度
    output_size = 50   # 输出维度
    seq_len = 3        # 序列长度（如"我爱北京"）
    
    # 创建 RNN
    rnn = SimpleRNN(input_size, hidden_size, output_size)
    
    # 生成随机输入（实际应用中应为词向量）
    inputs = np.random.randn(seq_len, input_size)
    
    # 前向传播
    outputs, hidden_states = rnn.forward(inputs)
    
    print(f"输入形状: {inputs.shape}")           # (3, 100)
    print(f"输出形状: {outputs.shape}")          # (3, 50)
    print(f"隐藏状态形状: {hidden_states.shape}") # (3, 128)
    print(f"最终隐藏状态: {hidden_states[-1][:5]}...")  # 最后一时刻的隐藏状态