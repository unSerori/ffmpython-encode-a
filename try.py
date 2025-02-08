import ffmpeg
import pygame

i_file = ".\\original_files\\01 song.wav"
o_file = ".\\encoded_files\\01 song.mp3"
encoder = "libmp3lame"

# pygame.mixer.init()
# pygame.mixer.music.load(i_file)
# pygame.mixer.music.play()

# input("enter...")
# pygame.mixer.music.stop()

# 変換 ffmpeg -i "%%h" -codec:a %encoder% "%%~nh.%afterext%"

i = ffmpeg.input(i_file)
stream = ffmpeg.output(i, o_file, acodec=encoder)

ffmpeg.run(stream)

# (
#     ffmpeg
#     .input(i_file)
#     .output(o_file, acodec=encoder, crf=23, preset='slow')
#     .run()
# )

# 標準imports
import chardet
import os
import sys
from pathlib import Path
import json
# サードパーティimports
import yaml
import ffmpeg
from mutagen import File
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import taglib
from pprint import pprint
# 自作
from gen_conf import generate_default_config

print()

# スクリプトファイルの場所に移動
os.chdir(os.path.dirname(sys.argv[0]))  # Courtesy of mattuu0

# YAMLからの設定値読み込み
def load_config():
    # なければデフォのファイルを作成
    if not os.path.exists("./config.yml"):
        generate_default_config()

    # 読みこみ
    with open("config.yml") as conf_file:
        config = yaml.safe_load(conf_file)
    return config

def encode_file(o_dir: str, i_filename: str, ext: str) -> bool | str:
    """エンコード
    
    ffmpegを利用して変換する

    Parameters
    ----------
    o_dir: str
        出力先ディレクトリ
    i_filename: str
        変換するファイルのパス
    ext: str
        変換したい拡張子

    Returns
    -------
    bool or str
        成功したらTrue、失敗したらエラーメッセージ
    """

    # 出力ファイル名
    o_filename = o_dir + os.path.sep + os.path.splitext(os.path.basename(i_filename))[0] + "." + ext
    print(o_filename)

    try:
        if os.path.exists(o_filename):
            raise FileExistsError(f"Cannot write because the target file '{o_filename}' already exists.")
        else:
            i = ffmpeg.input(i_filename) # 入力ファイル
            stream = ffmpeg.output(i, o_filename,) # streamとは # acodec=encoder
            ffmpeg.run(stream, overwrite_output=True) # 実行
    except (ffmpeg.Error, FileExistsError)  as e:
        print(f"Error encoding file: {e}")
        return e
    
    return True

def get_metadata(target_file: str) -> dict:
    """メタデータの取得
    
    ffprobeを利用してメタデータを取得する

    Parameters
    ----------
    target_file: str
        対象のファイルパス

    Returns
    -------
    dict
        メタデータの辞書
    """

    song = taglib.File(target_file)
    tags = song.tags
    pprint(tags)

    return tags

    # print("a")
    # print(target_file)

    # with taglib.File(target_file, save_on_exit=False) as song:
    #     print(type(song))
    #     print(type(song.tags))
    #     print(song.tags)
    #     song.length

    # print("b")




    # metadata = ffmpeg.probe(target_file) # メタデータを取得
    # tags = metadata.get("format", {}).get("tags", {}) # タグ情報のみ
    # print(tags)

    # decoded_tags = {}
    # for key, value in tags.items():
    #     try:
    #         # Unicode文字列を指定のエンコーディングでエンコードしてバイト列に変換し、その後utf-8でデコード
    #         decoded_value = value.encode('shift_jis').decode('utf-8')
    #     except (UnicodeEncodeError, UnicodeDecodeError):
    #         # エンコードまたはデコードに失敗した場合は元の値を使用
    #         decoded_value = value
    #     decoded_tags[key] = decoded_value

    # # デコードされたタグ情報を表示
    # for key, value in decoded_tags.items():
    #     print(f'{key}: {value}')

    #     # デコードされたタグ情報を表示
    #     for key, value in decoded_tags.items():
    #         print(f'{key}: {value}')    









        # detected = chardet.detect(v.encode())
        # print(detected)
        # # 判別されたエンコーディングでデコードを試みる
        # try:
        #     decoded_value = v.encode().decode(detected['encoding'])
        # except (UnicodeDecodeError, TypeError):
        #     # デコードできなかった場合はデフォルトでUTF-8に戻す
        #     decoded_value = v.encode().decode('utf-8', errors='ignore')
        
        # print(f"{k}: {decoded_value}")

    
    # metadata = ffmpeg.probe(target_file) # メタデータを取得
    # tags = metadata.get("format", {}).get("tags", {}) # タグ情報のみ
    # print(tags)
    # pyperclip.copy(tags)
    # adjustedTags = {}
    # for k, v in tags.items():
    #     detected = chardet.detect(v.encode())
    #     print(detected)
    #     # 判別されたエンコーディングでデコードを試みる
    #     try:
    #         decoded_value = v.encode().decode(detected['encoding'])
    #     except (UnicodeDecodeError, TypeError):
    #         # デコードできなかった場合はデフォルトでUTF-8に戻す
    #         decoded_value = v.encode().decode('utf-8', errors='ignore')
        
    #     print(f"{k}: {decoded_value}")

        # encoded_bytes = v.encode(errors="ignore") # 文字列をバイト列に
        # detected = chardet.detect(encoded_bytes)  # 文字コードを検出
        # encoding = detected["encoding"] or "utf-8"  # `None` の場合のデフォルト
        # try:
        #     fixed_value = encoded_bytes.decode(encoding)  # 検出されたエンコーディングでデコード
        # except (UnicodeDecodeError, TypeError):
        #     fixed_value = encoded_bytes.decode("shift_jis")  # 失敗したら UTF-8 で強制変換

        # print(f"{k}: {fixed_value} (Encoding: {encoding})\n")

        # detected = chardet.detect(v.encode())
        # print(k)
        # print(v)
        # print(detected)
        # v.encode(detected["encoding"]).decode("utf-8")
        # print(v)
        # print()
    




    # ffprobe -show_chapters -i foobar.mp4


# メタデータの書き込み
def write_metadata(target_file: str) -> bool:
    return bool

# main
def main():
    # 必要な設定値を読み込む
    config = load_config()
    conv_ext = config['convert']['a']['o_format_ext'] # ext

    # 入出力ディレクトリ
    i_dir = "./original_files/"
    o_dir = "./encoded_files/"
    def adjust_directory_path(dir: str) -> str:
        # /に統一、
        if "\\" in i_dir:
            dir = dir.replace("\\", "/")
        # パス形式に統一して不必要なもの（:末尾の/など）を除外
        dir = os.path.normpath(dir)

        return dir
    adjusted_i_dir = adjust_directory_path(i_dir)
    adjusted_o_dir = adjust_directory_path(o_dir)

    # なければ作成
    os.makedirs(adjusted_i_dir, exist_ok=True)
    os.makedirs(adjusted_o_dir, exist_ok=True)

    # 1ファイルずつ処理
    for filename in os.listdir(adjusted_i_dir): # 入力ディレクトリ内
        i_filepath = adjusted_i_dir + os.path.sep + filename

        # ファイルでないならコンテ
        if not os.path.isfile(i_filepath):
            print(f"{filename} is not file.")
            continue
        
        # エンコード
        ef = encode_file(adjusted_o_dir, i_filepath, conv_ext)
        if not ef:
            print(f"encode error: {ef}")
            return

        # メタデータを取得
        tags = get_metadata(i_filepath)
        # メタデータを書き込む

if __name__ == "__main__":
    main()