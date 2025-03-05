import yaml
import json

# 读取 YAML 文件
with open("2025-03-02.yml", "r", encoding="utf-8") as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)  # 解析 YAML

# 将 YAML 转换为 JSON
json_data = json.dumps(yaml_data, indent=4, ensure_ascii=False)

# 保存 JSON 文件
with open("terms/2025-03-02.json", "w", encoding="utf-8") as json_file:
    json_file.write(json_data)

print("转换完成！")
