# Phase 3 — HỢP ĐỒNG DỊCH VỤ (chứng từ 5)

> Khảo sát ERP ngày 2026-08-28, đọc trực tiếp `TanPhatDev/`. Số liệu đếm trên cơ sở dữ liệu gộp.
> Đây là **mắt xích cuối của đoạn A** trong luồng dịch vụ.

## 1. Quy mô và hiện trạng

| | |
| --- | --- |
| Controller ERP | `WarrantyRepairContractsController` — 1.391 dòng, 30 route |
| Model ERP | `WrServiceContract` — 3.327 dòng |
| Bảng | `wr_service_contracts` — **83 cột**, dùng chung cho 4 loại chứng từ |
| Bảng con | `..._products` 8.198 · `..._product_items` 3.080 · `..._product_services` 1.885 · `..._costs` 33.755 · `..._payments` 3.254 |

**HRM đã có sẵn** (làm từ bước Phiếu bảo hành): entity `WrServiceContract` với đủ 4 hằng `TYPE_*`
khớp ERP, 5 entity con, và bộ trạng thái `STATUSES_WARRANTY`. Phase này thêm `STATUSES` của hợp
đồng + tầng service/controller/FE.

## 2. Quyết định nền: GIỮ NGUYÊN BẢNG, tách nhánh bằng `type`

Bảng phục vụ 4 màn: Hợp đồng (2.321) · Phiếu bảo hành (3.631) · Phụ lục bổ sung (185) · Phụ lục
giảm (539); thêm 724 bản ghi có `parent_id` là phụ lục hợp đồng.

**Không tách bảng.** Lý do dứt khoát: cơ sở dữ liệu này **dùng chung với ERP đang chạy** — tách ra
phải chuyển 6.676 bản ghi thật trong khi ERP vẫn đọc bảng cũ, nó vỡ ngay. Cách tách nhánh bằng
`type` cũng đã chạy tốt qua `wr_service_quotations` (phiếu cung cấp thông tin / báo giá) và chính
bảng này với Phiếu bảo hành.

## 3. Ba phát hiện làm gọn phạm vi

1. **100% hợp đồng lập TỪ BÁO GIÁ** (2.321/2.321), không có cái nào lập độc lập → chỉ cần MỘT
   nhánh tạo. Khác hẳn Báo giá (77% lập độc lập, phải cắt 2 phase vì việc đó).
2. **Chỉ 2 lối vào có mục menu**: `?type=all` (2.321 bản ghi) và `?type=for-approve` (2 bản ghi
   đang Chờ duyệt). Ba nhánh `index` / `can_export` / `assign-task` không có mục menu nào.
3. Entity + tầng quyền đã port sẵn, kế thừa được ngay.

## 4. ⚠️ Bẫy đã thấy trước khi code

- **Hằng trạng thái TRÙNG GIÁ TRỊ**: ERP khai `DANG_THUC_HIEN = 5` **và** `DA_QUYET_TOAN = 5`.
  Cùng một số 5 mang hai tên. Khi port phải xác định số 5 thực tế nghĩa là gì trên dữ liệu, KHÔNG
  đọc theo tên hằng. Dữ liệu thật: **1.208 bản ghi mang status = 5** — nhóm lớn thứ nhất.
- **Ba bộ trạng thái đọc chung một cột** `status`: `STATUSES` (hợp đồng), `STATUSES_WARRANTY`
  (phiếu bảo hành), `STATUSES_ANNEX` (phụ lục). Cùng số nhưng khác nghĩa — đã dính bài học này ở
  chứng từ 3/4, phải rẽ nhãn theo `type` ngay từ đầu (`statusTable()`).
- **Quyền "Xem hợp đồng ẩn giá" (id 1037) KHÔNG phải quyền ẩn giá** — trong `searchByFilter` nó
  cho xem **toàn bộ danh sách** như quyền tổng công ty. Tên gây hiểu nhầm, đọc kỹ trước khi gate.

## 5. Phân quyền

4 quyền, hiện **chỉ có guard `web`** của ERP, chưa có bên HRM — phải thêm vào `PermissionsTableSeeder`:

| Quyền | id (web) | Ý nghĩa |
| --- | --- | --- |
| Xem hợp đồng dịch vụ SC - BH theo tổng công ty | 100420 | Xem toàn bộ |
| Xem hợp đồng dịch vụ SC - BH theo công ty | 100421 | Theo công ty + hợp đồng của mình |
| Xem hợp đồng dịch vụ SC - BH theo phòng ban | 100422 | Theo phòng quản lý + của mình |
| Xem hợp đồng ẩn giá | 101037 | Xem toàn bộ danh sách (xem bẫy ở mục 4) |

## 6. Trạng thái hợp đồng và số liệu thật

| Trạng thái | Số bản ghi |
| --- | --- |
| Đang tạo | 34 |
| Chờ duyệt | 2 |
| Có hiệu lực | 938 |
| Đang quyết toán | 67 |
| status = 5 (Đang thực hiện / Đã quyết toán — xem bẫy) | 1.208 |
| Đóng hợp đồng | 71 |
| Không duyệt | 1 |

Bản ghi cũ nhất 04/08/2025, mới nhất 28/07/2026 — luồng **đang sống**, không phải chức năng chết.

## 7. Cắt phase (user duyệt 2026-08-28)

### Phase A — làm trước, khép đoạn A của luồng

- Màn danh sách: 2 lối vào · bộ lọc (số hợp đồng, người duyệt, người lập, trạng thái, khách hàng,
  tên/mã hàng hoá, model, serial, dịch vụ) · 11 cột
- Màn xem chi tiết + màn lập hợp đồng **từ báo giá** (nhánh duy nhất)
- Các khối: **A** Dịch vụ sửa chữa bảo dưỡng (I thiết bị sửa chữa + II thiết bị cần bảo dưỡng) ·
  **B** Chi phí khác (I các khoản liên quan + II chi phí vận chuyển) · **C** Hàng hoá
- Sửa / Xoá theo `canEdit()`: **chỉ người lập**, và chỉ khi trạng thái Đang tạo hoặc Không duyệt
- In hợp đồng
- Lịch sử thay đổi

### Phase B — cần chốt thêm, đụng Kế toán

- Khối **D** Thông tin thanh toán (3.254 dòng dữ liệu thật)
- Ký hợp đồng · Duyệt / Không duyệt / Đóng hợp đồng · Quyết toán
- Các đường cắm sang phân hệ khác: Kho (xuất kho, mượn–bán, xuất giữ) · Kế toán (đề nghị thanh
  toán, yêu cầu hạch toán dịch vụ — 877 bản ghi) · Giao việc (`wr_assign_tasks` — 14.513 bản ghi)

### Sau Phase B

Phụ lục hợp đồng (724) · Phụ lục bổ sung (185) · Phụ lục giảm (539) — cùng bảng, làm liền mạch.

## 8. Ba điểm đã chốt (user 2026-08-28)

**1. Nút "Lập hợp đồng dịch vụ" — GIỮ NGUYÊN ERP.** Nguyên tắc user chốt: *"logic luôn phải tuân
thủ như ERP đang chạy, có lỗi thì fix thôi"*. Port đúng `canCreateContract()`:

- báo giá ở trạng thái **Duyệt**, VÀ
- có phần sửa chữa — ít nhất một trong: thiết bị sửa chữa · thiết bị bảo dưỡng · hàng hoá ·
  tổng chi phí sửa chữa > 0, VÀ
- **chính người đang đăng nhập là người lập báo giá** (Super Admin được miễn điều kiện này).

Không nới cho cả phòng.

**2. Ba nhánh không có mục menu — BỎ.** `index` / `can_export` / `assign-task` không port. HRM chỉ
làm 2 lối vào có menu thật: `?type=all` và `?type=for-approve`.

**3. Cột giá vốn — KHÔNG hiện, đúng ERP.**

Đã tra tận nơi: form hợp đồng của ERP **không có cột "Giá vốn"** (khác màn Báo giá). Bảng thiết bị
của hợp đồng dùng bộ cột khác hẳn — *Đơn giá · Thành tiền · Doanh số vượt trội · Đơn giá sau điều
chỉnh · % Chiết khấu · Tiền chiết khấu · Giảm giá · Đơn giá sau giảm · Thành tiền sau giảm*.

⚠️ Nhưng cột `engineering_work` trên bảng `wr_service_contract_products` **vẫn có dữ liệu thật**
(8.194/8.198 dòng): giá vốn được **chép sang từ báo giá và lưu lại**, chỉ là không hiển thị — để
dành cho quyết toán ở Phase B. Vậy HRM: **chép và lưu như ERP, không hiện cột, và KHÔNG cần cờ
`canViewCostPrice`** ở màn này (không hiển thị thì không có gì để gate).
