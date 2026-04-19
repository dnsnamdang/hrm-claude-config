# Test Cases UI — BOM List

| Thông tin | Chi tiết |
|-----------|----------|
| Feature | BOM List — Quản lý danh mục hàng hoá giải pháp |
| Ngày tạo | 2026-04-13 |
| Tổng test cases | 98 |

---

## 1. Màn danh sách BOM (`/assign/bom-list`)

### 1.1. Hiển thị & Phân quyền

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-001 | Truy cập danh sách BOM | Đăng nhập user có quyền xem → vào menu BOM Giải pháp | Hiển thị danh sách BOM, filter panel, bảng dữ liệu | High |
| TC-002 | Phân quyền xem tất cả | User quyền "Xem tất cả DS BOM" | Thấy tất cả BOM (trừ Đang tạo của người khác) | High |
| TC-003 | Phân quyền xem theo công ty | User quyền "Xem DS BOM theo công ty" | Chỉ thấy BOM cùng company_id + BOM do mình tạo | High |
| TC-004 | Phân quyền xem theo phòng ban | User quyền "Xem DS BOM theo phòng ban" | Chỉ thấy BOM phòng ban quản lý + BOM do mình tạo | High |
| TC-005 | Phân quyền xem theo bộ phận | User quyền "Xem DS BOM theo bộ phận" | Chỉ thấy BOM bộ phận quản lý + BOM do mình tạo | Medium |
| TC-006 | BOM Đang tạo chỉ người tạo thấy | User A tạo BOM nháp → User B xem danh sách | User B không thấy BOM nháp của User A | High |
| TC-007 | Hiển thị đầy đủ cột | Kiểm tra bảng danh sách | Có đủ: STT, Mã•Tên, Dự án, GP, HM, Version GP/HM, KH, Loại BOM, Trạng thái, Người tạo, Ngày tạo, Cập nhật | Medium |
| TC-008 | Status badge hiện đúng màu | Kiểm tra các BOM ở status khác nhau | Mỗi status hiện badge đúng tên + màu (11 status) | Low |

### 1.2. Bộ lọc

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-009 | Quick search theo mã BOM | Nhập "BOM-2026" vào ô tìm kiếm → Enter | Chỉ hiện BOM có mã chứa "BOM-2026" | High |
| TC-010 | Quick search theo tên BOM | Nhập tên BOM vào ô tìm kiếm | Lọc đúng theo tên | High |
| TC-011 | Filter cascading Dự án → GP → HM | Chọn Dự án → GP tự select → enable HM | GP auto lấy theo dự án, HM lọc theo GP | High |
| TC-012 | Filter Công ty → PB → BP | Chọn Công ty → PB hiện theo công ty → BP hiện theo PB | Cascading đúng | Medium |
| TC-013 | Filter trạng thái | Chọn "Đã duyệt" | Chỉ hiện BOM status=4 | Medium |
| TC-014 | Filter loại BOM | Chọn "Tổng hợp" | Chỉ hiện BOM type=2 | Medium |
| TC-015 | Filter ngày tạo | Chọn khoảng từ/đến | Chỉ hiện BOM created_at trong khoảng | Medium |
| TC-016 | Reset bộ lọc | Click "Đặt lại" | Tất cả filter về mặc định, reload danh sách | Medium |
| TC-017 | Phân trang | Click chuyển trang / đổi số dòng/trang | Phân trang đúng, dữ liệu thay đổi | Medium |
| TC-018 | Sắp xếp theo ngày tạo | Click header cột Ngày tạo | Toggle ASC/DESC đúng | Low |

### 1.3. Row Actions

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-019 | Hover hiện row actions | Hover vào cột Mã•Tên BOM | Buttons actions hiện ra (opacity transition) | Medium |
| TC-020 | Button Xem | Click icon Xem | Chuyển tới `/assign/bom-list/{id}` | High |
| TC-021 | Button Sửa hiện khi status 1/2 | BOM status=1 hoặc 2 + có quyền Tạo BOM | Hiện icon Sửa | High |
| TC-022 | Button Sửa ẩn khi status khác | BOM status=3,4,5,6,7... | Không hiện icon Sửa | High |
| TC-023 | Button Xoá hiện đúng ĐK | BOM status=1 + do mình tạo + có quyền | Hiện icon Xoá | High |
| TC-024 | Button Xoá ẩn khi không đủ ĐK | BOM status≠1 hoặc không phải người tạo | Không hiện icon Xoá | High |
| TC-025 | Xoá BOM | Click Xoá → Xác nhận | BOM bị xoá, biến mất khỏi danh sách | High |
| TC-026 | Button YC xây dựng giá | BOM status=4, type=2 (tổng hợp), không có module | Hiện icon YC xây dựng giá | High |
| TC-027 | YC xây dựng giá thành công | Click YC → Confirm | Toast thành công, BOM chuyển status=7, reload | High |
| TC-028 | Button Lịch sử phê duyệt | BOM status≥7 hoặc có price_requested_at | Hiện icon lịch sử | Medium |
| TC-029 | Xem lịch sử phê duyệt | Click icon lịch sử | Modal timeline hiện đúng các entries | Medium |
| TC-030 | Xuất Excel danh sách | Click "Xuất Excel" header | Download file .xlsx với dữ liệu theo filter + cột hiển thị | Medium |

### 1.4. Tuỳ chỉnh cột

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-031 | Mở modal tuỳ chỉnh cột | Click icon cấu hình cột | Modal hiện danh sách cột, toggle on/off | Low |
| TC-032 | Ẩn/hiện cột | Tắt cột "Hạng mục" | Cột biến mất khỏi bảng, lưu lại khi reload | Low |

---

## 2. Tạo BOM (`/assign/bom-list/add`)

### 2.1. Thông tin BOM

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-033 | Mã BOM tự sinh | Vào trang tạo mới | Mã BOM tự điền format BOM-YYYY-NNNNN, readonly | High |
| TC-034 | Chọn Dự án → auto fill | Chọn Dự án TKT | GP tự select theo dự án, KH tự fill | High |
| TC-035 | Loại BOM thành phần | Chọn "BOM LIST thành phần" | Ẩn nút "Chọn BL con" | High |
| TC-036 | Loại BOM tổng hợp | Chọn "BOM LIST tổng hợp" | Hiện nút "Chọn BL con" | High |
| TC-037 | BOM cấp GP bắt buộc Tổng hợp | GP có hạng mục → không chọn hạng mục | Loại BOM tự chuyển Tổng hợp, disable select | High |
| TC-038 | Chọn tiền tệ | Chọn loại tiền tệ khác VND | Hiển thị đúng mã tiền tệ trong bảng SP | Medium |

### 2.2. Sản phẩm

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-039 | Thêm hàng cha | Click "Thêm sản phẩm" → nhập thông tin → Lưu | Hàng cha hiện trong bảng | High |
| TC-040 | Thêm hàng con | Chọn hàng cha → "Thêm con" → nhập | Hàng con hiện dưới hàng cha, lùi đầu dòng | High |
| TC-041 | Dịch vụ không có con | Thêm SP loại Dịch vụ → thử thêm con | Không hiện nút "Thêm con" | High |
| TC-042 | Dịch vụ clear Model/Brand/Origin | Thêm SP loại Dịch vụ | 3 trường Model, Thương hiệu, Xuất xứ bị clear | Medium |
| TC-043 | Sửa sản phẩm | Click icon Sửa trên row SP | Modal sửa hiện, lưu thay đổi | Medium |
| TC-044 | Xoá sản phẩm | Click icon Xoá → Xác nhận | SP biến mất khỏi bảng | Medium |
| TC-045 | Tính tự động thành tiền | Nhập SL=10, Giá nhập=100,000, Giá bán=150,000 | Thành tiền nhập=1,000,000. Thành tiền bán=1,500,000. Tỷ suất LN=50% | High |

### 2.3. Nhóm hàng

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-046 | Tạo nhóm hàng | Click "Thêm nhóm" → nhập tên | Nhóm hiện trong bảng, STT la mã | Medium |
| TC-047 | Sửa nhóm hàng | Click icon sửa nhóm | Modal sửa tên nhóm | Low |
| TC-048 | Xoá nhóm hàng | Click icon xoá nhóm → Xác nhận | Nhóm bị xoá, SP trong nhóm chuyển về "Chưa phân nhóm" | Medium |

### 2.4. Lưu BOM

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-049 | Lưu nháp thành công | Nhập tối thiểu → Lưu nháp | BOM tạo status=1, redirect danh sách, toast thành công | High |
| TC-050 | Lưu nháp không cần required | Lưu nháp mà không nhập tên/dự án/GP/KH | Lưu được (draft mode bỏ required) | High |
| TC-051 | Lưu BOM thành công | Nhập đầy đủ → Lưu BOM | BOM tạo status=2, redirect, toast | High |
| TC-052 | Lưu BOM thiếu thông tin | Lưu BOM mà thiếu Tên/Dự án/GP/KH | Toast lỗi cụ thể: "Vui lòng nhập tên BOM" | High |
| TC-053 | Tên BOM trùng | Lưu BOM với tên đã tồn tại | Toast: "Tên BOM đã tồn tại" | High |

### 2.5. Import / Export

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-054 | Tải template import | Click Import → Tải template | Download file .xlsx template đúng format | Medium |
| TC-055 | Import sản phẩm | Upload file đúng format → Validate → Import | SP xuất hiện trong bảng BOM | Medium |
| TC-056 | Import file sai format | Upload file sai cấu trúc | Toast lỗi validate cụ thể | Medium |

---

## 3. Sửa BOM (`/assign/bom-list/:id/edit`)

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-057 | Sửa BOM status 1 | Mở edit BOM đang tạo | Cho sửa tất cả thông tin + SP | High |
| TC-058 | Sửa BOM status 2 | Mở edit BOM hoàn thành | Cho sửa tất cả thông tin + SP | High |
| TC-059 | Chặn sửa BOM status khác | Truy cập URL edit BOM status=4 | Toast lỗi + redirect về trang chi tiết | High |
| TC-060 | Lưu sửa thành công | Sửa tên + thêm SP → Lưu | Cập nhật thành công, toast | High |

---

## 4. Chi tiết BOM (`/assign/bom-list/:id`)

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-061 | Xem chi tiết BOM | Click Xem từ danh sách | Hiện đầy đủ thông tin readonly | High |
| TC-062 | Button Quay lại | Click Quay lại | Quay về trang trước đó (history back) | High |
| TC-063 | Button Sửa hiện khi status 1/2 | BOM status=1 hoặc 2 | Hiện button Sửa | High |
| TC-064 | Button Sửa ẩn khi status khác | BOM status=4, 7, 8... | Không hiện button Sửa | High |
| TC-065 | Button Xuất Excel | Click Xuất Excel → chọn fields | Download file .xlsx | Medium |
| TC-066 | Button YC xây dựng giá | BOM tổng hợp cấp GP status=4 | Hiện button, click → confirm → status=7 | High |
| TC-067 | Button YC xây dựng giá ẩn | BOM thành phần hoặc status≠4 | Không hiện button | High |
| TC-068 | Row TỔNG TIỀN | Xem chi tiết BOM có SP | Hiện tổng thành tiền nhập, tổng thành tiền bán, tỷ suất LN% | Medium |

---

## 5. BOM Tổng hợp — Gộp BOM con

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-069 | Chọn BOM con | Tạo BOM tổng hợp → Chọn BL con | Modal hiện DS BOM con cùng dự án + GP | High |
| TC-070 | Validate cùng cấu trúc nhóm | Chọn 2 BOM con: 1 có nhóm, 1 không | Toast lỗi: cấu trúc không khớp | High |
| TC-071 | Validate cùng tiền tệ | Chọn BOM con tiền tệ khác | Toast lỗi: tiền tệ không khớp | High |
| TC-072 | Gộp không cộng qty | Chọn BOM con có SP trùng mã | SP trùng giữ nguyên 2 dòng riêng, KHÔNG gộp SL | High |
| TC-073 | BOM cấp GP chỉ chọn BOM HM đã duyệt | Tạo BOM tổng hợp cấp GP | Chỉ hiện BOM tổng hợp hạng mục status=4 | High |
| TC-074 | Unique aggregate per version | Tạo BOM tổng hợp thứ 2 cùng GP + version | Toast lỗi: đã có BOM tổng hợp trên version này | High |

---

## 6. Xây dựng giá (`/assign/bom-list/:id/pricing`)

### 6.1. Giao diện

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-075 | Truy cập màn pricing | Từ DS chờ XD giá → click BOM | Mở trang pricing, chỉ unlock Giá nhập + Giá bán | High |
| TC-076 | Các cột khác readonly | Kiểm tra các input: Tên, SL, ĐVT, Thông số... | Tất cả readonly trừ giá nhập + giá bán | High |
| TC-077 | Thu gọn card thông tin | Click "Thu gọn thông tin" | Card thông tin BOM ẩn, bảng SP chiếm full | Medium |
| TC-078 | Footer realtime | Nhập giá → kiểm tra footer | Tổng nhập, Tổng bán, Tỷ suất LN%, Cấp duyệt dự kiến cập nhật realtime | High |
| TC-079 | Quy đổi VNĐ hiện khi currency khác | BOM dùng USD (exchange_rate=25000) | Footer hiện thêm dòng "Quy đổi VNĐ: xxx" | Medium |
| TC-080 | Cấp duyệt dự kiến | Nhập giá sao cho V≤1B, M≥20% | Badge "Cấp 1 — Tự duyệt" hiện ở footer | High |

### 6.2. Lưu nháp

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-081 | Lưu nháp giá | Nhập giá → Lưu nháp | Toast thành công, redirect về DS chờ XD giá, status=8 | High |
| TC-082 | Lưu nháp giá = 0 | Để giá = 0 → Lưu nháp | Cho lưu (nháp không validate giá > 0) | Medium |

### 6.3. Gửi duyệt

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-083 | Gửi duyệt — validate giá = 0 | Để 1 SP giá nhập = 0 → Gửi duyệt | Toast lỗi: "SP xxx chưa có giá nhập" | High |
| TC-084 | Gửi duyệt — Cấp 1 tự duyệt | Nhập giá V≤1B + M≥20% → Gửi duyệt | Popup "Bạn có thể tự duyệt" → Confirm → status=11 | High |
| TC-085 | Gửi duyệt — Cấp 2 TP | Nhập giá V=5B → Gửi duyệt | Popup "Cần gửi tới Trưởng phòng" → Confirm → status=9 | High |
| TC-086 | Gửi duyệt — Cấp 3 BGĐ | Nhập giá V=25B → Gửi duyệt | Popup "Cần gửi tới Ban giám đốc" → Confirm → status=10 | High |
| TC-087 | Gửi duyệt — Huỷ popup | Popup hiện → Click Huỷ | Không đổi status, giữ nguyên trang pricing | High |
| TC-088 | Gửi duyệt — M thấp overrides V | V≤1B nhưng M=5% | Cấp 3 (MAX(1,3)=3) → popup BGĐ | High |

---

## 7. Duyệt giá

### 7.1. DS BOM chờ XD giá (`/assign/bom-list/pending-pricing`)

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-089 | Truy cập DS chờ XD giá | User có quyền "Xây dựng giá" → menu Phê duyệt | Hiện DS BOM status 7, 8 | High |
| TC-090 | Cột hiển thị đầy đủ | Kiểm tra bảng | STT, Mã•Tên, Dự án, GP, Version GP, Phòng GP, PM, Phòng KD, NV KD, KH, Người YC, Ngày YC, Trạng thái | Medium |
| TC-091 | Row actions hover | Hover vào row | Hiện: Xây dựng giá, Xem chi tiết, Lịch sử | Medium |
| TC-092 | Xuất Excel | Click Xuất Excel | Download file .xlsx với data theo filter | Medium |

### 7.2. DS BOM chờ duyệt giá (`/assign/bom-list/pending-price-approval`)

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-093 | TP chỉ thấy status 9 | User có quyền TP duyệt giá | Chỉ hiện BOM status=9 | High |
| TC-094 | BGĐ thấy status 9 + 10 | User có quyền BGĐ duyệt giá | Hiện BOM status 9 và 10 | High |
| TC-095 | Duyệt giá từ danh sách | Click icon Duyệt (xanh) → Confirm | Toast thành công, BOM status→11, biến mất khỏi DS | High |
| TC-096 | Từ chối giá từ danh sách | Click icon Từ chối (đỏ) → Nhập lý do → Confirm | Toast thành công, BOM status→8, biến mất khỏi DS | High |
| TC-097 | Từ chối không nhập lý do | Click Từ chối → Để trống lý do → OK | Button OK disabled, không cho submit | High |

### 7.3. Duyệt giá từ trang chi tiết

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-098 | Button Duyệt giá hiện cho TP | User TP → xem BOM status=9 | Footer hiện "Duyệt giá" + "Từ chối giá" | High |
| TC-099 | Button Duyệt giá hiện cho BGĐ | User BGĐ → xem BOM status=10 | Footer hiện "Duyệt giá" + "Từ chối giá" | High |
| TC-100 | Button ẩn khi không có quyền | User thường → xem BOM status=9 | Không hiện button Duyệt/Từ chối | High |
| TC-101 | Duyệt giá từ chi tiết | Click Duyệt giá → Confirm | Toast thành công, trang reload, status=11 | High |
| TC-102 | Từ chối từ chi tiết | Click Từ chối → Nhập lý do → Confirm | Toast thành công, reload, status=8 | High |

---

## 8. Cấu hình duyệt giá (`/assign/settings/price-approval`)

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-103 | Truy cập trang cấu hình | User có quyền cấu hình → menu Cấu hình | Hiện 2 bảng: Giá trị ĐH + Tỷ suất LN + audit log | High |
| TC-104 | Giá trị ĐH — format tiền | Kiểm tra input "Đến" cấp 1 | Hiển thị format dấu phẩy (1,000,000,000) | Medium |
| TC-105 | Giá trị ĐH — auto sync | Sửa "Đến" cấp 1 = 2B | "Từ" cấp 2 tự cập nhật = 2B | High |
| TC-106 | Giá trị ĐH — cấp 1 Từ readonly | Kiểm tra input "Từ" cấp 1 | Disabled, giá trị = 0 | Medium |
| TC-107 | Tỷ suất LN — sửa Từ cấp 1 | Sửa "Từ" cấp 1 = 25% | "Đến" cấp 2 auto = 25% | High |
| TC-108 | Tỷ suất LN — sửa Từ cấp 2 | Sửa "Từ" cấp 2 = 15% | "Đến" cấp 3 auto = 15% | High |
| TC-109 | Tỷ suất LN — cấp 3 Từ = −∞ | Kiểm tra cấp 3 | "Từ" hiện "Không giới hạn" (bao gồm giá trị âm) | High |
| TC-110 | Mô tả auto generate | Sửa ngưỡng → kiểm tra cột Mô tả | Tự sinh: "Người làm giá (tự duyệt) (V ≤ 2,000,000,000)" | Medium |
| TC-111 | Lưu cấu hình thành công | Sửa ngưỡng → Lưu | Toast thành công, audit log ghi entry mới | High |
| TC-112 | Validate Từ ≥ Đến | Sửa "Đến" cấp 1 nhỏ hơn "Từ" → Lưu | Toast lỗi validate | Medium |
| TC-113 | Audit log hiển thị | Xem section lịch sử thay đổi | Hiện timeline: người sửa, thời gian, old→new | Medium |

---

## 9. Lịch sử phê duyệt

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-114 | Modal lịch sử từ DS BOM | Click icon lịch sử trên row | Modal hiện timeline actions | High |
| TC-115 | Modal lịch sử từ trang chi tiết | Click "Lịch sử phê duyệt" footer | Modal hiện timeline | High |
| TC-116 | Hiển thị đầy đủ entries | BOM đã qua nhiều actions | Mỗi entry: icon, action label, người thực hiện, status change, thời gian | Medium |
| TC-117 | Entry từ chối hiện lý do | BOM bị từ chối → xem lịch sử | Entry reject hiện note lý do (background đỏ nhạt) | Medium |
| TC-118 | Entry hiện cấp duyệt | BOM gửi duyệt cấp 2 | Entry submit hiện badge "Cấp 2" | Low |

---

## 10. Notification

| # | Test Case | Steps | Expected | Priority |
|---|-----------|-------|----------|----------|
| TC-119 | Notify khi YC xây dựng giá | PM click YC xây dựng giá | Users có quyền "Xây dựng giá" nhận notification bell | High |
| TC-120 | Notify khi gửi duyệt cấp 2 | Gửi duyệt → cấp 2 | Users có quyền TP nhận notification | High |
| TC-121 | Notify khi gửi duyệt cấp 3 | Gửi duyệt → cấp 3 | Users có quyền BGĐ nhận notification | High |
| TC-122 | Notify khi duyệt giá | TP/BGĐ duyệt | Người làm giá nhận notification "Đã duyệt" | High |
| TC-123 | Notify khi từ chối giá | TP/BGĐ từ chối | Người làm giá nhận notification "Bị từ chối" | High |

---

## Tổng kết

| Nhóm | Số TC | High | Medium | Low |
|------|-------|------|--------|-----|
| Danh sách BOM | 32 | 16 | 13 | 3 |
| Tạo BOM | 24 | 14 | 8 | 2 |
| Sửa BOM | 4 | 4 | 0 | 0 |
| Chi tiết BOM | 8 | 5 | 2 | 1 |
| Gộp BOM | 6 | 6 | 0 | 0 |
| Xây dựng giá | 14 | 11 | 3 | 0 |
| Duyệt giá | 14 | 12 | 1 | 1 |
| Cấu hình | 11 | 5 | 5 | 1 |
| Lịch sử | 5 | 2 | 2 | 1 |
| Notification | 5 | 5 | 0 | 0 |
| **Tổng** | **123** | **80** | **34** | **9** |
