import os
import yaml
import json
import glob

def convert_yaml_to_json(folder_path):
    # 获取所有 .yml 或 .yaml 文件
    yaml_files = glob.glob(os.path.join(folder_path, "*.yml")) + glob.glob(os.path.join(folder_path, "*.yaml"))

    if not yaml_files:
        print("未找到 YAML 文件！")
        return

    for yaml_file in yaml_files:
        try:
            # 读取 YAML 文件
            with open(yaml_file, "r", encoding="utf-8") as file:
                yaml_data = yaml.safe_load(file)

            # 生成对应的 JSON 文件路径
            json_file = os.path.splitext(yaml_file)[0] + ".json"

            # 写入 JSON 文件
            with open(json_file, "w", encoding="utf-8") as file:
                json.dump(yaml_data, file, indent=4, ensure_ascii=False)

            print(f"转换成功: {yaml_file} → {json_file}")

        except Exception as e:
            print(f"转换失败: {yaml_file}, 错误信息: {e}")

# 运行转换（修改为你的文件夹路径）
folder_path = "./"  # 替换为实际的文件夹路径
convert_yaml_to_json(folder_path)
