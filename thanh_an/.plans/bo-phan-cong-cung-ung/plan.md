# Plan — Bỏ cơ chế phân công NV phụ trách cung ứng

Phụ trách: @khoipv
Màn: `supply/contract_render` (Hợp đồng đã kết xuất) · luồng kết xuất HĐ sang cung ứng

## Bối cảnh / Yêu cầu
- Hiện tại HĐ kết xuất sang cung ứng phải **được phân công NV phụ trách** thì người đó mới lập được phiếu đề xuất cung ứng.
- Yêu cầu: **bỏ hẳn** ràng buộc này — HĐ đã kết xuất thì **ai có quyền "Lập phiếu đề xuất cung ứng" cũng lập được**.

## Quyết định đã chốt với user
1. **Bỏ hẳn** cơ chế phân công (không chỉ bỏ chặn): ẩn nút Phân công, bỏ cột "NV phụ trách cung ứng", bỏ auto-assign khi kết xuất.
2. **Bỏ luôn thông báo** khi kết xuất (cả 2 loại: báo cho người được phân công và báo cho người có quyền "Phân công đề xuất cung ứng").
3. Code cũ **comment lại**, KHÔNG xóa — sau cần thì bật lại.
4. **Không migration**: giữ nguyên cột `contracts.supply_manager_id`, `supply_received_time`, `supply_received_group_id` và bảng `contract_supply_assign_employees`. Giữ nguyên quyền "Phân công đề xuất cung ứng" trong DB.

## BE
- [x] `Modules/Category/Entities/Contract/Contract.php` — `canCreateSupplyProposal()`: comment điều kiện `supply_manager_id == auth()->id`
- [x] `Modules/Category/Services/ContractService.php` — `renderSupply()`: comment lời gọi `autoAssignSupplyManager()`
- [x] `ContractService`: ghi chú "tạm ngưng dùng" cho 4 hàm `autoAssignSupplyManager` / `notifySupplyAssignNeeded` / `findSupplyManagerId` / `assignSupplyEmployee` (giữ nguyên code)
- [x] `Modules/Supply/Routes/api.php` — comment route `PUT /rendered-contracts/{contract}/assign-employee`
- [x] `Modules/Supply/Http/Controllers/Api/V1/RenderedContractController.php` — comment method `assignEmployee()`
- [x] `Modules/Supply/Services/RenderedContractService.php` — comment method `assignEmployee()`
- [x] `Modules/Supply/Transformers/RenderedContract/RenderedContractResource.php` — comment 3 key `supply_manager_id`, `supply_manager_name`, `can_assign_supply_employee`
- [x] `php -l` các file đã sửa

## FE
- [x] `pages/supply/contract_render/index.vue` — comment: nút "Phân công lập phiếu đề xuất cung ứng", slot `cell(supply_manager_name)`, import + đăng ký + thẻ `AddEmployeeCreateSupplyProposalModal`, data `selectedContractId`, method `showAssignModal()` + `assignSupplyEmployee()`
- [x] `pages/supply/contract_render/constants.js` — comment cột `supply_manager_name`
- [x] Giữ nguyên file `components/modals/AddEmployeeCreateSupplyProposalModal.vue`

## Verify
- [x] Grep: không còn tham chiếu `supply_manager` / `can_assign_supply_employee` đang hoạt động (chỉ còn trong code đã comment)
- [ ] User test: đăng nhập user KHÔNG phải người được phân công → Cung ứng → Hợp đồng đã kết xuất → thấy nút "Tạo phiếu đề xuất cung ứng" và lập được phiếu
- [ ] Cột "NV phụ trách cung ứng" và nút Phân công không còn hiển thị
- [ ] Kết xuất 1 HĐ mới → không sinh thông báo phân công

⚠️ Sửa cả BE lẫn FE → build lại client + hard refresh.

### Checkpoint — 15/09/2026
Vừa hoàn thành: toàn bộ BE + FE (comment lại code phân công, không xóa). `php -l` 6 file BE sạch; compile thử template + script + constants của `contract_render` bằng vue-template-compiler → sạch, render function không còn tham chiếu `supply_manager` / `can_assign_supply_employee`. Bổ sung ngoài plan: comment eager-load `supplyManager.info` trong `RenderedContractService::getList()`.
Đang làm dở: không có.
Bước tiếp theo: build lại client + hard refresh, user test trên trình duyệt (3 mục Verify còn lại).
Blocked:
