#!/bin/bash
# Dựng lại HDSD khách hàng bản 1.3 từ bản Drive đã tải về ($1) → out/, cập nhật mục lục bằng Word, gỡ font nhúng, xuất PDF soát.
set -e
H="$(cd "$(dirname "$0")" && pwd)"; OUT="$H/out/HDSD_Danh muc khach hang.docx"
python3 "$H/patch_hdsd_v13.py" "$1" "$OUT"
osascript -e "tell application \"Microsoft Word\"
  open POSIX file \"$OUT\"
  delay 3
  set d to active document
  update table of contents 1 of d
  save d
  close d saving no
end tell"
python3 -c "import sys;sys.path.insert(0,'$H/../../_catalog_docs_lib');from qg_writer import strip_embedded_fonts;print('size',strip_embedded_fonts('$OUT'))"
rm -rf "$H/out/pdf"; mkdir -p "$H/out/pdf"; soffice --headless --convert-to pdf --outdir "$H/out/pdf" "$OUT" >/dev/null 2>&1
