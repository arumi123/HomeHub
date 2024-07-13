#!/bin/bash

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

if [ "$1" = "Set" ]; then
    case "$3" in
        "On")
            if [ "$1" = "1" ]; then
                python3 home/shun/irrp.py -p -g17 -f codes light:on
                exit 0
            else
                python3 home/shun/irrp.py -p -g17 -f codes light:on
                exit 0
            fi
            ;;
    esac
fi