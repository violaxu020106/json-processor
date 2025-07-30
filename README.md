# JSON数据处理工具

这是一个用于处理Excel/CSV文件中JSON数据的Web应用。主要功能是从`result_data`字段中提取`reflection`和`attributes`信息，并生成新的列。

## 功能特点

- 🚀 **简单易用**: 拖拽上传文件，一键处理
- 📊 **数据预览**: 处理前可预览数据结构和内容
- 📈 **处理统计**: 显示处理成功和失败的统计信息
- 💾 **多格式支持**: 支持CSV、Excel (.xlsx, .xls) 格式
- 🔄 **实时反馈**: 处理进度条和状态提示
- 📱 **响应式设计**: 支持各种设备访问

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

### 3. 访问应用

打开浏览器访问: http://localhost:5000

## 使用说明

### 1. 上传文件
- 点击上传区域或直接拖拽文件到指定区域
- 支持的文件格式: CSV、Excel (.xlsx, .xls)
- 最大文件大小: 16MB

### 2. 文件格式要求
上传的文件必须包含以下列:
- `result_data`: 包含JSON格式数据的列

### 3. 处理逻辑
- 从`result_data`字段中解析JSON数据
- 提取`message`字段中的`reflection`内容
- 提取`message`字段中的`attribute`内容并转换为标准JSON格式
- 如果解析失败，在对应列显示"failed"

### 4. 输出结果
处理后的文件将包含以下新列:
- `reflection`: 提取的reflection内容
- `attributes`: 提取的attributes内容（标准JSON格式）

## 文件结构

```
├── app.py              # Flask应用主文件
├── process_json.py     # JSON数据处理逻辑
├── requirements.txt    # Python依赖包
├── README.md          # 说明文档
├── templates/         # HTML模板
│   └── index.html     # 主页面
├── uploads/           # 上传文件存储目录
└── temp/              # 处理结果临时存储目录
```

## 示例数据格式

### 输入格式
```csv
primary_key,image_url,prod_name,result_data
/10000000483863,https://...,Face Pack Korea...,{"message":"{\n  \"reflection\": \"从产品名称和图片中可以确定...\",\n  \"attribute\": {\n    \"Logo Customized\": \"\",\n    \"Skin Type\": \"\",\n    \"Place of Origin\": \"KOREA\"\n  }\n}"}
```

### 输出格式
```csv
primary_key,image_url,prod_name,result_data,reflection,attributes
/10000000483863,https://...,Face Pack Korea...,{"message":"..."},从产品名称和图片中可以确定...,{"Logo Customized":"","Skin Type":"","Place of Origin":"KOREA"}
```

## 技术栈

- **后端**: Python Flask
- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **数据处理**: Pandas
- **文件处理**: openpyxl (Excel), csv (CSV)

## 注意事项

1. 确保上传的文件包含`result_data`列
2. JSON数据格式必须符合预期结构
3. 大文件处理可能需要较长时间
4. 处理失败的行会在新列中显示"failed"

## 故障排除

### 常见问题

1. **文件上传失败**
   - 检查文件格式是否正确
   - 确认文件大小不超过16MB

2. **处理结果为空**
   - 检查`result_data`列是否存在
   - 确认JSON格式是否正确

3. **大量数据解析失败**
   - 检查JSON数据是否包含转义字符
   - 确认数据格式是否一致

## 开发说明

### 本地开发

1. 克隆项目
2. 安装依赖: `pip install -r requirements.txt`
3. 运行开发服务器: `python app.py`
4. 访问 http://localhost:5000

### 自定义处理逻辑

如需修改JSON处理逻辑，请编辑`process_json.py`文件中的`process_json_data`函数。

## 许可证

MIT License 