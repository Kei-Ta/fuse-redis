# Redisでファイルシステムを作る
## 概要
FUSE(Filesystem in Userspace)を利用し、自前のファイルシステムを作成します。今回はRedisを用いてファイルシステムを構築する。機能としてはファイルを作成と削除、書き込みと読み込みをできるようにする。ディレクトリの作成などは機能に含まれてません。

## 設計
ファイルシステムの設計は、redisのgetとsetコマンドを使用し、keyの値をファイル名、valueの値をファイルの中身とする。

## 起動方法
ワーキングディレクトリはpyに移動する。
``` sh
cd py
```

### 1. コンテナをビルドする
``` sh
 docker build -t redis-fuse .  
```
### 2. コンテナを起動する
``` sh
 docker run --privileged -it --rm --name fuse redis-fuse
```

## 動作確認
### 1. コンテナの中に入る
``` sh
 docker exec -it fuse /bin/bash
```

### 2. マウント先に移動する
``` sh
 cd /mnt/redis
```

### 3. ファイルの作成、削除
``` sh
 touch a.txt
```
lsコマンドを実行するとファイルが作成されていることがわかる。
``` sh
 a.txt
```
redisに入って確認してみる。
``` sh
 redis-cli
```
キーを取得すると作成したファイルのキーが存在していることがわかる。
``` sh
 keys *
 1) "a.txt"
```
次にファイルを削除する。
``` sh
 rm a.txt
```
lsコマンドを実行するとファイルが消えていることがわかる。
``` sh
 ls
```
redisからもキーが削除されていることを確認する。
```
 redis-cli
 keys a.txt
 (empty array)
```

### 4. ファイルに書き込み、読み込み
``` sh
 echo "hello world" > b.txt
```
catコマンドを実行するとファイルに値が書き込まれてることがわかる。
``` sh
 cat b.txt
 hello world
```