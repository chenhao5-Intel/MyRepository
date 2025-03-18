import subprocess
from collections import defaultdict

def get_deleted_folders(repo_path, commit1, commit2):
    # 运行 git diff 命令
    result = subprocess.run(
        ['git', '-C', repo_path, 'diff', '--name-status', commit1, commit2],
        capture_output=True, text=True, check=True
    )

    # 提取被删除的文件
    deleted_files = [line.split('\t')[1] for line in result.stdout.splitlines() if line.startswith('D')]

    # 组织文件夹结构
    folder_files = defaultdict(set)
    for file_path in deleted_files:
        folder = '/'.join(file_path.split('/')[:-1])
        folder_files[folder].add(file_path)

    # 检查文件夹是否被完全删除
    deleted_folders = set()
    for folder, files in folder_files.items():
        # 如果文件夹下的所有文件都在 deleted_files 中，则认为文件夹被删除
        if all(file in deleted_files for file in files):
            deleted_folders.add(folder)

    return deleted_folders

# 使用示例
if __name__ == "__main__":
    # 替换为你的 Git 仓库路径
    repo_path = 'C:/Works/MyRepository/'

    # 替换为你要比较的两个提交的哈希值
    commit1 = '703441edefada314872fe6fb6a57d35a34921c24'
    commit2 = '9020ddbd92a2062953c4a45ecea2187c298bbaf4'

    # 获取被删除的文件夹
    deleted_folders = get_deleted_folders(repo_path, commit1, commit2)

    # 打印结果
    print("Deleted folders:")
    for folder in deleted_folders:
        print(folder)