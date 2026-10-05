# Phiếu huỷ hàng giữ kế toán (ERP → HRM) — design

**Người phụ trách:** @junfoke — 2026-09-28

- **Trạng thái**: CODE XONG + VERIFY (2026-09-29), CHƯA COMMIT — xem checkpoint cuối `./plan.md`
- **Phạm vi**: 1 màn — `Phiếu huỷ hàng giữ kế toán` (bảng ERP `accounting_prepick_cancels`). Là màn
  **cuối cùng** của nhóm Giữ hàng chưa port.
- **Phân hệ đích**: Tài chính → nhóm menu **Giữ hàng**. Mục menu đã có sẵn placeholder
  `{ label: 'Phiếu huỷ hàng giữ kế toán' }` trong `components/subsystem-menu/finance.js`, chỉ thiếu `link`.
- **Tiền lệ**: [Hủy hàng giữ](../finance-prepick-cancel-request/design.md) — dùng lại
  `PrepickStockService`, `PrepickStockSearchModal`, bộ quyền, cách ghi `prepick_logs`.
- **Spec đầy đủ**: `docs/superpowers/specs/gop-db/2026-09-28-finance-accounting-prepick-cancel-design.md`
- **Nhánh**: `feat/finance-accounting-prepick-cancel` ở cả 2 repo, tách từ `gop_db`.

---

## Mục tiêu

Kế toán (quyền `Quản lý giữ hàng`) **huỷ thẳng** hàng đang giữ của một nhân viên, không cần phiếu yêu
cầu, không có vòng duyệt. Một phiếu gồm nhiều hàng hoá, mỗi hàng hoá huỷ cho **nhiều khách hàng**.
Bấm **Duyệt** = lưu phiếu + trừ tồn giữ FIFO ngay, không sửa / xoá được.

Khác màn `Phiếu hủy hàng giữ` thường:

| | Phiếu hủy thường (`prepick_cancels`) | Phiếu hủy KẾ TOÁN (`accounting_prepick_cancels`) |
|---|---|---|
| Nguồn | Từ 1 phiếu yêu cầu hủy | Kế toán tự lập |
| Khách hàng | 1 KH / phiếu | Nhiều KH / 1 hàng hoá (bảng gộp dòng) |
| ĐVT | Khoá, luôn ĐV cơ bản | **Chọn được**, quy đổi `cancel_qty = qty × hệ số` |
| Mã phiếu | `PHHG-xxxxx` | `KTPHHG-xxxxx` |
| `prepick_logs.objectable` | `PrepickCancel` + id phiếu | `AccountingPrepickCancelDetailCustomer` + **id dòng KH** |

## Quyết định user chốt (2026-09-28)

1. **`PrepickStockService::deductFifo()`** (hàm dùng chung) thêm tham số tuỳ chọn `$objectableType`,
   mặc định giữ `PrepickCancel` → 2 màn đang gọi không đổi hành vi.
2. **Dropdown Nhân viên** = toàn bộ NV đang làm việc, **giữ như ERP**. Bù lại: popup chọn hàng báo rõ
   "Nhân viên này hiện không giữ hàng hoá nào" khi rỗng.
3. **Gửi thông báo** cho NV bị huỷ hàng (ERP không có) — mã phiếu + link chi tiết.
4. **Phạm vi xem giữ như ERP**: mọi API gate quyền `Quản lý giữ hàng`, danh sách lọc theo công ty của
   người đăng nhập. KHÔNG áp 3 cấp quyền xem như màn phiếu hủy thường.

## Dữ liệu (dùng chung ERP — không tạo bảng nghiệp vụ mới)

`accounting_prepick_cancels` (≈600 phiếu) → `accounting_prepick_cancel_details` (≈1.616, snapshot
tên / model / thương hiệu / mã hàng) → `accounting_prepick_cancel_detail_customers` (≈1.641,
`customer_id`, `qty`, `unit_id`, `unit_name`, `unit_coefficient`, `cancel_qty`). Không có cột status.
Bảng MỚI duy nhất: `accounting_prepick_cancel_history` (lịch sử thay đổi).

Bị GHI khi duyệt: `prepick_details` (tồn giữ thật) + `prepick_logs`.

## Lỗi ERP vá khi port (chi tiết ở spec mục 4)

1. `print()` đọc nhầm `PrepickCancelRequest` + hằng mẫu in không tồn tại → fatal → **dựng mẫu in mới**.
2. `canView()` bị comment ở `show()` → gate lại (quyền + cùng công ty).
3. `updateWarehouse()` không kiểm đủ tồn, trừ hụt im lặng → khoá lô + kiểm trước (`deductFifo`).
4. Cho chọn **trùng khách hàng** trong cùng 1 hàng hoá; mỗi dòng kiểm riêng với toàn bộ tồn → tổng
   vượt tồn vẫn qua → gộp theo (hàng hoá, KH) rồi mới kiểm.
5. Cột Hành động ở danh sách là dropdown rỗng → In phiếu · Lịch sử.
6. `catch (Exception $e)` thiếu `\` → lỗi không bao giờ rollback đúng → transaction chuẩn Laravel.
7. Popup chọn hàng lấy số "Đang giữ" thô, form lại lấy số đã trừ ĐN xuất kho chưa xong → dùng chung
   `availableQty`.
8. `syncProducts()` đọc `$product->brand->name` / `model->name` — hàng không có thương hiệu/model là
   lỗi 500 (cột NOT NULL) → ghi chuỗi rỗng / `0`.
9. Form tạo có modal "Phiếu yêu cầu hủy hàng giữ" copy thừa + nút Hủy trỏ nhầm danh sách phiếu hủy
   thường → bỏ modal, Quay lại về đúng danh sách.
10. Dropdown KH của 1 hàng hoá không `GROUP BY` (KH nhiều lô bị lặp) và không lọc công ty → hàm mới
    `holdingCustomersOfProduct()`.
11. Dòng KH qty = 0 bị bỏ nhưng dòng hàng hoá vẫn ghi → phiếu có hàng hoá rỗng KH → không ghi.

## Phạm vi code

- **BE** `Modules/Finance`: 4 entity (`Entities/AccountingPrepickCancel/`), 2 service, 1 controller,
  1 FormRequest, 2 Resource, 2 blade in, 1 migration, 10 route. Sửa nhỏ 2 file dùng chung:
  `PrepickStockService` (tham số mới + 1 hàm mới), `PrepickStockReportService` (gắn `hrm_path`).
- **FE** `pages/finance/accounting-prepick-cancels/`: danh sách V2 · tạo · chi tiết · xuất Excel ·
  lịch sử · in phiếu / in danh sách bằng **popup xem trước** `ReportPrintPreviewModal` (skill
  `print-page` mục 0 — không dựng trang `/print`). Dùng lại `components/finance/prepick/PrepickStockSearchModal.vue`
  (nguyên component — prop `emptyText` / `hideExisting` có sẵn) và `PrepickHistory{Panel,Modal}.vue`. Gắn link menu.

## Rủi ro chính

- **Ghi tồn thật** → sao lưu 6 bảng trước khi test, chỉ thao tác phiếu tự tạo, dọn xong đối chiếu từng cột.
- Sửa `deductFifo` dùng chung → phải test lại luồng duyệt của màn Phiếu hủy thường.
- Kế toán khác công ty chủ lô: ERP tìm lô theo `company_id` của phiếu (= công ty kế toán) nên không ra
  lô, trừ hụt im lặng. HRM tra lô theo công ty **NV chủ lô** (tiền lệ `PrepickCancelService::store()`),
  `company_id` của phiếu vẫn là công ty người lập như ERP.
