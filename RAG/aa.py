# 示例：每 200 字符一块，重叠 20 字符
chunk_size = 50
chunk_overlap = 10

# 原始文本：关于Python装饰器的知识点
text = """
    Python装饰器是一种用于修改函数或方法行为的高级特性。
    它本质上是一个接受函数作为参数并返回新函数的函数。
    使用@语法糖可以让代码更加简洁优雅。
    装饰器常用于日志记录、权限验证、性能监控等场景。
    理解装饰器需要掌握闭包和函数作为一等公民的概念。
    """

# 固定大小分块实现
def fixed_size_split(text: str, chunk_size: int, chunk_overlap:int) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        # 截取当前块
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.replace('\n', ''))
        # 下一个块的起始位置（考虑重叠）
        start = end - chunk_overlap
    return chunks

def main() -> None:
    # 执行切分
    chunks = fixed_size_split(text, chunk_size, chunk_overlap)

    # 切分结果
    for i, chunk in enumerate(chunks):
        print(f"第{i+1}块：{chunk}")

if __name__ == "__main__":
    main()
