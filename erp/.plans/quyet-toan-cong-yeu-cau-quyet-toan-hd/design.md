# Design — Điều kiện quyết toán công: yêu cầu đã quyết toán HĐ

## Mục tiêu

Thay đổi điều kiện cho phép **quyết toán công** (màn HRM `assign/settlement_contract/create`).
Quy tắc mới (thống nhất): hợp đồng phải **quyết toán HĐ xong** thì mới được quyết toán công —
áp dụng cho **HĐ bán / ĐHNT / HĐDV**. Riêng **PBH / YCGVK** giữ nguyên điều kiện cũ ("giao việc xong").

## Bối cảnh luồng

- Màn chính ở HRM (`hrm-client/pages/assign/settlement_contract/create.vue`).
- HRM BE (`Modules/Assign/.../SettlementContractController@getDataForSettlementContract`) gọi sang ERP:
  1. `GET {ERP_URL}/admin/checkContractIsDone?contract_id=&contract_type=` ← **nơi check điều kiện** (file cần sửa)
  2. `GET {ERP_URL}/hrm/wr_service_contracts/apiGetDataForSettlement?...` ← lấy dữ liệu công
- File sửa duy nhất: `ERP/TanPhatDev/app/Http/Controllers/Common/CheckContractIsDoneController.php@checkContractIsDone`
- Blast radius thấp: `checkContractIsDone` chỉ được HRM gọi (route `admin/checkContractIsDone`).

## Ánh xạ loại HĐ ↔ phân biệt tại contract-level

| Loại | contract_type | Phân biệt | Điều kiện mới |
| ---- | ------------- | --------- | ------------- |
| HĐ bán | `firm` | `FirmContract` | `status == DA_QUYET_TOAN (10)` |
| ĐHNT | `firm` | `FirmContract.type = 8` | `status == DA_QUYET_TOAN (10)` (như HĐ bán) |
| HĐDV (+ phụ lục) | `wr` | `WrServiceContract.type != BAO_HANH(2)` | `status == DA_QUYET_TOAN (5)` |
| PBH (bảo hành) | `wr` | `WrServiceContract.type == BAO_HANH(2)` | GIỮ CŨ: "giao việc xong" |
| YCGVK | `firm` | (không có dòng riêng — luôn nằm trong 1 FirmContract) | theo HĐ firm = cần quyết toán HĐ |

### Quyết định (Phương án A)
- Mọi dòng `firm` trong danh sách quyết toán công đều là một `FirmContract` thật (HĐ bán/ĐHNT) —
  YCGVK độc lập (`firm_contract_id` null) bị lọc khỏi danh sách (`whereNotNull('contractable_code')`),
  nên KHÔNG có dòng "HĐ thuần YCGVK". → Nhánh `firm` chỉ cần check `status == 10`.
- "Quyết toán HĐ xong" dùng **`status` của HĐ** làm nguồn chân lý (FirmContract=10, WrServiceContract=5),
  vì khi `SettlementContract` duyệt (`DA_DUYET=5`) → `markSettlement()` → `markSettlementContract()`
  tự set status HĐ. Không cần truy bảng settlement.

## Hằng số tham chiếu
- `FirmContract::DA_QUYET_TOAN = 10`
- `WrServiceContract::DA_QUYET_TOAN = 5`, `WrServiceContract::BAO_HANH = 2`

## Message khi chưa đủ điều kiện
"Hợp đồng chưa quyết toán, không thể quyết toán công" (FE hiển thị toast warning từ `data.message`).

## Phạm vi KHÔNG đổi
- FE HRM, HRM BE: không sửa (chỉ tiêu thụ `status`/`message` trả về như cũ).
- Logic "giao việc xong" giữ nguyên cho nhánh PBH.
