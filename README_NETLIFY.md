# JSON数据处理工具 - Netlify部署版

这是一个完全在前端运行的JSON数据处理工具，可以直接部署到Netlify等静态网站托管平台。

## 功能特点

- 🚀 **纯前端实现**：无需后端服务器，完全在浏览器中运行
- 📊 **支持多种格式**：CSV、Excel (.xlsx, .xls) 文件
- 🔄 **实时处理**：文件上传后立即处理，无需等待
- 📱 **响应式设计**：支持各种设备访问
- 💾 **本地处理**：所有数据都在本地处理，保护隐私

## 部署到Netlify

### 方法一：通过GitHub部署（推荐）

1. **上传到GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/你的用户名/json-processor.git
   git push -u origin main
   ```

2. **在Netlify中部署**
   - 访问 [Netlify](https://netlify.com)
   - 点击 "New site from Git"
   - 选择你的GitHub仓库
   - 点击 "Deploy site"

### 方法二：直接拖拽部署

1. 将项目文件夹压缩成ZIP文件
2. 访问 [Netlify](https://netlify.com)
3. 将ZIP文件拖拽到部署区域
4. 等待部署完成

## 文件说明

- `index.html` - 主页面文件，包含所有功能
- `netlify.toml` - Netlify配置文件
- `README_NETLIFY.md` - 部署说明文档

## 技术实现

- **前端框架**：纯HTML + CSS + JavaScript
- **文件处理**：使用PapaParse处理CSV，SheetJS处理Excel
- **JSON解析**：原生JavaScript JSON.parse
- **文件下载**：使用Blob API生成下载文件

## 使用说明

1. 打开网站
2. 点击上传区域或拖拽文件
3. 等待处理完成
4. 查看预览数据
5. 点击下载按钮获取处理后的文件

## 浏览器兼容性

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 注意事项

- 文件大小限制：16MB
- 支持的文件格式：CSV、Excel (.xlsx, .xls)
- 所有处理都在本地完成，不会上传到服务器
- 需要包含result_data列的文件才能正常处理

## 自定义配置

如需修改文件大小限制或其他配置，请编辑 `index.html` 文件中的相应参数。 