# サードパーティimports
import yaml

# デフォの設定値の定義
default_config = {
    'convert':{
        'a': {
            'o_format_ext': "m4a"
        }
    }
}
# default_config = {
#     'encoder': {
#         'a': {
#             "m4a": "aac",
#             "mp3": "libmp3lame",
#         },
#         'b': {},
#         'c': [
#             "d",
#             "e",
#         ],
#         'd': []
#     },
# }

# 空の辞書やリストを削除
def remove_empty(data):
    if isinstance(data, dict): # 辞書なら削除処理を行う
        return {k: remove_empty(v) for k, v in data.items() if v != {} and v != []} # 値が空でなければその中も探索する、空ならばif文を抜けdataを返す
    elif isinstance(data, list):
        return [remove_empty(item) for item in data if item != []]
    return data

# main
def generate_default_config(filename="config.yml"):
    clean_default_config = remove_empty(default_config)
    print(clean_default_config)
    with open(filename, 'w') as file:
        yaml.dump(clean_default_config, file, default_flow_style=False, allow_unicode=True) # default_flow_styleはインデント付きのブロック形式

if __name__ == "__main__":
    generate_default_config()