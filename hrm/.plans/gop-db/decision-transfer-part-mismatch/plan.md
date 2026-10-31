# QĐ điều chuyển nhân sự — bộ phận sau điều chuyển không thuộc phòng ban (Redmine: chưa có số) — @cuong61n

## Phase 1 — Điều tra

- [x] (31/10/2026) Điều tra vì sao nhiều QĐ điều chuyển có "Bộ phận sau điều chuyển" không thuộc "Phòng ban sau điều chuyển"
  - Nghiệp vụ: chọn NV → cột "Sau điều chuyển" chép nguyên từ "Hiện tại" (cả phòng ban lẫn bộ phận). Đổi phòng ban nhưng ô bộ phận không tự xoá → bộ phận phòng cũ bị lưu vào QĐ; duyệt QĐ → phụ lục HĐ chép theo → ghi vào hồ sơ NV.
  - Kỹ thuật: `InfoFormComponent.vue` watcher `formSubmit.new.department_id` không reset `new.part_id`; BE `TransferPersonnelRequest` không có rule `new.part_id`; `AppendixLaborContractService` ~dòng 602 ghi `employee_infos.part_id`.
  - Kiểm: local 14/38 QĐ lệch, prod 14/44 QĐ lệch — 100% là bộ phận cũ giữ nguyên khi đổi phòng.

## Phase 2 — Sửa code (nhánh gop_db)

### FE
- [x] (31/10/2026) `pages/decision/transfer-personnel/components/InfoFormComponent.vue`: đổi phòng ban → xoá `new.part_id`/`new.part_name` nếu bộ phận không thuộc phòng mới; hiện lỗi BE dưới ô Bộ phận (`formError['new.part_id']`)

### BE
- [x] (31/10/2026) `TransferPersonnelRequest`: rule `new.part_id` nullable|integer + phải thuộc `new.department_id`, sai trả 422 "Bộ phận không thuộc phòng ban sau điều chuyển"

### Test (local, stack develop — 2 file giống hệt gop_db)
- [x] API: bộ phận sai phòng → 422 đúng câu; đúng phòng / để trống → không lỗi bộ phận
- [x] Playwright màn Tạo mới: chọn NV Đinh Văn Vinh → PB/BP chép đúng (CSKH / BP Bảo hành); đổi sang HN_XNK → `part_id` = null, ô hiện "Chọn bộ phận"
- [x] Playwright màn Sửa QĐ 21, 22 (dữ liệu đúng) → giữ nguyên bộ phận khi mở

### Đẩy & deploy
- [x] (31/10/2026) Push thẳng `gop_db`: hrm-api `583b27969`, hrm-client `31988bd13`
- [x] (31/10/2026) Deploy PROD bằng `~/build_tpe.sh` (chỉ 2 commit này, không migration), FE 200

## Phase 3 — Sửa dữ liệu PROD (`hrm_erp_gop`, 31/10/2026)

- [x] Sao lưu dòng bị đụng: `~/backup_fix/transfer_part_20261031_{dtp,alc,ei}.sql` trên hrm-prod
- [x] 14 QĐ điều chuyển (đều đã duyệt): `new_part_id`/`new_part_name` → NULL (không đoán bộ phận đúng)
- [x] 14 phụ lục HĐ sinh từ các QĐ đó: `new_part_id`/`new_part_name` → NULL
- [x] 8 hồ sơ NV còn đang mang bộ phận sai (QĐ 1, 2, 23, 30–33, 37): `employee_infos.part_id` → NULL; 6 NV khác đã đổi bộ phận về sau → không đụng
- [x] Kiểm lại: 0 QĐ lệch, 0 phụ lục lệch
- Lưu ý: sửa bằng SQL nên không ghi lịch sử thay đổi hồ sơ NV; HR cần chọn lại bộ phận đúng cho 8 NV nếu có
- [ ] Local `local_hrm_erp` chưa sửa dữ liệu (14 QĐ lệch còn nguyên)
