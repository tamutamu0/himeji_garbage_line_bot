# 概要

## 参考リンク
[DockerでPython実行環境を作ってみる](https://qiita.com/jhorikawa_err/items/fb9c03c0982c29c5b6d5)

## ゴミの日

### 使用API

**エリア**

https://admin.gomisuke.jp/app/0083/data/files/1-1/area.plist
https://admin.gomisuke.jp/app/0083/data/files/1-2/area.plist
https://admin.gomisuke.jp/app/0083/data/files/1-3/area.plist
https://admin.gomisuke.jp/app/0083/data/files/1-4/area.plist

**カレンダー**

https://admin.gomisuke.jp/app/0083/data/files/1-1/calendar.plist
https://admin.gomisuke.jp/app/0083/data/files/1-2/calendar.plist
https://admin.gomisuke.jp/app/0083/data/files/1-3/calendar.plist
https://admin.gomisuke.jp/app/0083/data/files/1-4/calendar.plist

## コマンド

コンテナに入る: docker compose exec python3 bash
ビルド：docker compose build
起動: docker compose up --build
curl: curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'