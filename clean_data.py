import json
import os

# 读取文件3，构建filename到text的映射
filename_to_text = {}
with open('/mnt/afs/xueyingyi/image_vague/loc_dection/text.jsonl', 'r') as f3:
    for line in f3:
        data = json.loads(line)
        file_name = data['file_name']
        text = data['text'].strip()  # 去除首尾空白字符
        if text:  # 只保留非空文本
            filename_to_text[file_name] = text

# 读取文件1，构建image_path到detections的映射
image_path_to_detections = {}
with open('/mnt/afs/xueyingyi/image_vague/loc_dection/dections_Eimage.jsonl', 'r') as f1:
    for line in f1:
        data = json.loads(line)
        image_path = data['image_path']
        image_path_to_detections[image_path] = data['detections']

# 处理文件2并生成更新后的内容
output_lines = []
with open('/mnt/afs/xueyingyi/image_vague/loc_dection/api_match_dections_Eimage.jsonl', 'r') as f2:
    for line in f2:
        entry = json.loads(line)
        detections = entry['detections']
        image_path = entry['image_path']
        
        # 仅处理detections为空的情况
        if not detections:
            file_name = os.path.basename(image_path)  # 从路径提取文件名
            text = filename_to_text.get(file_name, '')
            
            if text:  # 文本不为空
                # 从文件1获取对应detections
                detections_f1 = image_path_to_detections.get(image_path, [])
                
                if detections_f1:  # 确保文件1中存在检测结果
                    first_bbox = detections_f1[0]['bbox']
                    # 创建新的detection条目
                    new_detection = {
                        "bbox": first_bbox,
                        "text": text
                    }
                    entry['detections'] = [new_detection]
        
        # 将更新后的条目写入输出
        output_lines.append(json.dumps(entry) + '\n')

# 将结果写入新文件（可根据需求修改输出路径）
with open('/mnt/afs/xueyingyi/image_vague/loc_dection/processed_dections_Eimage_UPDATED.jsonl', 'w') as f_out:
    f_out.writelines(output_lines)

print("处理完成！结果已保存至 processed_dections_Eimage_UPDATED.jsonl")