# Design (tóm tắt) — Phiếu yêu cầu hạch toán bổ sung (ERP → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo, code thẳng trên nhánh này) · Ngày: 2026-08-25
> **Spec đầy đủ**: `docs/superpowers/specs/gop-db/2026-08-25-finance-addition-accounting-request-design.md`
> Feature tham chiếu: `.plans/gop-db/finance-bill-adjust-dept-request/` · `.plans/gop-db/finance-bill-payment-request/`

---

## Mục tiêu

Port màn ERP `admin/income-expenditure/addition_accounting_requests` sang HRM, phân hệ **Tài chính**,
route `/finance/addition-accounting-requests`. Chứng từ nhân viên lập để **đề nghị kế toán hạch toán
bổ sung một khoản công nợ**; kế toán duyệt rồi lập phiếu kế toán ghi sổ.

**Nguyên tắc user chốt: bám sát logic ERP.** Chỉ đổi nguồn hợp đồng bán, khoác giao diện chuẩn HRM,
và vá các lỗi ERP đã liệt kê.

## Scope

**Trong**: 6 loại tạo mới (1–6) · loại 7 chỉ xem/in · 2 chế độ danh sách · tạo/sửa/xoá nháp ·
gửi duyệt · từ chối · file đính kèm S3 · in · xuất Excel phiếu + danh sách · thông báo chuông ·
lịch sử thay đổi.

**Ngoài**: màn *Phiếu kế toán điều chỉnh công nợ* (`bill_adjust_dept`) — HRM chỉ có nút mở sang cổng
ERP · **HRM không ghi sổ cái `account_details`** · không port màn Phiếu xác nhận bảo hành / Phiếu xử
lý hàng thiếu / Quyết toán HĐ bán (chỉ đọc bảng).

## Quyết định lớn (user chốt 2026-08-25)

| # | Quyết định |
| --- | --- |
| 1 | Dùng chung **5 bảng ERP**, **0 migration** |
| 2 | Port **đủ 6 loại tạo mới như ERP** (kể cả loại 1 và 5 hiện 0 phiếu, phải dựng 2 popup chọn chứng từ nguồn) |
| 3 | **Loại 7 "Phối hợp kinh doanh" làm như ERP**: hiện trong danh sách, chỉ xem + in, không tạo/sửa |
| 4 | **Dừng ở "Chờ duyệt"** + nút *Lập phiếu kế toán* **mở sang cổng ERP** qua `utils/erp-link.js` |
| 5 | **Hợp đồng bán `firm_contracts` → `hrm_contracts`** (đồng bộ màn Điều chỉnh công nợ 17/08) |
| 6 | **Lịch sử thay đổi dùng `catalog_histories`** + trait `LogsCatalogHistory` — không thêm bảng |
| 7 | **File đính kèm giữ ở cột `attachments` của ERP** (chuỗi URL S3), KHÔNG dùng bảng `files` — 2 cổng đọc chung 1 phiếu. Thư mục S3 giữ nguyên lỗi chính tả của ERP: `addiiton_accounting_requests` |
| 8 | **4 quyền mới guard `api` id 1177–1180**, trùng tên ERP; duyệt dùng lại `Kế toán thanh toán` (1152) / `Kế toán` (100079) / `Kế toán kho` (1136) |
| 9 | **3 mục menu** đã chờ sẵn trong `finance.js`: nối dòng 58 (danh sách) và 464 (chờ duyệt); dòng 360 **để trống** cho khớp màn Điều chỉnh công nợ |
| 10 | `objectable_type` (KH/NCC) **KHÔNG thêm vào morphMap toàn cục** — resolve thủ công theo chuỗi, tránh đổi hành vi morph của `TpCustomer` toàn hệ thống |

## Khác biệt có chủ đích so với ERP — vá 9 lỗi

1. `canEdit()`/`canDelete()` thiếu vế `created_by` → ai cũng sửa/xoá được phiếu nháp người khác.
2. Xoá bằng **GET**, không gate quyền/trạng thái → đổi `DELETE` + gate.
3. `store()/update()` gán thẳng `$request->status` → nhảy cóc lên *Đã duyệt*; HRM chỉ nhận 1 hoặc 2.
4. Màn *Chờ duyệt* không lọc trạng thái cho người thường → luôn `status = 2`.
5. Ô lọc "Phiếu xác nhận BH" khai sai key và BE không đọc → **ô lọc chết**; sửa key + lọc thật.
6. Lọc ngày dùng `>` / `<` → mất phiếu đúng ngày kết thúc; đổi `whereDate`.
7. Bản in loại 4 in nhãn NCC nhưng đổ dữ liệu KH; loại 5 in nhầm mã Phiếu xác nhận BH.
8. `reject()` không lưu ai từ chối và lúc nào.
9. Loại 4 chọn *Nhân viên* không có rule validate → lưu được phiếu không đối tượng.

**Không sửa có chủ đích:** `generateCode()` sinh mã từ `id` nên không trùng — không cần lock.

## Số liệu nền (DB `gop_db`, 2026-08-25)

1.937 phiếu — loại 6 NCC 1.033 · loại 2 KH 861 · loại 7 Phối hợp KD 36 · loại 4 Khác 7 ·
**loại 1/3/5 = 0**. Trạng thái: Đã duyệt 1.816 · Đang tạo 75 · Chờ duyệt 45 · Đang duyệt 1.
Dòng chi tiết 2.849 (Supplier 2.292 · Customer 557), gắn 8 loại hợp đồng khác nhau.

## Rủi ro đã biết

- **Loại 1 và 5 chưa từng chạy thật** (0 phiếu, 2 màn nguồn chưa port) → chỉ kiểm chứng bằng seeder.
- Phiếu HRM gắn `hrm_contracts` sẽ lỗi *Class not found* khi mở bên ERP — hệ quả đã biết, đã chấp nhận.
- `objectable_type = App\Model\Sale\Supplier` trong khi bảng `suppliers` **rỗng**, NCC nằm ở
  `customers.is_supplier` → resolve sai là tên NCC ra trống.
- `customer_id` và `contractable_id` là **varchar** → so sánh với id số phải cast.
