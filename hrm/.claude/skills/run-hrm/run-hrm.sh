#!/usr/bin/env bash
# Chạy HRM local: MySQL -> API :8000 -> client Nuxt :3000 (Node 14). Idempotent.
set -u

HRM="/Users/nguyentrancu/DEV/code/ERP-HRM/HRM"
NODE14="$HOME/.nvm/versions/node/v14.21.3/bin"
LOGDIR="${TMPDIR:-/tmp}/run-hrm"
mkdir -p "$LOGDIR"
API_LOG="$LOGDIR/api.log"
CLIENT_LOG="$LOGDIR/client.log"

listening() { lsof -iTCP:"$1" -sTCP:LISTEN -n -P >/dev/null 2>&1; }

echo "==> [1/3] MySQL"
if /usr/local/bin/mysql -uroot -h127.0.0.1 -P3306 -e "SELECT 1" >/dev/null 2>&1; then
  echo "    MySQL đã chạy"
else
  brew services start mysql@8.0 >/dev/null 2>&1
  for i in $(seq 1 30); do
    /usr/local/bin/mysql -uroot -h127.0.0.1 -P3306 -e "SELECT 1" >/dev/null 2>&1 && break
    sleep 1
  done
  /usr/local/bin/mysql -uroot -h127.0.0.1 -P3306 -e "SELECT 1" >/dev/null 2>&1 \
    && echo "    MySQL đã lên" || { echo "    !! MySQL không lên được"; exit 1; }
fi

echo "==> [2/3] API :8000"
if listening 8000; then
  echo "    API đã chạy"
else
  ( cd "$HRM/hrm-api" && nohup php artisan serve --host=0.0.0.0 --port=8000 >"$API_LOG" 2>&1 & )
  for i in $(seq 1 20); do listening 8000 && break; sleep 1; done
  listening 8000 && echo "    API đã lên (log: $API_LOG)" || { echo "    !! API không lên — xem $API_LOG"; exit 1; }
fi

echo "==> [3/3] Client Nuxt :3000 (Node 14)"
if listening 3000; then
  echo "    Client đã chạy"
else
  [ -d "$NODE14" ] || { echo "    !! Thiếu Node 14.21.3 ở $NODE14"; exit 1; }
  ( cd "$HRM/hrm-client" && PATH="$NODE14:$PATH" nohup npm run dev >"$CLIENT_LOG" 2>&1 & )
  echo "    Đang compile client (vài phút)... (log: $CLIENT_LOG)"
  for i in $(seq 1 300); do
    if grep -qE "Waiting for file changes|Compiled successfully" "$CLIENT_LOG" 2>/dev/null; then
      echo "    Client compile xong"; break
    fi
    if grep -qE "Failed to compile|ERROR in|Missing binding" "$CLIENT_LOG" 2>/dev/null; then
      echo "    !! Client lỗi build — xem $CLIENT_LOG"; tail -15 "$CLIENT_LOG"; exit 1
    fi
    sleep 2
  done
fi

echo
echo "HRM sẵn sàng:"
echo "  API    : http://localhost:8000"
echo "  Client : http://127.0.0.1:3000   (mở bằng 127.0.0.1, KHÔNG dùng localhost)"
echo "  Logs   : $API_LOG | $CLIENT_LOG"
