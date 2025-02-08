# taglib

pythonでtablibを使いたいとき  

pytaglibはcppライブラリのtaglibを前提としている  

## インストール方法

### windows

### pytaglibの公式通りに [この手順](#以下はよくわからず途中でリタイヤ)で必要な要素があるかも

1. くろーｎ

    ```cmd
    cd build
    git clone git@github.com:supermihi/pytaglib.git
    ```

2. Visual Studio Build Tools 2022のインストール
3. pytaglibのスクリプトを利用してビルド

    ```ps
    # vs build toolsのコンソールかつ仮想環境内で。
    pip install Cython
    cd pytaglib
    python build_native_taglib.py
    python setup.py install
    ```

### 以下はよくわからず途中でリタイヤ

[公式README](https://github.com/taglib/taglib/blob/master/INSTALL.md#windows)

1. Visual Studio Build Tools 2022のインストール
2. scopeのインストール

    ```ps
    iex (new-object net.webclient).downloadstring('https://get.scoop.sh')
    ```

3. cmakeとそのた必要なもの

    ```cmd
    scoop install cmake
    vcpkg install utfcpp zlib cppunit
    ```

4. clone

    ```cmd
    git clone git@github.com:taglib/taglib.git
    ```

5. build
   ディレクトリ設定
        1. TAGLIB_SRC_DIR
        2. TAGLIB_DST_DIR
        3. TAGLIB_DST_DIR

    ```ps
    # Adapt these environment variables to your directories
    $env:TAGLIB_SRC_DIR = "D:\IT\Python\projects\ffmpeg\ffmpeg\build\taglib"
    $env:TAGLIB_DST_DIR = "D:\IT\Python\projects\ffmpeg\ffmpeg\build\taglib\msvs_vcpkg_build"
    cd $env:TAGLIB_SRC_DIR
    cmake -B $env:TAGLIB_DST_DIR -DBUILD_SHARED_LIBS=ON -DVISIBILITY_HIDDEN=ON `
    -DBUILD_TESTING=ON -DBUILD_EXAMPLES=ON -DBUILD_BINDINGS=ON `
    -DCMAKE_BUILD_TYPE=Release `
    -DCMAKE_TOOLCHAIN_FILE="$env:VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake" `
    -G "Visual Studio 17 2022"
    cmake --build $env:TAGLIB_DST_DIR --config Release

    # Add directories containing DLL dependencies to path
    $env:Path += -join(";$env:TAGLIB_DST_DIR\taglib\Release;",
    "$env:TAGLIB_DST_DIR\bindings\c\Release;",
    "$env:VCPKG_ROOT\packages\cppunit_x64-windows\bin;",
    "$env:VCPKG_ROOT\packages\utfcpp_x64-windows\bin;",
    "$env:VCPKG_ROOT\packages\zlib_x64-windows\bin")
    cmake --build $env:TAGLIB_DST_DIR --config Release --target check

    # Install to \pkg folder on current drive
    cmake --install $env:TAGLIB_DST_DIR --config Release --prefix /pkg --strip

    # Static library
    $env:TAGLIB_DST_DIR = "D:\IT\Python\projects\ffmpeg\ffmpeg\build\taglib\msvs_vcpkg_static_build"
    cmake -B $env:TAGLIB_DST_DIR -DBUILD_SHARED_LIBS=OFF -DVISIBILITY_HIDDEN=ON `
    -DBUILD_TESTING=ON -DBUILD_EXAMPLES=ON -DBUILD_BINDINGS=ON `
    -DCMAKE_BUILD_TYPE=Release `
    -DCMAKE_TOOLCHAIN_FILE="$env:VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake" `
    -G "Visual Studio 17 2022"
    cmake --build $env:TAGLIB_DST_DIR --config Release

    cmake --build $env:TAGLIB_DST_DIR --config Release --target check

    # Install to \pkg_static folder on current drive
    cmake --install $env:TAGLIB_DST_DIR --config Release --prefix /pkg_static --strip
    ```
