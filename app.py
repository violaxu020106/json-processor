from flask import Flask, render_template, request, send_file, jsonify
import os
import pandas as pd
from werkzeug.utils import secure_filename
from process_json import process_json_data, save_processed_file
import tempfile
import uuid

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TEMP_FOLDER'] = 'temp'

# 确保目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['file']
        
        # 检查文件名
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        # 检查文件类型
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件格式，请上传CSV或Excel文件'}), 400
        
        # 保存上传的文件
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # 处理文件
        try:
            df = process_json_data(file_path)
            
            # 生成输出文件名 - 保持原始格式
            output_filename = f"processed_{filename}"
            
            output_path = os.path.join(app.config['TEMP_FOLDER'], output_filename)
            
            # 保存处理后的文件
            if output_filename.endswith('.csv'):
                # 处理NaN值，避免JSON解析错误
                df_clean = df.fillna('')
                df_clean.to_csv(output_path, index=False, encoding='utf-8-sig')
            elif output_filename.endswith('.xlsx'):
                df.to_excel(output_path, index=False, engine='openpyxl')
            elif output_filename.endswith('.xls'):
                df.to_excel(output_path, index=False, engine='xlwt')
            else:
                # 默认保存为CSV
                df_clean = df.fillna('')
                df_clean.to_csv(output_path, index=False, encoding='utf-8-sig')
            
            # 返回处理结果统计
            total_rows = len(df)
            success_count = len(df[df['reflection'] != 'failed'])
            failed_count = total_rows - success_count
            
            return jsonify({
                'success': True,
                'message': '文件处理成功',
                'filename': output_filename,
                'stats': {
                    'total_rows': total_rows,
                    'success_count': success_count,
                    'failed_count': failed_count
                }
            })
            
        except Exception as e:
            return jsonify({'error': f'处理文件时出错: {str(e)}'}), 500
        
    except Exception as e:
        return jsonify({'error': f'上传文件时出错: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['TEMP_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': '文件不存在'}), 404
        
        return send_file(file_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': f'下载文件时出错: {str(e)}'}), 500

@app.route('/preview/<filename>')
def preview_file(filename):
    try:
        file_path = os.path.join(app.config['TEMP_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': '文件不存在'}), 404
        
        # 读取文件并返回前10行预览
        if filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(file_path, engine='openpyxl')
        elif filename.endswith('.xls'):
            df = pd.read_excel(file_path, engine='xlrd')
        else:
            # 尝试自动检测格式
            try:
                df = pd.read_excel(file_path, engine='openpyxl')
            except:
                df = pd.read_excel(file_path, engine='xlrd')
        
        # 处理NaN值，避免JSON解析错误
        df = df.fillna('')
        preview_data = df.head(10).to_dict('records')
        columns = df.columns.tolist()
        
        return jsonify({
            'success': True,
            'columns': columns,
            'preview': preview_data,
            'total_rows': len(df)
        })
        
    except Exception as e:
        return jsonify({'error': f'预览文件时出错: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 