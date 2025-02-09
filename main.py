# 標準imports
import os
import sys
# サードパーティimports
import yaml
import ffmpeg
# 自作
from gen_conf import generate_default_config

print()

# スクリプトファイルの場所に移動
os.chdir(os.path.dirname(sys.argv[0]))  # Courtesy of mattuu0

def load_config(conf_path: str) -> map:
    """YAMLからの設定値読み込み
    
    指定されたYAMLファイルに記載された設定値をmapとして読み込む

    Parameters
    ----------
    conf_path: str
        読み込むファイルのパス
    """

    adjusted_conf_path = os.path.normpath(conf_path)

    # なければデフォのファイルを作成
    if not os.path.exists(adjusted_conf_path):
        generate_default_config(adjusted_conf_path)

    # 読みこみ
    with open(adjusted_conf_path) as conf_file:
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
    o_filename = os.path.join(o_dir, os.path.splitext(os.path.basename(i_filename))[0] + "." + ext)

    print("i_filename: " + i_filename)
    print("o_filename: " + o_filename)

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

# main
def main():
    # 必要な設定値を読み込む
    config = load_config("config.yml")
    conv_ext = config['convert']['a']['o_format_ext'] # ext

    # 入出力ディレクトリ
    i_dir = "./target_files/"
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

    def recursive_process_files(i_dir: str, callback: callable):
        """ディレクトリ内を一括処理
        
        ディレクトリ内のファイルを一括処理、その際にディレクトリがあったらその中を再帰する

        Parameters
        ----------
        o_dir: str
            作業を適用するディレクトリ
        """

        # 1ファイルずつ処理
        for entry in os.listdir(i_dir): # 入力ディレクトリ内
            # 処理対象のパスを作成（:対象ディレクトリとファイルorディレクトリ名を結合）
            entry_path = os.path.join(i_dir, entry)
            print("entry_path: " + entry_path)

            # ファイルなら処理、
            if os.path.isfile(entry_path):
                # 出力先パスを作成
                i_dir_split = os.path.normpath(i_dir).split(os.sep, 1) # 1層目のディレクトリとそれをのぞいたパスが返る
                o_filename_path = os.path.join(o_dir, i_dir_split[1]) if len(i_dir_split) > 1 else o_dir # 二層以上に分かれているなら、、、一層目をのぞいて出力ディレクトリを結合 el 一層目だけ返す
                # 処理
                ef = callback(o_filename_path, entry_path, conv_ext)
                if not ef:
                    print(f"encode error: {ef}")
                    return
            # ディレクトリなら必要なディレクトリを作成し、再帰する
            else:
                print(f"{entry} is not file.")
                # 結果パス内に作成する出力ディレクトリパスを作成
                i_dir_split = os.path.normpath(entry_path).split(os.sep, 1) # 1層目のディレクトリとそれをのぞいたパスが返る
                o_path = os.path.join(o_dir, i_dir_split[1]) if len(i_dir_split) > 1 else o_dir # 二層以上に分かれているなら、、、一層目をのぞいて出力ディレクトリを結合 el 一層目だけ返す
                print("o_path:", o_path)
                # ディレクトリを作成
                os.makedirs(o_path, exist_ok=True) # 再帰作成、既に存在するならpass
                # 再起
                recursive_process_files(entry_path, callback)
    
    # 対象ディレクトリのルートで再帰を開始
    recursive_process_files(adjusted_i_dir, encode_file)

if __name__ == "__main__":
    main()