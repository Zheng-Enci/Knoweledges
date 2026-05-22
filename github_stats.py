"""
统计 GitHub 用户所有仓库的代码量
"""
import requests
import json
from datetime import datetime

def get_github_stats(username):
    """获取 GitHub 用户所有仓库的统计信息"""
    
    print(f"🔍 正在获取 {username} 的 GitHub 仓库信息...\n")
    
    # 获取所有仓库
    repos = []
    page = 1
    while True:
        url = f'https://api.github.com/users/{username}/repos?per_page=100&page={page}'
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ 请求失败: {response.status_code}")
            return
        
        page_repos = response.json()
        if not page_repos:
            break
        
        repos.extend(page_repos)
        page += 1
    
    print(f"✅ 找到 {len(repos)} 个仓库\n")
    print("=" * 80)
    
    # 统计信息
    total_size_kb = 0
    total_stars = 0
    total_forks = 0
    language_stats = {}
    
    # 按大小排序
    repos_sorted = sorted(repos, key=lambda x: x.get('size', 0), reverse=True)
    
    print(f"{'仓库名称':<35} {'大小':>10} {'语言':<12} {'⭐':>5} {'🍴':>5}")
    print("=" * 80)
    
    for repo in repos_sorted:
        name = repo['name']
        size_kb = repo.get('size', 0)  # KB
        language = repo.get('language', 'N/A') or 'N/A'
        stars = repo.get('stargazers_count', 0)
        forks = repo.get('forks_count', 0)
        
        total_size_kb += size_kb
        total_stars += stars
        total_forks += forks
        
        # 统计语言
        if language != 'N/A':
            language_stats[language] = language_stats.get(language, 0) + 1
        
        # 打印（只显示非空仓库）
        if size_kb > 0:
            print(f"{name:<35} {size_kb:>8}KB {language:<12} {stars:>5} {forks:>5}")
    
    print("=" * 80)
    
    # 总计
    total_size_mb = total_size_kb / 1024
    total_size_gb = total_size_mb / 1024
    
    print(f"\n📊 统计汇总：")
    print(f"  总仓库数: {len(repos)} 个")
    print(f"  有内容的仓库: {len([r for r in repos if r.get('size', 0) > 0])} 个")
    print(f"  总代码量: {total_size_kb:,} KB = {total_size_mb:.2f} MB = {total_size_gb:.3f} GB")
    print(f"  总 Stars: {total_stars:,} 个")
    print(f"  总 Forks: {total_forks:,} 个")
    
    # 语言分布
    if language_stats:
        print(f"\n📝 编程语言分布：")
        sorted_languages = sorted(language_stats.items(), key=lambda x: x[1], reverse=True)
        for lang, count in sorted_languages:
            percentage = count / len(repos) * 100
            print(f"  {lang:<15} {count:>3} 个仓库 ({percentage:.1f}%)")
    
    # Top 5 最大仓库
    print(f"\n🏆 Top 5 最大仓库：")
    for i, repo in enumerate(repos_sorted[:5], 1):
        if repo.get('size', 0) > 0:
            size_mb = repo['size'] / 1024
            print(f"  {i}. {repo['name']}: {size_mb:.2f} MB")
    
    print(f"\n✨ 统计完成！")

if __name__ == "__main__":
    username = "Zheng-EnCi"
    get_github_stats(username)
