# Đề nghị nhập kho (WarehouseImportRequest) — Design (tóm tắt)

> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-08-25-de-nghi-nhap-kho-design.md`
> Nhánh: `gop_db` · Phụ trách: @namdangit

## Mục tiêu
Port màn **Đề nghị nhập kho** (ERP `WarehouseImportRequest`, mã `PDNNK`) sang HRM — tầng 2 trong
luồng nhập kho 3 tầng: **Yêu cầu nhập hàng** (`ProductImportRequest`, đã port) → **Đề nghị nhập kho**
(việc lần này) → Phiếu nhập kho thực + hạch toán (tầng 3, phase sau).

## Phạm vi (chốt A — chỉ chứng từ, KHÔNG đụng tồn/hạch toán)
Lập từ YCNH + list + chi tiết + Thủ kho duyệt + Từ chối + Hủy + In. Duyệt/hủy chỉ đổi status cấp
chứng từ. Tồn kho + sổ kế toán chỉ xảy ra ở tầng 3 → **tách phase sau**.

## Quyết định chính
1. **Module Finance** (đi cùng cha YCNH). URL BE `/api/v1/finance/warehouse-import-requests`. Lập từ YCNH:
   `GET .../product-import-requests/{id}/warehouse-import-data` + `POST .../{id}/warehouse-import-requests`.
   FE `pages/finance/warehouse-import-requests/`.
2. **Dùng thẳng bảng ERP** trên DB gộp (`warehouse_import_requests` + 6 bảng con), KHÔNG tạo bảng mới.
   Chỉ 1 migration add cột `emplement_contract_id/type/code` (mirror product_import_requests) để cõng HĐ HRM loại 21.
3. **Bộ status WIR riêng** (1 Đang nhập kho, 2 Chờ duyệt, 3 Đang tạo, 4 Đã hạch toán, 5 Đã hủy,
   6 Đã nhập kho, 7 Đang hạch toán) — KHÔNG trộn status YCNH. Type dùng lại ImportModel.
4. **Service layer** (khác fat-model ERP): `WarehouseImportRequestService`.
5. **Phân quyền = mirror Đề nghị xuất kho**:
   - Ghi (lập/sửa/hủy/đính kèm): `checkPermission:Kế toán kho` (dùng lại quyền có sẵn).
   - List: `checkPermissionListWithColumn` 4 cấp — thêm 4 quyền `Xem đề nghị nhập kho theo {tổng công ty|công ty|phòng ban|bộ phận}` + fallback phiếu mình tạo; ẩn nháp người khác.
6. **Generic mọi type**: cho lập đề nghị cho mọi YCNH status=2, snapshot **dòng phẳng** từ
   `product_import_request_details` (bám sát sibling ĐNXK, KHÔNG port tabs cha-con — HRM PIR không có `tabs()`).
   Nhánh type 4 (bán trả lại) / 9 (bán mượn trả lại) trừ `warehouse_exported_qty` HĐ hãng: **GÁC LẠI tầng 3**
   (đụng tồn HĐ hãng — ngoài biên scope A). Tinh chỉnh so với bản gốc quyết định 6.
7. **Biên scope A**: dừng ở WIR status 1 (Đang nhập kho); chỗ nối tầng 3 để phase sau.
8. **Xét quyền LẬP ĐNNK dùng `canApprove()` (trait raw-pivot RỘNG), KHÁC ĐNXK** (chốt 2026-09-22, fix Redmine "mất dữ liệu + không có quyền dù tk có quyền"): nút "Tạo ĐNNK" gate bằng cờ BE `is_can_approve`=`canApprove()` (đọc pivot thô, không lọc model_type/company/guard) nên `assertCanCreate()` cũng phải uỷ quyền về `canApprove()` để "thấy nút = lập được". ĐNXK thì FE+BE đều HẸP (`store.permissions` / global `isCurrentEmployeeHasPermission`) và **CỐ Ý giữ nguyên** — user chốt **A (2026-09-22)**: ĐNXK đang nhất quán, không ai báo lỗi, KHÔNG nới quyền. ⇒ 2 màn xét quyền lệch nhau là có chủ ý, đừng "đồng bộ" ĐNXK theo ĐNNK.

## Luồng trạng thái
`Lập` nháp(3)/gửi(2). Lập → cha YCNH sang 7 (Đang lập đề nghị); gửi thủ kho (WIR=2, Chờ duyệt) → YCNH sang 1 (Đã đề nghị).
`Thủ kho duyệt` WIR 2→1 (Đang nhập kho), YCNH→4 (Đang nhập kho). `Từ chối` WIR 2→3 (Đang tạo), YCNH→7 (Đang lập đề nghị).
`Hủy` (chỉ nháp WIR=3, người tạo) WIR→5 (Đã hủy), YCNH→6 (Đã hủy — mirror ERP `PIR::cancel`).
Bước hoàn `warehouse_exported_qty` HĐ hãng khi hủy type 4/9: **gác tầng 3**.

## Phase
- **P1 (làm ngay)** — BE: entity + migration + service + controller + request + routes + quyền + validate.
- **P2** — FE: index/detail/create + form + history; rewire nút "Tạo đề nghị nhập kho" ở product-import-requests.
- **Tầng 3 (feature tách)** — phiếu nhập kho thực + hạch toán ghi tồn/sổ.
