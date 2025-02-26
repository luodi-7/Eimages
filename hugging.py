from huggingface_hub import HfApi  
import os  
import time  

api = HfApi()  

# 本地文件夹路径  
local_folder = "/mnt/afs/niuyazhe/data/lister/meme/quickmeme_images"  

# 仓库中的目标路径  
repo_path = "quickmeme_images"  

# 遍历本地文件夹中的所有文件  
for root, dirs, files in os.walk(local_folder):  
    for file in files:  
        # 本地文件路径  
        local_file_path = os.path.join(root, file)  

        # 仓库中的文件路径  
        relative_path = os.path.relpath(local_file_path, local_folder)  
        repo_file_path = os.path.join(repo_path, relative_path)  

        try:  
            # 上传文件  
            api.upload_file(  
                path_or_fileobj=local_file_path,  
                path_in_repo=repo_file_path,  
                repo_id="luodi-7/quickmeme",  
                repo_type="dataset"  
            )  
            print(f"Uploaded: {repo_file_path}")  
        except Exception as e:  
            print(f"Failed to upload {repo_file_path}: {e}")  
            print("Waiting for 10 minutes before retrying...")  
            time.sleep(600)  # 等待 10 分钟后重试