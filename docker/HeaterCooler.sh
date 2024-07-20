#!/bin/bash

#第一引数がGet(ポーリングに使われる)の場合
#第2引数は同じスイッチから複数の機器を指定する際に、
#どの機器について指定するかをさす

if [ "$1" = "Get" ]; then
    case "$3" in
        "On")
            ping -c3 server > /dev/null
            if [ $? = 0 ]; then
                echo 1
            else
                echo 0
            fi
            ;;
    esac
    exit 0
fi



#第1引数がSet(状態の変更)の場合
if [ "$1" = "Set" ]; then
    case "$3" in
        "active")
            if [ "$4" = "1" ]; then
                #power on command
                exit 0
            else
                #power off command
                exit 0
            fi
            ;;
        "targetHeaterCoolerState")
            if [ "$4" = "1" ]; then
                #Hearter command
                exit 0
            else
                #Cooler command
                exit 0
            fi
            ;;
        "currentTemperature")
                #$4を温度とする温度変更のコマンドを作成する。
                exit 0
            ;;
    esac
    exit 0
fi