#!/bin/bash

#第一引数がGet(ポーリングに使われる)の場合
#第2引数は同じスイッチから複数の機器を指定する際に、
#どの機器について指定するかをさす

if [ "$1" = "Get" ]; then
    case "$3" in
        "On")
            ping -c3 server > /dev/null
            if [ $? = 0 ]; then
                export VAR_NAME="value"
                echo 1
            else
                echo 0
            fi
            ;;
    esac
    exit 0
fi


export MyHeaterCooler_Active 
state = off , cooler , heater , auto
coolertemp = 0～35 （ほんとは16～30）
heatertemp = 0～35 （ほんとは16～30）


#第1引数がSet(状態の変更)の場合
if [ "$1" = "Set" ]; then
    case "$3" in
        "active")
            if [ "$4" = "0" ]; then
                #power off command
                #オフのステート
                exit 0
            fi
            ;;
        "targetHeaterCoolerState")
            if [ "$4" = "1" ]; then
                #Hearter command
                #ヒーターのステート
                exit 0
            elif [ "$4" = "2" ]; then
                #Cooler command
                #クーラーのステート
                exit 0
            else
                #Auto commandでスクリプトで調整することも可能だがめんどすぎるのでやめる
                #オートのステート
                exit 0
            fi
            ;;
        "HeatingThresholdTemperature")
                #$4を温度とするヒーターの温度変更のコマンドを作成する。
                #ヒーター温度のステートを変更する
                exit 0
            ;;
        "CoolingThresholdTemperature")
                #冷房にするコマンド
                python3 irrp.py -p -g17 -f codes HeaterCooler:$4
                #クーラー温度のステートを変更する
                #ステートををクーラーにする
                #オンオフのステートをオンにする
                exit 0
            ;;
    esac
    exit 0
fi