import json  
import os  
import re  
from collections import defaultdict  

# 处理第一个文件并收集需要删除的文本  
deleted_text_map = defaultdict(list)  

# 输入输出文件路径  
input_file1 = "/mnt/afs/xueyingyi/image_vague/loc_dection/processed_dections_Eimage_UPDATED.jsonl"  
output_file1 = "/mnt/afs/xueyingyi/image_vague/loc_dection/processed_dections_FILTERED.jsonl"  
input_file2 = "/mnt/afs/xueyingyi/image_vague/loc_dection/text.jsonl"   
output_file2 = "/mnt/afs/xueyingyi/image_vague/loc_dection/text_FILTERED.jsonl"  

# 处理第一个文件  
with open(input_file1, "r") as f_in, open(output_file1, "w") as f_out:  
    for line in f_in:  
        data = json.loads(line.strip())  
        image_name = os.path.basename(data["image_path"])  
        
        # 过滤检测框并记录被删除的文本  
        filtered = []  
        for detection in data["detections"]:  
            text = detection["text"]  
            if any(s in text for s in (".com", ".net", "http")):  
                deleted_text_map[image_name].append(text.strip().lower())  
            else:  
                filtered.append(detection)  
        
        # 写入处理后的数据  
        data["detections"] = filtered  
        f_out.write(json.dumps(data) + "\n")  

# 处理第二个文件  
with open(input_file2, "r") as f_in, open(output_file2, "w") as f_out:  
    for line in f_in:  
        data = json.loads(line.strip())  
        image_name = data["file_name"]  
        
        # 获取需要删除的文本列表  
        to_remove = deleted_text_map.get(image_name, [])  
        
        # 分割文本并过滤  
        lines = data["text"].split("\n")  
        pattern = re.compile(r"\.com|\.net|http", re.IGNORECASE)  
        filtered_lines = [ln for ln in lines if not pattern.search(ln)]  
        
        # 重新组合文本并保留换行结构  
        data["text"] = "\n".join(filtered_lines)  
        f_out.write(json.dumps(data) + "\n")  

print("处理完成！结果保存在：\n", output_file1, "\n", output_file2)