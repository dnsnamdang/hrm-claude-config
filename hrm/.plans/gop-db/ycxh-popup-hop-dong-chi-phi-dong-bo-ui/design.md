# YCXH — Đồng bộ popup "Chọn hợp đồng chi phí" (loại Xuất khác) theo popup HĐ hãng

@dangquang.tom

## Bối cảnh
Màn YCXH `/finance/product-export-requests/create`, loại **Xuất khác (99)** có ô "Hợp đồng chi phí"
→ mở popup `ContractCostModal.vue` (endpoint `GET assign/product-export-requests/cost-contracts`).
Loại **Xuất bán hàng (14)** mở popup `FirmContractSearchModal.vue` (HĐ hãng).

User phản ánh: popup HĐ chi phí đang **khác khuôn** popup HĐ hãng, và logic lấy HĐ "có vẻ không đúng"
(ERP hiện ra HĐ, HRM rỗng).

## Quyết định đã chốt (user 2026-10-14)
- **CHƯA sửa logic lấy HĐ** (phạm vi theo công ty vs theo quyền + lọc loại HĐ) — để Phase 5 như
  comment service đã ghi. KHÔNG đụng `costContractScope()`.
- **Ưu tiên sửa GIAO DIỆN: đồng bộ khuôn tìm kiếm + cột** của popup HĐ chi phí cho giống popup HĐ hãng.

## Khác biệt UI cần xử lý (chốt làm)
| | HĐ hãng (chuẩn) | HĐ chi phí (hiện tại) | Sau khi sửa |
|---|---|---|---|
| Khung tìm | Số HĐ + Khách hàng + nút **Tìm kiếm** + **Làm mới** | Loại HĐ (select) + 1 ô gõ chung + **Làm mới** (debounce auto) | Loại HĐ (giữ, chức năng) + Số HĐ + Khách hàng + **Tìm kiếm** + **Làm mới** |
| Bảng | `V2BaseDataTable` server-sort + phân trang nhúng | `<table>` tay + `V2BasePagination` | Dựng lại trên `V2BaseDataTable` (khuôn firm) |
| Cột | STT / Mã hợp đồng / Khách hàng / **Địa chỉ** | STT / Mã HĐ / Khách hàng | STT / Mã hợp đồng / Khách hàng / **Địa chỉ** |
| Chọn | click cả dòng | click cả dòng | giữ click cả dòng |

### Ghi chú thiết kế
- **Giữ lại select "Loại hợp đồng"** vì đây là yếu tố CHỨC NĂNG (chọn bảng nguồn: contracts/
  service_contracts/project_contracts/opening_contracts/hrm_contracts) — HĐ hãng chỉ 1 bảng nên không có.
  Khuôn tìm = Loại HĐ + Số HĐ + Khách hàng + Tìm kiếm + Làm mới.
- **Mã HĐ để chữ TRƠN, KHÔNG link** (khác firm có link sang ERP): nguồn HĐ chi phí trải 5 class
  (`App\Contract`, `ServiceContract`, `ProjectContract`, `OpeningContract`, `HrmContract`) mà
  `utils/contract-link.js` chỉ map được OpeningContract → link sẽ lệch/null cho hầu hết. Ngoài phạm vi
  yêu cầu (chỉ đồng bộ khuôn tìm + cột).
- **Cột Địa chỉ**: `contracts/service_contracts/project_contracts/hrm_contracts` có cột
  `customer_address` → lấy thẳng. `opening_contracts` không có → join `customers` lấy `address_text`
  (đã join sẵn `cu` để lấy tên).

## File chạm
- FE: `hrm-client/pages/finance/product-export-requests/components/ContractCostModal.vue` (dựng lại theo khuôn `FirmContractSearchModal.vue`)
- BE: `hrm-api/Modules/Assign/Services/ProductExportRequestPickerService.php::costContracts()` — thêm
  filter `code`/`customer` tách, `sort_by`/`sort_desc`, select `customer_address`. **KHÔNG đụng** `costContractScope()`.
- BE: `.../Http/Controllers/Api/V1/ProductExportRequestController.php::costContracts()` — validate + truyền thêm tham số.

## Phạm vi KHÔNG đụng
- KHÔNG sửa phạm vi lọc theo công ty (`costContractScope`) — đó là "logic lấy HĐ" user hoãn.
- KHÔNG thêm link mã HĐ sang ERP.
- KHÔNG đổi envelope JSON của endpoint cost (giữ `{data:[...], meta:{...}}`).
