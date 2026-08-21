# customer-lock — Khóa / Mở khóa khách hàng (tóm tắt)

**Nhánh:** `gop_db` · **Người phụ trách:** @khoipv · **Ngày:** 2026-08-11
**Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-08-11-customer-lock-design.md`

## Mục tiêu

Bổ sung Khóa / Mở khóa khách hàng cho `/assign/customers`, tương đương ERP
(`Sale\CustomersController@delete` / `@unlock`).

## Chốt

- Khóa = `customers.status = 0`, mở khóa = `= 1`; không đụng field khác, không chặn điều kiện
  nghiệp vụ (ERP `canDelete()` luôn true)
- Quyền: dùng **quyền ERP `Xóa khách hàng`** (FE đã có `perm.delete` từ `my-permissions`),
  không tạo permission mới
- 2 endpoint mới: `POST /assign/customers/{id}/lock` và `/unlock` (ERP dùng GET, HRM đổi sang POST)
- Nút icon Khóa/Mở khóa nằm trong hàng nút ở cột *Mã KH - Tên KH*, có modal xác nhận
- KH khóa **không chọn được ở form**, nhưng **ô lọc vẫn hiện đủ** để tra cứu dữ liệu cũ

## Phát hiện khi khảo sát (làm gọn phạm vi)

- Popup chọn KH của form Dự án TKT / Meeting / Phiếu chuyển hàng dùng chung
  `components/modals/ChooseErpCustomerModal.vue` và **đã lọc `status: 1` sẵn**
- 21 chỗ còn lại lấy danh sách KH đều là **ô lọc** → giữ nguyên
- Chỗ duy nhất còn hở: ô **"Công ty mẹ"** trong form KH (`parent-options`) — ERP có lọc `status = 1`,
  HRM chưa → bổ sung
- `filteredCustomers` trong `pages/assign/meeting/components/GeneralInfo.vue` là code chết
  (gán nhưng không render) — không đụng

## Không làm

Không migration · không permission mới · không đụng ERP · không đổi hành vi ô lọc KH các màn khác.
