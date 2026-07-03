# Tổng hợp thay đổi — Phase 31: Logic hàng hoá cha-con (BOM + Báo giá)

> Phạm vi: màn **BOM** (`/assign/bom-list` tạo/sửa) và **Báo giá** (`/assign/quotations` tạo/sửa, loại tự tạo + từ BOM).
> Ngày: 2026-06-09.

## ⚙️ Chuẩn bị trước khi test (BẮT BUỘC)
1. **Chạy migration** (repo API): `php artisan migrate` — thêm cột `show_children`. (Chưa chạy thì tính năng ẩn/hiện con + export sẽ sai.)
2. **Build/restart FE** (Nuxt) + **hard-refresh** trình duyệt (Ctrl/Cmd+Shift+R).
3. Chuẩn bị 2 tài khoản: **CÓ** quyền *"Xem giá vốn hàng hoá"* và **KHÔNG** có quyền — để test phần phân quyền.
4. Chuẩn bị 1 mã hàng ERP **có công thức ghép bộ** (ví dụ id 14329 — "Bộ bàn ghế ENEOS", có 2 hàng con) và 1 mã ERP **không có** công thức ghép bộ.

---

## 1. Hàng cha là hàng ERP CÓ công thức ghép bộ (recipe)

**Thay đổi:** Khi chọn 1 hàng ERP là bộ ghép làm hàng cha → hệ thống **tự nạp hàng con** theo công thức ghép bộ trong ERP. Hàng con **khoá hoàn toàn** (không thêm/bớt/sửa).

**Test:**
- [ ] Chọn hàng ERP có recipe làm hàng cha → các hàng con tự xuất hiện bên dưới (đúng số con + đơn giá lấy từ ERP).
- [ ] Hàng cha ERP **KHÔNG có** nút "Thêm con".
- [ ] Ô **số lượng hàng con bị khoá** (không sửa được); ô giá hàng con khoá (lấy từ ERP).
- [ ] **Đổi số lượng hàng cha** → số lượng hàng con **tự nhân lại** đúng theo công thức (vd cha có 4 ghế/bộ, tăng cha lên 2 → 8 ghế).
- [ ] Lưu rồi mở lại → đổi số lượng cha vẫn nhân đúng.

## 2. Hàng ERP KHÔNG có công thức ghép bộ
**Test:**
- [ ] Chọn hàng ERP không có recipe → là **hàng lẻ**, không có hàng con, không có nút "Thêm con".

## 3. Nút "Ẩn / Hiện con" (chỉ với hàng cha ERP)
**Thay đổi:** Mỗi hàng cha ERP có nút mắt (Ẩn con / Hiện con). Đây là cờ hiển thị, **KHÔNG xoá dữ liệu con**.

**Test:**
- [ ] Bấm "Ẩn con" → hàng con biến mất khỏi bảng (edit), icon đổi sang mắt gạch, chữ "Hiện con".
- [ ] Bấm "Hiện con" → hàng con xuất hiện lại.
- [ ] Khi ẩn → **Tổng tiền / Tỷ suất LN KHÔNG đổi** (chỉ ẩn hiển thị, không trừ).
- [ ] Lưu khi đang ẩn → mở lại vẫn ở trạng thái ẩn; **hàng con vẫn còn trong dữ liệu** (bấm Hiện con thấy lại).
- [ ] Ẩn con → **Xuất Excel** và **In báo giá** đều KHÔNG hiển thị hàng con của hàng cha đó.

## 4. Hàng cha là hàng TỰ TẠO (hàng tạm)
**Thay đổi:** Cha tạm được chọn hàng con là **hàng ERP** hoặc **hàng tự tạo**.

**Test (tài khoản CÓ quyền "Xem giá vốn hàng hoá"):**
- [ ] Tạo 1 hàng tạm làm cha → bấm "Thêm con" → chọn được **hàng ERP** làm con (trước đây bị chặn).
- [ ] Chọn được hàng tự tạo làm con.
- [ ] Hàng con tự tạo: **hiện ô giá bán** đầy đủ (nhập được). Hàng con ERP: giá khoá từ ERP.

**Test (tài khoản KHÔNG có quyền):**
- [ ] Thêm con cho cha tạm → trong popup **KHÔNG thấy hàng ERP** (chỉ chọn được hàng tự tạo) + có ghi chú "Bạn không có quyền xem giá vốn...".
- [ ] Nếu cố lưu hàng ERP làm con → BE chặn, báo lỗi rõ ràng.

## 5. Hiển thị giá bán hàng con
**Test:**
- [ ] Con của cha **tự tạo** → hiện **giá bán + thành tiền** trên màn xem + in báo giá.
- [ ] Con của cha **ERP** → giá bán hiển thị "—" (giữ như cũ).

## 6. Validate khi LƯU NHÁP và GỬI DUYỆT (báo giá)

### Áp dụng cho CẢ Lưu nháp + Gửi duyệt:
- [ ] **VAT** ngoài khoảng 0–100% (vd 150%) → bị chặn, báo "VAT phải trong khoảng 0–100%".
- [ ] **Chiết khấu %** ngoài 0–100% (CK theo dòng hoặc CK tổng) → bị chặn, báo "Chiết khấu (%) phải trong khoảng 0–100%".

### Chỉ áp dụng khi GỬI DUYỆT (Lưu nháp vẫn cho qua):
- [ ] **Thành tiền bán** của mỗi hàng hoá / dịch vụ phải **> 0** → nếu có dòng = 0 thì chặn gửi duyệt (lưu nháp vẫn được). *(Chi phí vận chuyển KHÔNG bị validate.)*
- [ ] **Giá bán hàng cha tự tạo ≥ tổng giá bán hàng con** → nếu nhỏ hơn thì chặn gửi duyệt + viền đỏ ô giá bán cha. (Lưu nháp KHÔNG chặn.)
- [ ] **Giá nhập bắt buộc với hàng tự nhập** (báo inline đỏ tại ô giá nhập). **Hàng ERP giá nhập = 0 là hợp lệ** (không bị chặn — vì giá ERP khoá, không sửa được).
- [ ] **Dịch vụ**: bắt buộc tên + số lượng > 0 + giá bán > 0 + chiết khấu ≤ đơn giá (báo inline đỏ ô giá bán dịch vụ, đồng nhất hàng hoá).

## 7. Input số lượng
**Test:**
- [ ] Các ô **số lượng** (cha + con, ở cả BOM và báo giá) **không còn nút mũi tên tăng/giảm** (spinner).

## 8. Tạo báo giá từ BOM (không phải tự tạo)
**Test:**
- [ ] Tạo báo giá từ 1 BOM có cha-con → cấu trúc cha-con + trạng thái ẩn/hiện con copy đúng.
- [ ] Báo giá cũ (tạo trước thay đổi) mở/sửa/lưu vẫn bình thường (không vỡ).

---

## Lưu ý cho tester
- Các tính năng cha-con áp dụng cho **cả BOM và Báo giá tự tạo**; validate giá (mục 6) hiện áp ở **Báo giá**.
- "Recipe" (công thức ghép bộ) là dữ liệu chỉ-đọc bên ERP — snapshot 1 lần khi chọn cha; ERP đổi recipe sau đó KHÔNG ảnh hưởng phiếu đã tạo.
- Quyền dùng: **"Xem giá vốn hàng hoá"** (không tạo quyền mới).
