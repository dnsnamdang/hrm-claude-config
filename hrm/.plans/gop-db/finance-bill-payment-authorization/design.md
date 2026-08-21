# Design (tóm tắt) — Phiếu ủy nhiệm chi (ERP → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo) · Ngày: 2026-08-20
> **Spec đầy đủ**: `docs/superpowers/specs/gop-db/2026-08-20-finance-bill-payment-authorization-design.md`
> Feature tiền đề: `.plans/gop-db/finance-bill-payment-request/` (Đề nghị thanh toán — đã xong)
> Feature soi gương: `.plans/gop-db/finance-bill-payment/` (Phiếu chi tiền — đã xong)

---

## Mục tiêu

Port màn ERP `admin/income-expenditure/bill_payment_authorizations` (**Phiếu ủy nhiệm chi**) sang
HRM, phân hệ **Tài chính**, route `/finance/bill-payment-authorizations` (mục menu đã có sẵn dạng
placeholder trong nhóm *Quản lý tiền → Thanh toán tiền mặt*).

UNC là **cặp song sinh CHUYỂN KHOẢN của Phiếu chi**: cùng lập từ Đề nghị thanh toán trạng thái 6,
khác ở chỗ UNC chỉ nhận đề nghị `type_payment = 2` còn Phiếu chi lấy tiền mặt. Bên ERP 2 màn dùng
chung class JS và 2 blade bảng nhân viên.

## Scope

**Trong**: 1 màn danh sách duy nhất · chi tiết · tạo/sửa/xóa nháp · **"Lưu và duyệt" ghi sổ cái
ngay** · đủ 5 nhóm loại chi kể cả loại 4 "Chi thu nhập nhân viên".

**Ngoài**: gửi duyệt / duyệt / hủy (ERP đã bỏ dở) · in · xuất Excel · lịch sử thay đổi · không đụng
repo ERP · không migration · không `mysql2`.

## Số liệu thật (`gop_db`, đo 2026-08-20)

2.574 phiếu · 5.267 dòng chi tiết · **100% trạng thái 3 (Đã hạch toán)** · loại chi 1 (2.471) ·
2 (47) · 6 (37) · 12 (19) · **0 phiếu loại 4** · 100% `type_payment = 2` · 0 đề nghị có 2 UNC ·
0 đề nghị có cả UNC lẫn Phiếu chi.

## Quyết định lớn (user chốt 2026-08-20)

| # | Quyết định |
| --- | --- |
| 1 | **Luồng trạng thái 1:1 ERP** — chỉ "Lưu" (Đang tạo) và "Lưu và duyệt" (Đã hạch toán). Không có bước gửi duyệt |
| 2 | **Không chặn chéo** với Phiếu chi — giữ nguyên logic ERP, không đụng màn đã nghiệm thu |
| 3 | **Port đủ loại chi 4** dù DB 0 phiếu |
| 4 | **Không in, không xuất Excel** — đúng 1:1 ERP |
| 5 | Dùng chung 3 bảng ERP, không migration |
| 6 | Gộp 3 chế độ danh sách của ERP về **1 màn duy nhất** |
| 7 | **Giữ nguyên lỗi cộng dồn bút toán Có** của ERP (xem dưới) |
| 8 | **Không** thêm luật "1 đề nghị chỉ 1 UNC" ở popup |
| 9 | `date_accounting >= hôm nay` áp cả tạo lẫn sửa |

## 🚨 6 ruling CỐ Ý GIỮ ĐIỂM HỞ — đọc trước khi "sửa lỗi"

| Ruling | Nội dung |
| --- | --- |
| U-UNC-1 | Bút toán **Có** = tiền **DÒNG CUỐI**, không phải tổng (ERP gán `=` thay vì `+=`). Đo được **433/433 phiếu nhiều dòng lệch, thiếu 111.371.119.571 đ**. User xem số liệu rồi vẫn chốt giữ để đối chiếu 1:1 với ERP |
| U-UNC-2 | Popup chọn đề nghị KHÔNG loại đề nghị đã có UNC (Phiếu chi thì có) |
| U-UNC-3 | Không cho hạch toán lùi ngày, kể cả ở màn Sửa |
| U-UNC-4 | Không chặn chéo với Phiếu chi |
| U-UNC-5 | Không in, không xuất Excel |
| U-UNC-6 | Không có gửi duyệt / duyệt / hủy — trạng thái 2 và 4 là **trạng thái chết** |

## Điểm kỹ thuật chính

- **BE** `Modules/Finance`: `Entities/BillPaymentAuthorization/*` (entity + trait quyền + 2 detail
  model) · 4 service (`Service` đọc · `WriteService` ghi · `AccountingService` sổ cái nhánh A ·
  `EmployeeAccountingService` sổ cái nhánh B) · 2 FormRequest · 2 Resource · Controller **8 endpoint**.
- **Không tái dùng service ghi sổ của Phiếu chi**: 2 hàm ERP khác nhau **6 điểm** (nhánh A) và
  **5 điểm** (nhánh B) — tài khoản lấy từ phiếu hay từ dòng, nguồn khách hàng/NCC, số khoản, bộ mã
  vụ việc, `account_from_number`. Gộp bằng cờ điều kiện sẽ hỏng cả 2 màn.
- **Bảng UNC không có cột tổng tiền** như `bill_payments` → mọi truy vấn cần tổng đi qua
  `withSum('details', ...)`; sort cột tiền dùng alias `details_sum_payment_money_approve_exchange`.
- **Không gắn middleware `checkPermission`** — trên DB gộp middleware chung bỏ sót role gán từ thời
  ERP. Gate bằng `applyScope()` + `canView/canEdit/canDelete` + `isAccountant()`.
- **Quyền**: 2 quyền api MỚI id **1515 / 1516** (nguyên văn tên ERP, bản `web` là 100229/100230);
  tạo/sửa/xóa dùng lại `Kế toán thanh toán` (1152). Không có quyền duyệt riêng.
- **5 trường riêng** so với form Phiếu chi: `account_dept` (cấp phiếu) · `date_accounting` ·
  `source_money` · `bank_from` · `account_from`. Ngược lại UNC KHÔNG có ô "Người nhận" ở nhánh A và
  KHÔNG có cột "Đối tượng" trong bảng chi tiết.
- Đề nghị nguồn nhảy **6 → 8**, bỏ qua 7 (Phiếu chi đi đủ 7 → 8).

## Sửa lỗi ERP (có chủ ý)

1. Gán 3 cột đơn vị ở hook `creating` thay vì `created` + `save()` lần 2.
2. `updateStatus()` đọc `bill_payment_request_id` từ **bản ghi**, không từ payload (ERP cho sửa
   payload là đổi trạng thái phiếu đề nghị bất kỳ).
3. `generateCode()` có `lockForUpdate()`.
4. `canEdit/canDelete` bắt buộc **đúng người lập + có quyền** (ERP chỉ kiểm trạng thái → ai gọi được
   URL cũng xóa được phiếu người khác).
5. Xóa phiếu dọn cả 2 bảng con (ERP để lại dòng mồ côi).
6. Ép `status` client gửi về {1, 3}; thêm luật validate cho `type`.
7. Màu badge: Đang tạo **xám** · Chờ duyệt **vàng** · Hủy đỏ (ERP để `danger` cho cả 3).

## 🐛 4 lỗi chỉ trình duyệt mới lộ (đã sửa, 2026-08-20)

1. **Ngày hạch toán chặn hoàn toàn việc lưu** — FE gửi `dd/mm/yyyy`, luật `date` của Laravel đọc
   chuỗi có `/` theo kiểu m/d/Y ⇒ màn không lưu được **từ ngày 13 hàng tháng trở đi**. Sửa 2 lớp:
   FE gửi ISO + BE `prepareForValidation()` nhận cả 2 định dạng.
2. **403 khi kéo dữ liệu phiếu đề nghị** — popup không áp phạm vi xem (đúng thiết kế) nhưng
   `GET /bill-payment-requests/{id}` lại gate bằng `canView()` của màn kia. Thêm endpoint riêng
   `GET /bill-payment-authorizations/payment-requests/{id}` gate bằng `isAccountant()`.
   ⚠️ **Cả Phiếu chi lẫn Phiếu thu đã nghiệm thu đều dính CÙNG lỗi** — user chốt sửa luôn
   2026-08-20, đã thêm endpoint tương ứng cho từng màn (xem plan.md Phase 11). Đo trước khi sửa:
   popup Phiếu chi trả 95 phiếu / Phiếu thu 33 phiếu nhưng 3/3 phiếu thử đều 403 ⇒ 2 màn đó thực tế
   không lập được phiếu với tài khoản kế toán khác công ty.
3. **500 `Column 'receiver' cannot be null`** — nhánh A không có ô Người nhận/Phòng ban chi, FE gửi
   rỗng, middleware `ConvertEmptyStringsToNull` đổi thành null, 5 cột `NOT NULL` không default nổ.
   Ép mặc định theo đúng dữ liệu thật ERP (`receiver=''`, `payment_department_id=0`).
4. **Nhánh loại 4 thừa cột "Chi phí khác"** — bảng dùng chung có 6 khoản, ERP bản UNC chỉ ghi sổ 5;
   tiền nhập vào ô đó không bao giờ vào sổ cái. Thêm prop `excludeFields`.

## Kết quả verify

- **Replay sổ cái 63 phiếu cũ → 62/63 khớp tuyệt đối 31 trường** + số dòng ref. 1 phiếu lệch cột
  `part_id` là **trôi dữ liệu nhân viên**, đã truy ra mốc thay đổi.
- 8/8 endpoint GET trả 200 đúng số liệu; luồng ghi end-to-end chạy trong transaction rồi rollback,
  4 bảng về đúng số dòng cũ.
- `php -l` sạch 12 file BE · compile 6/6 file Vue · 5/5 lệnh grep tự kiểm sạch.
- **Test Playwright toàn luồng (2026-08-20)**: 25 kịch bản đạt — phạm vi quyền 2/2.574 · 16/16 ô lọc
  khớp DB · lưu nháp → sửa → lưu và duyệt → xóa · **bút toán Có = tiền DÒNG CUỐI (RULING U-UNC-1
  tái lập được qua giao diện)** · đề nghị 6 → 8 · guard `/edit` · cảnh báo chưa lưu · **0 lỗi
  console**. Dọn dẹp xong **8/8 chỉ số về đúng baseline** kể cả `MAX(id)`. Chi tiết ở plan.md Phase 10.

## 📌 Còn treo

1. ~~CHỜ USER XÁC NHẬN (a)~~ **user đã chốt 2026-08-20**: đã thêm prop `excludeFields` vào component DÙNG CHUNG
   `PaymentEmployeeTable.vue` của màn Phiếu chi (mặc định `[]`, màn cũ không đổi hành vi) để màn
   UNC ẩn cột "Chi phí khác" — ERP bản UNC chỉ ghi sổ 5 khoản, để nguyên 6 cột là mất tiền im lặng.
2. ~~CHỜ USER XÁC NHẬN (b)~~ **user đã chốt 2026-08-20 — giữ bản sửa**: ERP `update()` thiếu loại 12 trong danh sách ghi sổ so với `store()` →
   phiếu loại 12 lưu nháp rồi duyệt sẽ KHÔNG có bút toán nào. HRM dùng cùng một danh sách cho cả 2
   đường (xem plan.md mục 9.5).
3. Chưa đối chiếu trực tiếp giao diện với cổng ERP; chưa dựng phiếu thử loại 6 / 12 / 4.
4. Nhánh loại 4 và bảng phân bổ phiếu xuất hàng **không có dữ liệu thật** để kiểm chứng.
5. Bảng con "phân bổ theo phiếu xuất hàng" trong form CỐ Ý chưa dựng (bảng 0 dòng toàn hệ thống).
6. Chưa có SRS / testcase / HDSD.
