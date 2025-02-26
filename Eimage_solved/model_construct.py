import json
import os

# 文件路径设置，根据实际情况调整
dections_path = '/mnt/afs/xueyingyi/image_vague/loc_dection/Eimage_solved/dections_Eimage_normalized.jsonl'
text_filtered_path = '/mnt/afs/xueyingyi/image_vague/loc_dection/text_FILTERED.jsonl'
output_path = '/mnt/afs/xueyingyi/image_vague/loc_dection/Eimage_solved/Eimage_final.jsonl'

# 读取text数据，构建文件名到文本的映射
text_data = {}
with open(text_filtered_path, 'r') as f:
    for line in f:
        entry = json.loads(line)
        text_data[entry['file_name']] = entry['text']

# 处理检测数据并生成输出
output_entries = []
current_id = 1

with open(dections_path, 'r') as f:
    for line in f:
        det_entry = json.loads(line)
        image_path = det_entry['image_path']
        file_name = os.path.basename(image_path)
        
        # 获取对应的文本
        if file_name not in text_data:
            continue  # 跳过没有对应文本的条目
        text = text_data[file_name]
        
        # 构建image列表
        new_image_path = image_path.replace('/image/', '/inpainting_demo/')
        image_list = [
            "/mnt/afs/xueyingyi/image_vague/inpainting_demo/image_ (0).jpg",
            new_image_path
        ]
        
        # 构建对话内容
        # Human部分
        human_value = f"""I'm going to give you a sentence and a picture. Please divide the whole sentence sensibly and place each in the right place in the picture to convey the meaning of the whole picture humor. Finally, please give me the text box coordinates location and the corresponding text.\n\nFor example, this picture:\n<image>\nthis sentence:That moment after you throw up and your friend asks you \"YOU GOOD BRO?\" I'M FUCKIN LIT\nthe answer should be:<ref>Writable text area</ref><box>[[0000, 0001, 0992, 0290]]</box>:That moment after you throw up and your friend asks you \"YOU GOOD BRO?\",\n<ref>Writable text area</ref><box>[[0276, 0801, 0746, 0903]]</box>:I'M FUCKIN LIT\nNow look at this picture:\n<image>\n Now, please deal with this sentence: {text}"""
        
        # GPT部分
        gpt_lines = []
        detections = det_entry['detections']
        for i, det in enumerate(detections):
            bbox = [str(num).zfill(4) for num in det['bbox']]
            line = f"<ref>Writable text area</ref><box>[[{', '.join(bbox)}]]</box>:{det['text']}"
            # 最后一个元素不加逗号
            if i != len(detections) - 1:
                line += ","
            gpt_lines.append(line)
        gpt_value = '\n'.join(gpt_lines)
        
        # 构建完整条目
        output_entry = {
            "id": current_id,
            "image": image_list,
            "conversations": [
                {"from": "human", "value": human_value},
                {"from": "gpt", "value": gpt_value}
            ]
        }
        output_entries.append(output_entry)
        current_id += 1

# 写入输出文件
with open(output_path, 'w') as f:
    for entry in output_entries:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')