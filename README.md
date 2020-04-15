# openpose_write

## 概要
openposeで取得したjsonファイルをcsvに書き出す
- 画像（一つのファイルを部位ごとに書き出す）
- 動画（時系列通りに複数のファイルを書き出すもの）

__オプション__
- 頭・手の部位書き出しをするかどうか

## 使い方
1. 画像（write_by_images.py）と動画（write_by_mov.py）を選ぶ
2. jsonファイルが入っているフォルダを指定
3. オプションを選択（頭と顔を書き出すかどうか、書き出す場合は１　スペース区切り）
4. pythonファイルと同じ階層にresult.csvが書き出される
## 参考　
- [openpose（本家)](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
- [Kim Biology & Informatics](https://kimbio.info/openpose%E3%81%AEjson%E5%BD%A2%E5%BC%8F%E3%82%92csv%E3%81%AB%E5%A4%89%E6%8F%9B%E3%81%99%E3%82%8B)
