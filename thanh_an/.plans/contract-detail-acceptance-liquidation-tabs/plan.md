# Chi tiết HĐ — Tab Biên bản nghiệm thu + Biên bản thanh lý

> @khoipv — làm theo pattern tab "Phụ lục liên quan" (GeneralComponent.vue)

## Yêu cầu
Màn `contract/contract/[id]`: thêm 2 tab **Biên bản nghiệm thu** và **Biên bản thanh lý**, bảng liệt kê (STT / Mã / [Loại] / Trạng thái), click mã mở tab mới sang chi tiết. Giống tab "Phụ lục liên quan".

## Task
### BE
- [x] `Contract` entity: thêm quan hệ `acceptanceReports()` (hasMany AcceptanceReport) + `liquidations()` (hasMany ContractLiquidation) + import 2 entity.
- [x] `ContractDetailResource`: thêm field `acceptance_reports` (id, code, type_name, status, status_name) + `liquidations` (id, code, status, status_name).

### FE — GeneralComponent.vue
- [x] Thêm tab "Biên bản nghiệm thu": bảng STT / Mã BBNT / Loại NT / Trạng thái; click mã → `/contract/acceptance_report/{id}` (tab mới). Empty: "Chưa có biên bản nghiệm thu".
- [x] Thêm tab "Biên bản thanh lý": bảng STT / Mã BBTL / Trạng thái; click mã → `/contract/contract_liquidation/{id}` (tab mới). Empty: "Chưa có biên bản thanh lý".
- [x] Dùng `status_name` từ BE + `statusColorMap` sẵn có cho màu (1-4). Đặt 2 tab cạnh tab "Phụ lục liên quan".

### Checkpoint — 2026-07-21
Vừa hoàn thành: BE (2 quan hệ Contract + 2 field resource) + FE (2 tab BBNT/BBTL trong GeneralComponent.vue, tái dùng BaseStatusColor + statusColorMap).
Đang làm dở: chưa chạy nuxt dev (Node 14, cần user chạy).
Bước tiếp theo: user mở /contract/contract/[id] kiểm tra 2 tab hiển thị + click mã mở đúng chi tiết.
Blocked:

## Ghi chú
- Route chi tiết: BBNT `/contract/acceptance_report/{id}`, BBTL `/contract/contract_liquidation/{id}`.
- Status codes 1-4 (Nháp/Chờ duyệt/Đã duyệt/Không duyệt) — dùng status_name BE cho chuẩn nhãn.
