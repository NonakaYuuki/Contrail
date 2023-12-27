# contrail

## 飛行機雲形成エリアの可視化方法
### 1.　気象データのダウンロード
以下のコマンドでMSMデータをダウンロードする。\
$ ```python data/MSM_download.py```

以下のURLからClimCOREデータを```./data/ClimCORE```にダウンロードする。\
http://www.atmos.rcast.u-tokyo.ac.jp/miyasaka/data/eriitoh_20230927.jBPbpdXGdUjQ/

### 2.　飛行機雲形成エリアの可視化
$ ```python3 src/main.py ```

<br>

## ./src/main.py
飛行データ（CARATSオープンデータ or OpenSkyデータ）と気象データ（MSMデータ or ClimCOREデータ）を用いて、飛行機雲を発生させるフライトの数を計算する。また、飛行機雲が発生しうる空域の可視化も行う。\

```Contrail_in_Japan```クラスの入力は、分析したい日時・緯度経度の範囲である。

### ```vis_contrail_MSM()```
MSMデータを使って、飛行機雲が発生しうる空域を可視化する。

### ```vis_contrail_ClimCORE()```
ClimCOREデータを使って、飛行機雲が発生しうる空域を可視化する。

### ```count_flight()```
飛行機雲を発生させうるフライトがいくつあるかを数える。


<br>

## ./src/ClimCORE.py
ClimCOREクラスに年・月・日・時・緯度（度）・経度（度）・気圧高度（feet）を引数として入力する。\
そして、下記の関数を実行することによって、入力した日時、場所の気象データを出力として得ることができる。\
ちなみに出力はxarray.datasetの型で出力される。\

### ```Pressure（）```
気圧を出力する関数。（hPa）

### ```RHi（）```
氷に対する相対湿度を出力する関数。（％）

### ```Temperature（）```
温度を出力する関数。（K）

### ```U_Wind（）```
東西方向の風速を出力する関数。西風が正。（m/s）

### ```V_Wind（）```
南北方向の風速を出力する関数。南風が正。（m/s）

<br>

## ※　xesmfのインストール＆importに手こずった時
xesmf_envという名前の仮想環境をcondaによって作成する。\
$ ```conda create -n xesmf_env```

xesmf_env仮想環境に入る。\
$ ```conda activate xesmf_env```

xesmfをインストール\
$ ```conda install -c conda-forge xesmf```\
$ ```conda install -c conda-forge dask netCDF4```

<br>

## ./src/CARATS.py
```path```にCARATSオープンデータ（CSVファイル）へのパスを入力する。
### ```cover_path()```
ある点からある点への飛行経路の間を補完する関数。点と点の間が約0.1度になるように補完される。

### ```rmk_flight_data()```
上記の関数で補完されたフライトデータを返す。

### ```vis_path()```
CARATSオープンデータのフライトデータを可視化する。

<br>

## ./src/vapor_pressure_graph.py
これまでに論文で提案された水の飽和蒸気圧曲線と氷の飽和蒸気圧曲線をグラフにした。\
これらの式は水に対する相対湿度から氷に対する相対湿度への変換に使われる。

<br>

## ./src/vertical_profile.py
関数```vis_profile(date, hour, lat, lon)```に日時・経度緯度を入力すると、その地点での温度、氷に対する相対湿度の鉛直プロファイルが可視化される。
