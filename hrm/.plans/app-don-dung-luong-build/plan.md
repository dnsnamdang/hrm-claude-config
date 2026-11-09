# Dọn dung lượng build TPE_APP (không có số Redmine) — @cuong61n

## Bối cảnh
TPE_APP chiếm 29 GB, code thật khoảng 40 MB. Phần còn lại là file build và cache: `app/build` 19 GB, `.dart_tool` 5,4 GB, `android/app/build` 3,7 GB, `output/` 852 MB.

## Phase 1 — Thư mục output/ chỉ giữ bản build mới nhất
- [x] Rà dung lượng TPE_APP, tìm thư mục nặng (07/11/2026)
- [x] Dọn output/: xoá tpeProd-2.3.5-102.ipa và tpeProd-2.3.6-101.ipa (đã có tpeProd-release.ipa mới hơn), production-release.aab (flavor cũ, đã có tpeProd-release.aab). output/ còn 662 MB, mỗi app và mỗi loại file chỉ còn 1 bản (07/11/2026)
- [x] scripts/build/build_mac.sh `copy_to_output()`: trước khi copy, xoá file cũ cùng flavor và cùng đuôi, kể cả bản có số version do gia hạn TestFlight đặt tên (07/11/2026)
- [x] scripts/build/testflight_renew.sh: trước khi copy IPA, xoá IPA cũ của flavor đó, kể cả tên flavor cũ trước 19/10/2026 (staging→etek, tanphat→etekPower…) (07/11/2026)
- [x] Kiểm tra: `bash -n` và `zsh -n` không lỗi. Chạy thử trên thư mục giả: bản cũ bị xoá, `thanhantest-*` không bị dính khi build `thanhan`, flavor không có tên cũ không lỗi (07/11/2026)
- [ ] Trạng thái: đã sửa ở local nhánh `tpe`, chưa commit. makefile `release_apk`/`release_aab` vốn ghi đè tên cố định nên không phải sửa

## Phase 2 — Chỉ dọn cache CHẾT, giữ cache đang dùng
User chốt không `flutter clean` toàn bộ, vì cache giúp lần build và chạy app sau nhanh hơn. Chỉ xoá phần không bao giờ dùng lại, và tự dọn sau mỗi lần build.
- [x] Thêm scripts/build/clean_stale_cache.sh [--dry-run] [thư mục app/]. Xoá cache Android/iOS/APK/AAB của flavor không còn trong productFlavors (develop, erp, production…), thư mục `.dart_tool/flutter_build` không có file nào được ghi trong 30 ngày, file hot reload `*.cache.dill.track.dill` trừ file mới nhất. Danh sách flavor đọc từ build.gradle, đọc không được thì dừng, không xoá gì (07/11/2026)
- [x] Thêm lệnh `make clean_stale [args=--dry-run]`. Tự gọi ở cuối build_mac.sh và cuối testflight_renew.sh (dọn worktree ~/.tpe-testflight-renew/worktree/app) (07/11/2026)
- [x] Kiểm tra: dry-run liệt kê 270 mục, không mục nào thuộc flavor đang dùng. Chạy thật lấy lại 10,4 GB, TPE_APP từ 29 GB còn 19 GB. Worktree gia hạn TestFlight 3,2 GB toàn cache mới nên không xoá gì (07/11/2026)
- [ ] Trạng thái: đã sửa ở local nhánh `tpe`, chưa commit (clean_stale_cache.sh, build_mac.sh, testflight_renew.sh, makefile)

### Checkpoint — 07/11/2026
Vừa hoàn thành: Phase 1 + Phase 2
Đang làm dở:
Bước tiếp theo: chờ user quyết commit 4 file script
Blocked:
