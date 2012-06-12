#!/bin/bash
export APACHE_RUN_USER=www-data
export APACHE_RUN_GROUP=www-data
export APACHE_PID_FILE=/var/run/apache2.pid
export LANG=C
export LANG

apache2 -f /pentest/web/xssfuzz/apache2.conf -k start

zenity --info --text "Apache2 started on *:8080"
