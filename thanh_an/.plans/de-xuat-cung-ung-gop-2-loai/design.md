# Gộp loại đề xuất cung ứng còn 2 loại — Tóm tắt

> Phụ trách: @khoipv · Ngày: 25/09/2026 · Trạng thái: **đã chốt thiết kế, chờ duyệt spec**
> Spec đầy đủ: [docs/superpowers/specs/2026-09-25-de-xuat-cung-ung-gop-2-loai-design.md](../../docs/superpowers/specs/2026-09-25-de-xuat-cung-ung-gop-2-loai-design.md)

## Mục tiêu

Ô "Loại đề xuất" ở màn lập phiếu đề xuất cung ứng rút từ **6 xuống 2 lựa chọn**: *Cung ứng nội bộ* /
*Cung ứng khách hàng*. Người dùng không còn phải tự biết hàng nằm trong HĐ loại nào trước khi chọn loại phiếu.

## Quyết định đã chốt

| Quyết định | Chốt |
|---|---|
| Ô Loại đề xuất | 2 lựa chọn: Nội bộ / Khách hàng |
| Pool hàng khi chọn Khách hàng | Hàng của **mọi loại HĐ** của khách đó (cả 5 loại) + toàn bộ danh mục |
| 1 phiếu 1 hợp đồng | **Giữ nguyên** — popup đã có cơ chế khóa `activeContractId` |
| Kiểu bảng hàng hóa | Suy theo **loại HĐ của dòng hàng đã chọn**, không theo ô Loại |
| Duyệt BGĐ | **Giữ nguyên hành vi**: HĐ trong/ngoài thầu → vào thẳng inbox; còn lại → Chờ BGĐ duyệt |
| Cột `supply_proposals.type` | **Giữ 6 mã**, BE tự suy lúc lưu → không migrate, không đụng hạ nguồn |
| Chỉ chọn hàng ngoài HĐ | → `type = 3` khách lẻ (khách chưa có HĐ nào) |
| 2 màn danh sách | Cột Loại hiện 2 tên gộp, bộ lọc 2 nhóm (`type_group`) |

## Bảng suy loại

| Hàng đã chọn | `type` lưu | Bảng hàng hóa | Khi gửi |
|---|---|---|---|
| Nội bộ | 2 | 2 cột tồn kho/đang mua | Chờ BGĐ |
| HĐ trong/ngoài thầu | 1 | đủ 6 cột theo HĐ | Thẳng inbox |
| HĐ đặt/mượn | 4 | kiểu khách lẻ | Chờ BGĐ |
| HĐ trao tặng | 5 | kiểu khách lẻ | Chờ BGĐ |
| HĐ nguyên tắc | 6 | kiểu khách lẻ | Chờ BGĐ |
| Chỉ hàng ngoài HĐ | 3 | kiểu khách lẻ | Chờ BGĐ |

## Điểm cần cẩn thận

- `goods-pool` và `/customers` **dùng chung với màn phiếu xử lý và màn Hợp đồng đã kết xuất** →
  thêm tham số `group`, thiếu `group` thì chạy y nguyên nhánh cũ.
- `supply_proposals.contract_id` là **HĐ nguồn** (phiếu lập từ màn Kết xuất HĐ), **không** suy ngược
  từ dòng hàng — suy vào sẽ bật nhầm `isFromContract` bên FE.
- BE **không tin** `type` / `contract_type` FE gửi lên, đọc lại `contracts.type` từ DB.

## Phạm vi file

**BE**: `Entities/SupplyProposal.php` · `Services/SupplyProposalService.php` ·
`Http/Requests/SupplyProposal/StoreSupplyProposalRequest.php` ·
`Http/Controllers/Api/V1/SupplyProposalController.php` ·
`Transformers/SupplyProposal/{Detail,}SupplyProposalResource.php`

**FE**: `pages/supply/supply_proposals/{constants.js, add.vue, index.vue, inbox.vue}` ·
`components/GoodsPickerModal.vue`

**Không đụng**: migration, `supply_handlings`, báo cáo nhu cầu mua, đơn mua, export Excel.
