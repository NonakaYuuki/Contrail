# contrail

<br>

## ./src/main.py
飛行データ（CARATSオープンデータ or OpenSkyデータ）と気象データ（MSMデータ or ClimCOREデータ）を用いて、飛行機雲を発生させるフライトの数を計算する。また、飛行機雲が発生しうる空域の可視化も行う。\
```ClimCORE```ライブラリは自作のものなので、自分でパスを通す必要がある。

```Contrail_in_Japan```クラスの入力は、分析したい日時・緯度経度の範囲・高度である。

### ```vis_contrail_MSM()```
MSMデータを使って、飛行機雲が発生しうる空域を可視化する。

### ```vis_contrail_ClimCORE()```
ClimCOREデータを使って、飛行機雲が発生しうる空域を可視化する。

### ```count_flight()```
飛行機雲を発生させうるフライトがいくつあるかを数える。

![test](https://github.com/itoh-lab-aero-ut/contrail/assets/77204155/57c20a88-b4f9-4a51-bde7-0b1ca638088c)


<br>

## ./src/CARATS.py
```path```にCARATSオープンデータ（CSVファイル）へのパスを入力する。
### ```cover_path()```
ある点からある点への飛行経路の間を補完する関数。点と点の間が約0.1度になるように補完される。

### ```rmk_flight_data()```
上記の関数で補完されたフライトデータを返す。

### ```vis_path()```
CARATSオープンデータのフライトデータを可視化する。

<img width="1382" alt="スクリーンショット 2023-10-12 10 23 54" src="https://github.com/itoh-lab-aero-ut/contrail/assets/77204155/753fd5f5-b7df-4e72-9736-107eae8b163e">


<br>

## ./src/flight_data.py
https://github.com/openskynetwork/opensky-api
これに倣って、OpenSkyApiをローカルにインストール必要がある。

https://keisan.casio.jp/exec/system/1526003938
start_timeやend_timeはUNIX時間を入れる。

opensky_api.pyのtimeoutが15秒に設定されており、よくタイムアウトしてエラーが起きるので、45秒など長めに書き換えた方がいいかも。

### ```flightdata_waypoint()```
フライトからそのフライトの通過したウェイポイントの経度・緯度・高度を取得する。

### ```cover_path()```
ある点からある点への飛行経路の間を補完する関数。点と点の間が約0.1度になるように補完される。

### ```rmk_flight_data()```
上記の関数で補完されたフライトデータを返す。

### ```vis_path()```
OpenSkyデータのフライトデータを可視化する。

!['RJTT', 'RJAA', 'RJBB', 'RJFF', 'RJOO', 'RJGG' _12h](https://github.com/itoh-lab-aero-ut/contrail/assets/77204155/2f10fea5-4c15-4c7a-8f58-7fede4f162e9)


<br>

## ./src/vapor_pressure_graph.py
これまでに論文で提案された水の飽和蒸気圧曲線と氷の飽和蒸気圧曲線をグラフにした。\
これらの式は水に対する相対湿度から氷に対する相対湿度への変換に使われる。

![test](https://github.com/itoh-lab-aero-ut/contrail/assets/77204155/b04374e7-4885-4ab3-ba9c-35dcd425d409)


<br>

## ./src/vertical_profile.py
関数```vis_profile(date, hour, lat, lon)```に日時・経度緯度を入力すると、その地点での温度、氷に対する相対湿度の鉛直プロファイルが可視化される。

![20220301_vertical_profile_RJCC](https://github.com/itoh-lab-aero-ut/contrail/assets/77204155/d4c0e8f4-3be0-4de5-a9c6-6db21fb1a805)


<br>

## ./data
download.pyを使用して、ここにMSMデータをダウンロードする。