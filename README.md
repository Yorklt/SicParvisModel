# Sic Parvis Model
これはBlenderのアドオンです。
Blenderの標準のFBXエクスポーターを使って、キャラクター用のFBXを出力します。
<br>
<br>
3Dモデルをゲームエンジン向けに作る際には、どうしてもトライ＆エラーが必要で、
なんどもFBXを出力することになりますが、その時にすべて手動でやっていると、
ミスが起こりますし時間がかかってしまいます。
このアドオンはそれを少しだけ解消します。
<br>
<br>
特徴
<br>
・オブジェクト（形状）だけのFBXと、アニメーションだけのFBXを分けて出力できます。
<br>
・コレクション別にFBXをまとめて複数出力できます。<br>
　例えば、サブパーツ違いのキャラクターがいて、パーツを変えながら複数のFBXを<br>
　出力したいときなどに使用できます。
<br>
・アンダースコア(_)で始まる名前のオブジェクトを、出力から除外できます。<br>
　Blendファイル内にアタリ用のダミーデータが入っていて、それを無視して出力したいときなどに使用できます。
<br>
・名前に関わらず、カメラとライトは出力から除外されます。
<br>
<br>
出力設定は、RPG Developer Bakinでの使用を想定しています。RPG Developer Bakinは株式会社スマイルブームさんの製品です。


# インストール
ZIPファイルは解凍しなくて大丈夫です。
Blenderのプリファレンス（ユーザー設定）から、「アドオン」を選んで、「インストール」ボタンを押します。
ダウンロードしたZIPファイルを指定します。
すると「テスト中」タブの中に、このアドオンが表示されるようになるので、チェックボックスにチェックを入れてください。

# 使い方
Blenderのメニューから、「ファイル」＞「エクスポート」を選んでください。

# 注意
このアドオンを実行すると、オブジェクトの可視設定や選択状態、および、現在のフレームが変更されます。
気になる場合は、実行後にBlendファイルを開きなおしてください。

