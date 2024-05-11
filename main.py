import pandas as pd
from geojson import Feature, FeatureCollection, LineString
import re


# 用于从字符串中提取坐标的辅助函数
def extract_coordinates(point_str):
    # 使用正则表达式匹配数字
    match = re.match(r'POINT \(([^ ]+) ([^ ]+)\)', point_str)
    if match:
        # 将提取的字符串坐标转换为浮点数
        return float(match.group(1)), float(match.group(2))
    else:
        raise ValueError(f"Can't parse point string: {point_str}")


# 读取CSV文件
df = pd.read_csv('20231102_all_connected_clean_routes_seg_counts.csv')

# 创建GeoJSON特征列表
features = []

for _, row in df.iterrows():
    # 假设START_POINT和END_POINT是以逗号分隔的字符串："经度,纬度"
    start_lon, start_lat = extract_coordinates(row['START_POINT'])
    end_lon, end_lat = extract_coordinates(row['END_POINT'])

    # 创建LineString对象
    line = LineString([(start_lon, start_lat), (end_lon, end_lat)])

    # 创建特征并添加到列表
    features.append(Feature(geometry=line,properties={
        'seg_id': row['SEG_ID'],
        'count': row['COUNT']
    }))

# 创建特征集合
feature_collection = FeatureCollection(features)

# 将GeoJSON对象写入文件
with open('output.geojson', 'w') as f:
    f.write(str(feature_collection))

print('GeoJSON file created successfully.')
