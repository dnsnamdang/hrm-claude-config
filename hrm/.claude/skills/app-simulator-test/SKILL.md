---
name: app-simulator-test
description: Quy trình test E2E TPE_APP trên iOS simulator bằng mobile-mcp TRƯỚC khi báo xong — từng bước một, mỗi thao tác chạy step.sh (chụp màn đúng toạ độ + soi lỗi Flutter ẩn trong run.log + API lỗi), ma trận trạng thái (tổ hợp nhóm mở, lọc ra 0 dòng, bấm 2 lần, đổi tab rồi quay lại, kéo tải lại), mọi trạng thái phải có lối quay ra, lỗi BE / mất mạng, dữ liệu biên, nhiều tài khoản quyền khác nhau, trả dữ liệu. Kèm cách chạy app (fvm, flavor tpeLocal / tpeDev), hot reload, bàn phím ảo, thử push. Dùng khi vừa sửa app xong, khi user nói "test kỹ", "test e2e", "chạy thử", "xem trên simulator", "sao bấm không được", "bị đơ".
---

# Test E2E trên simulator — TPE_APP

**User chốt 29/10 + 31/10/2026: "test thật kỹ, thao tác từng bước từng bước một, bảo đảm không có lỗi".**
Báo xong = đã BẤM THẬT từng bước theo mục 3–5, mỗi bước có ảnh + `step.sh` sạch lỗi. `analyze` sạch KHÔNG phải test.

### Lỗi đã lọt vì test hời hợt (đọc để biết mình hay sót chỗ nào)

| Lỗi lọt tới user | Vì sao test không thấy | Luật chặn (mục) |
|---|---|---|
| Việc của tôi đơ cả tab (31/10): 1 việc nằm cả "Hôm nay" lẫn "Tuần này", key trùng → ListView vỡ | Chỉ mở từng nhóm một; bản debug in lỗi ra log nhưng vẫn vẽ → nhìn ảnh tưởng ổn | Soi log mỗi bước (2), tổ hợp trạng thái (4b) |
| Bấm nút lọc vai trò ra 0 dòng → mất luôn dòng Tổng + nút, không bỏ lọc được (31/10) | Chỉ thử lọc ra có dữ liệu | Mọi trạng thái có lối quay ra (4a), dữ liệu 0 dòng (4d) |
| Lưu biên bản meeting báo "Vui lòng kiểm tra dữ liệu nhập" mà không ô nào đỏ (30/10) | Không thử dữ liệu cũ (hạn đã qua) + lỗi ở tab khác | Dữ liệu biên (4d), lỗi BE (4c) |
| Bàn phím che nút Lưu; "Làm mới" bộ lọc không xoá; nút thiếu icon (29/10) | Gõ bằng bàn phím Mac; không bấm hết nút | Bàn phím ảo (1), bấm MỌI nút (3) |

## 1. Chạy app

- Luôn `fvm` (Flutter 3.41.7), chạy nền 1 lần, giữ suốt phiên (log là nguồn soi lỗi — PHẢI ghi ra file):
  `cd TPE_APP/app && ~/fvm/versions/3.41.7/bin/flutter run --debug -t lib/main.dart --flavor tpeLocal --dart-define=FLAVOR=tpeLocal -d <UDID> > <scratchpad>/run.log 2>&1`
- `tpeLocal` → `127.0.0.1:8000` (`HRM/hrm-api`, kiểm `lsof -iTCP:8000 -sTCP:LISTEN`). Cần dữ liệu dev → `tpeDev`
  (đổi flavor = dừng tiến trình cũ rồi chạy lại, không chạy 2 cái song song). Xong việc trên dev → quay về `tpeLocal`.
- Hot reload `kill -USR1 $(pgrep -f "flutter_tools.*run --debug"|head -1)`; đổi `main`/khởi tạo/state đang hỏng →
  hot restart `-USR2`. Thêm route / DI / freezed → `make gen` rồi chạy lại. **Sau hot reload, màn đang mở có thể chưa
  nhận code mới** (State giữ nguyên) → kéo tải lại / thoát vào lại rồi mới kết luận.
- Màn đỏ còn sót từ lỗi cũ thì hot reload không gỡ → hot restart, test lại từ đầu luồng.
- Lỗi link `SAMKeychain`: `make fix_pod_dev` + `pod install` (ngoài sandbox), xong `git checkout app/ios/Podfile`.
- Agent chạy nền KHÔNG build / bật simulator / `build_runner`.
- **Bàn phím ảo:** simulator nối bàn phím Mac thì KHÔNG hiện bàn phím ảo → test form phải ngắt ⇧⌘K. Trả lại cho user: ⇧⌘K lần nữa.

## 2. Vòng lặp 1 bước — BẮT BUỘC sau MỌI thao tác

```
thao tác (mobile-mcp: 1 chạm / 1 vuốt / 1 lần gõ)
→ bash .claude/skills/app-simulator-test/step.sh <run.log> "<tên bước>" [giây chờ]
→ Read ảnh step.sh vừa in → so với KẾT QUẢ MONG ĐỢI viết TRƯỚC khi bấm
→ ✅ cả 3 (ảnh đúng · không lỗi Flutter mới · API đúng) mới sang bước sau
```

- **`step.sh`** chụp màn thu về rộng 393 → **toạ độ trên ảnh = toạ độ chạm**, không nhân hệ số (đã chạm trượt
  sang nhóm bên dưới vì nhân sai). Ưu tiên `mobile_list_elements_on_screen` + chạm theo `ref` khi phần tử có trong
  cây; cây có thể chứa phần tử của màn ẩn (IndexedStack, màn trước lệch x=−130) — đối chiếu với ảnh.
- **Có dòng "❌ LỖI FLUTTER MỚI" = bước FAIL dù ảnh trông bình thường.** Bản debug in lỗi rồi vẽ tiếp; bản release
  (TestFlight) cùng lỗi đó = đứng hình / ô xám / mất tương tác. Đọc đoạn log được chỉ ra, tìm nguyên nhân, sửa.
- **Thao tác không có phản ứng** (ảnh không đổi) → KHÔNG giả định chạm trượt rồi bỏ qua: chụp lại, kiểm toạ độ
  bằng cây phần tử, thử lại 1 lần; vẫn không ăn → đó là lỗi (nút chết / bị che / màn đơ), điều tra.
- "⚠️ API LỖI" → màn phải hiện câu lỗi đúng chỗ (dưới ô / toast có nội dung), tắt trạng thái đang tải, bấm lại được.
- Mỗi bước 1 thao tác. Gom nhiều chạm vào `mobile_batch_commands` CHỈ khi đã test từng bước luồng đó rồi và đang
  chạy lại để tái hiện; batch xong vẫn phải `step.sh`.

## 3. Kịch bản gốc theo loại màn (bấm MỌI nút, MỌI ô có trên màn)

**Form** (`app-form`), bàn phím ảo BẬT:
1. Gõ ô 1 dòng → Enter sang ô sau. 2. Ô nhiều dòng → chạm vùng trống → bàn phím đóng, thấy nút Lưu.
3. Vuốt form khi bàn phím mở → đóng. 4. Chạm ô chỉ đọc khi đang gõ → đóng. 5. Danh sách gõ nhanh: Enter và ➕ đều
thêm, bàn phím giữ. 6. Để trống bắt buộc → Lưu → lỗi đỏ ĐÚNG ô (BE trả) + toast nói rõ thiếu gì. 7. Sửa → ‹ → hỏi
chưa lưu. 8. Lưu thật → về màn trước, kiểm DB (`mysql -uroot local_hrm_erp`). 9. Mở lại bản ghi vừa lưu → đủ giá trị.

**Danh sách** (`app-list-page`): mở lọc → chọn → Xem N → chip + badge đúng; ✕ chip; **Làm mới → Xem kết quả → hết
lọc**; tìm ra 0 → "Không có dữ liệu phù hợp." + vẫn còn ô tìm / nút lọc / nút vai trò để bỏ; kéo tải lại; cuộn
cuối trang → tải trang 2 (không lặp dòng); bấm thẻ → chi tiết → sửa → quay lại thấy mới.

**Chi tiết / Hub** (`app-detail-page`): đủ trạng thái (nháp / đang chạy / đã xong / huỷ / không quyền) → đúng nút,
khớp nút màn danh sách; mọi thao tác ghi có hỏi; lưu ở màn con → quay lại thấy mới; menu ⋮ bấm hết mục.

**Khung / chung:** đổi tab con, tab đáy (không giật); màu + vân + chuông đúng phân hệ ở màn con; nút có icon; thanh
nút không cắt chữ (màn 393pt).

**Thông báo** (`app-notification`): bấm từng loại → đúng màn; push trên màn hình khoá (`simctl push`); app đang tắt
→ bấm push mở đúng màn.

## 4. Ma trận bắt buộc — làm SAU kịch bản gốc (đây là chỗ hay sót)

**4a. Mọi trạng thái phải có lối quay ra.** Với từng nút bật/tắt, lọc, nhóm mở/đóng, tab, chế độ xem: bật → kiểm
→ TẮT lại → kiểm về đúng như cũ. Đặc biệt khi trạng thái đó cho ra 0 dòng / lỗi / màn trống: điều khiển để thoát
(nút lọc, ✕ chip, dòng Tổng, nút vai trò, ‹) phải VẪN CÒN trên màn.

**4b. Tổ hợp trạng thái** — đừng chỉ thử từng cái một:
- Mở NHIỀU nhóm / khối cùng lúc (tất cả nhóm của danh sách nhóm), rồi đóng 1 nhóm, tick 1 việc, kéo tải lại.
- 1 bản ghi xuất hiện ở 2 chỗ trên cùng màn (Hôm nay + Tuần này, 2 ngày của việc nhiều ngày) → thao tác lên nó.
- Lọc + tìm + vai trò cùng bật → bỏ từng cái theo thứ tự khác nhau.
- Đổi tab con rồi quay lại (IndexedStack giữ state) · sang màn khác rồi ‹ về · tắt hẳn app mở lại (lọc đã lưu
  còn, không kẹt trạng thái 0 dòng).
- Thao tác xong (tick / lưu / xoá) → mọi nơi hiển thị bản ghi đó (2 tab, đếm số, badge chuông) cập nhật đúng.

**4c. Bấm nhanh & lỗi:**
- Chạm 2 lần liên tiếp nhanh vào: nút Lưu / Hoàn thành / Xoá, nút trong hộp thoại xác nhận, ô tick, thẻ (mở 2 màn?).
- Lỗi BE: dữ liệu sai để BE trả 422 → lỗi đúng ô; 403 (tài khoản không quyền); 500/mất mạng (tạm dừng
  `php -S` hoặc tắt mạng simulator) → câu lỗi + tắt đang tải + bấm lại được, KHÔNG kẹt màn.

**4d. Dữ liệu biên** (tạo trước bằng SQL/tinker, tiền tố `[TEST-…]`): 0 dòng · 1 dòng · nhiều trang · tên rất dài
(cắt chữ, không tràn) · trường null/rỗng · mốc ngày (quá hạn, hôm nay, ngày mai, cuối tuần, tuần sau) · dữ liệu
cũ không còn hợp lệ với rule mới (hạn đã qua, danh mục đã khoá) · việc nhiều ngày.

**4e. Nhiều tài khoản** (memory "Test là test như testcase"): ít nhất 1 TK đủ quyền + 1 TK thiếu quyền → nút ẩn
đúng, API không lộ dữ liệu. TK local: namdangit@gmail.com / 2025Dns@2 (user 13); TK thường `Test@123` (memory
"TK test local meeting"). Local được đổi mật khẩu TK khác, trừ namdangit.

## 5. Kết thúc

- Chạy lại TOÀN BỘ luồng chính 1 lần cuối từ hot restart, mỗi bước `step.sh` — bản sửa lỗi này hay làm hỏng chỗ khác.
- Trả dữ liệu đã đổi trên dev về như cũ (local thì tuỳ, ghi rõ). Prod: không ghi khi chưa hỏi.
- Để nguyên simulator + app (memory "Giữ simulator sau test"). **User đang dùng simulator** (màn đổi giữa 2 lần
  chụp, có chữ mình không gõ) → DỪNG ngay, chỉ báo cách xem.
- Báo cáo: bảng `bước → kết quả mong đợi → thực tế → lỗi log` (số bước, số bước FAIL đã sửa); ghi rõ cái CHƯA thử
  (Android, TK không quyền, mất mạng…). Không viết "đã test kỹ" khi còn mục 4 chưa làm. Ghi vào plan.md.
