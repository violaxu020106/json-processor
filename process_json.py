import pandas as pd
import json
import re
import ast

def clean_json_string(json_str):
    """
    清理JSON字符串，处理控制字符和转义字符
    """
    if not isinstance(json_str, str):
        return json_str
    
    # 移除控制字符
    json_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_str)
    
    # 处理转义字符
    json_str = json_str.replace('\\n', '\n')
    json_str = json_str.replace('\\"', '"')
    json_str = json_str.replace('\\t', '\t')
    json_str = json_str.replace('\\r', '\r')
    
    # 移除开头和结尾的引号
    if json_str.startswith('"') and json_str.endswith('"'):
        json_str = json_str[1:-1]
    
    return json_str

def extract_json_from_string(text):
    """
    从字符串中提取JSON数据
    """
    if not isinstance(text, str):
        return None
    
    # 尝试直接解析
    try:
        return json.loads(text)
    except:
        pass
    
    # 尝试清理后解析
    try:
        cleaned = clean_json_string(text)
        return json.loads(cleaned)
    except:
        pass
    
    # 尝试使用ast.literal_eval
    try:
        return ast.literal_eval(text)
    except:
        pass
    
    # 尝试正则表达式提取JSON
    try:
        # 查找最外层的JSON对象
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, text)
        if matches:
            return json.loads(matches[0])
    except:
        pass
    
    return None

def process_json_data(file_path):
    """
    处理Excel/CSV文件中的JSON数据
    从result_data字段中提取reflection和attributes
    """
    try:
        # 读取文件
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("不支持的文件格式，请使用CSV或Excel文件")
        
        # 检查是否存在result_data列
        if 'result_data' not in df.columns:
            raise ValueError("文件中没有找到'result_data'列")
        
        # 创建新的列
        df['reflection'] = 'failed'
        df['attributes'] = 'failed'
        
        success_reflection = 0
        success_attributes = 0
        
        # 处理每一行
        for index, row in df.iterrows():
            result_data = row['result_data']
            
            if pd.isna(result_data) or result_data == '':
                continue
            
            try:
                # 解析外层JSON
                outer_json = extract_json_from_string(str(result_data))
                if not outer_json:
                    continue
                
                # 获取message字段
                message = outer_json.get('message', '')
                if not message:
                    continue
                
                # 解析内层JSON
                inner_json = extract_json_from_string(str(message))
                if not inner_json:
                    continue
                
                # 提取reflection
                reflection = inner_json.get('reflection', '')
                if reflection:
                    df.at[index, 'reflection'] = reflection
                    success_reflection += 1
                
                # 提取attributes
                attributes = inner_json.get('attribute', {})
                if attributes:
                    df.at[index, 'attributes'] = json.dumps(attributes, ensure_ascii=False)
                    success_attributes += 1
                
            except Exception as e:
                print(f"处理第{index+1}行时出错: {str(e)}")
                continue
        
        # 保存处理后的文件
        output_file = 'processed_result.csv'
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"处理完成，结果已保存到: {output_file}")
        print(f"\n处理统计:")
        print(f"总行数: {len(df)}")
        print(f"成功提取reflection: {success_reflection}")
        print(f"成功提取attributes: {success_attributes}")
        
        return df
        
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        return None

def save_processed_file(df, output_path):
    """
    保存处理后的文件
    """
    try:
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        return True
    except Exception as e:
        print(f"保存文件时出错: {str(e)}")
        return False

if __name__ == "__main__":
    # 处理CSV文件
    process_json_data("result (21).csv") 