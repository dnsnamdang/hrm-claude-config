#!/bin/bash
# Dọn DB về trạng thái sau prep + khởi động lại app về màn chọn phân hệ.
cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/hrm-api
PREP=$HOME/.cache/tpe-video-work/prep_mytodo.json SINCE="${SINCE:-2026-11-09 00:05:00}" /opt/homebrew/opt/php@7.4/bin/php artisan tinker \
  --execute="$(cat /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/app-video-huong-dan/video/tools/reset_mytodo.php)" 2>&1 | grep -v "imagick\|Deprecated\|^$\|Warning"
P=$(ps -A -o pid,command | grep "flutter_tools.snapshot run" | grep "8001" | grep -v grep | awk '{print $1}' | head -1)
[ -n "$P" ] && kill -USR2 $P && sleep 7
