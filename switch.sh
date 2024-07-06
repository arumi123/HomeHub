#!/bin/bash

# Get コマンドの処理
if [ "$1" = "Get" ]; then
    case "$3" in
        "On")
            if [ $? = 0 ]; then
                echo 1
            else
                echo 0
            fi
            ;;
    esac
    exit 0
fi

# Set コマンドの処理
if [ "$1" = "Set" ]; then
    case "$3" in
        "On")
            if [ "$4" = "1" ]; then
                python3 irrp.py -p -g17 -f codes light:on
            else
                python3 irrp.py -p -g17 -f codes light:on
                exit 0
            fi
            ;;
    esac
fi
