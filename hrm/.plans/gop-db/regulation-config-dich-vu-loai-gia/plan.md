# Khai quy chế — dòng Dịch vụ lưu Loại giá 0 làm báo giá chỉ-dịch-vụ báo "Không tìm được quy chế phù hợp"

Vé: phòng NSHC (HN_NSHC, dept 43, cty 1) có quy chế dịch vụ nhưng lập báo giá vật tư chỉ gồm dịch vụ (BG 65547) bị báo chưa có quy chế.

## Nguyên nhân (kiểm DB hrm_erp_gop 20/11/2026)
- BG 65547: price_type=1, 0 dòng hàng, 2 dòng chi phí → tra quy chế condition_type [1,2].
- ERP `SupportAccountingService::getRegulations` (và HRM `ContractSupportAccountingService::getRegulations`) lọc `condition_sale_type = price_type HĐ`.
- HRM `RegulationConfigService::fillGridRow` ghi Dịch vụ `condition_sale_type = 0` → quy chế 702/703 không bao giờ khớp.
- ERP cũ: ô Loại giá ẩn khi Dịch vụ (từ b2a57b8382, 24/01/2022) nhưng form giữ mặc định '1' → 86 quy chế DV loại giá 1, 1 quy chế loại 2.

## Quyết định (user chốt "cách 2", 20/11/2026)
Giữ hành vi ERP cũ: HRM lưu Dịch vụ với Loại giá 1; KHÔNG sửa hàm tra quy chế dùng chung.

## Task
- [x] Test `service_condition_type_saves_condition_sale_type_one_like_erp` (RED 0≠1 → GREEN)
- [x] `RegulationConfigService::fillGridRow`: Dịch vụ → 1
- [x] Sửa dữ liệu hrm_erp_gop: regulations 702, 703 condition_sale_type 0→1 (giữ updated_at); còn 0 dòng DV loại giá 0
- [x] Commit+push 20/11: hrm-api develop c5ee6418b, gop_db af52888fe (local develop b6a8df1e0)

### Checkpoint — 2026-11-20
Vừa hoàn thành: fix code + data; RegulationHoahongGridTest 10/10, RegulationTabRegistryTest 11/11
Đang làm dở: —
Bước tiếp theo: deploy; user thử lại BG 65547
Blocked:
