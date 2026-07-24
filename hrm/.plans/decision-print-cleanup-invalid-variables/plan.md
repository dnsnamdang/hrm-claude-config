# Plan — Dọn biến mẫu in sai/thừa toàn bộ loại QĐ

@manhcuong · Spec: `docs/superpowers/specs/2026-07-15-decision-print-cleanup-invalid-variables-design.md`

## Phase 0 — Rà soát (XONG, có bằng chứng)

- [x] Script đối chiếu picker vs controller fill → 11 biến chết (loại gộp)
- [x] Script rà ngữ nghĩa `_TRUOC/SAU_THAY_DOI` ở loại không phải thay đổi → 15 biến sai loại
- [x] Đối chiếu usage data thật (675 decisions + 55 print_templates) tách theo loại QĐ
- [x] Xác minh biến thay thế TỒN TẠI + được fill trước khi đề xuất (chặn được: QĐ tiếp nhận KHÔNG có `PHONG_BAN`, phải dùng `PHONG_BAN_TIEP_NHAN`)

## Phase 1 — Nhóm 1: bỏ khỏi picker, GIỮ fill (7 biến)

### BE
- [x] `PrintTemplateVariable.php` — Chấm dứt HĐLĐ: bỏ 4 dòng `PHONG_BAN_/BO_PHAN_/CHUC_VU_/NGUOI_QUAN_LY_TRUC_TIEP_TRUOC_THAY_DOI`
- [x] `PrintTemplateVariable.php` — Tạm hoãn HĐLĐ: bỏ 3 dòng `PHONG_BAN_/BO_PHAN_/CHUC_VU_TRUOC_THAY_DOI`
- [x] KHÔNG đụng Termination/Suspend controller (giữ fill để mẫu id=18 + Decision#669 vẫn in đúng)

## Phase 2 — Nhóm 2: đổi tên (8 biến)

### BE
- [x] Kiểm tra key mới chưa bị dùng trong picker/controller Nghỉ hưu + Kỷ luật (tránh đè giá trị)
- [x] `PrintTemplateVariable.php` — Nghỉ hưu: đổi 5 key sang `PHONG_BAN`/`BO_PHAN`/`CHUC_VU`/`CHUC_DANH`/`NGUOI_QUAN_LY_TRUC_TIEP`
- [x] `PrintTemplateVariable.php` — Kỷ luật: đổi 3 key sang `PHONG_BAN`/`BO_PHAN`/`CHUC_VU`
- [x] `RetirementController.php`: đổi 5 key fill tương ứng
- [x] `EmployeeDisciplineController.php`: đổi 3 key fill tương ứng

## Phase 3 — Nhóm 3: bỏ khối chết (11 biến)

### BE
- [x] `PrintTemplateVariable.php`: bỏ khối `TYPE_TERMINATION_AND_SUSPEND_LABOR_CONTRACT` (0 QĐ, 0 mẫu, không có print())

## Phase 4 — Nhóm 4: sửa data 2 QĐ tiếp nhận

- [x] Backup `print_template` của Decision#511 + #512
- [x] Thay `{{PHONG_BAN_TRUOC_THAY_DOI}}`→`{{PHONG_BAN_TIEP_NHAN}}`, `{{CHUC_VU_TRUOC_THAY_DOI}}`→`{{CHUC_VU}}`, `{{NGUOI_QUAN_LY_TRUC_TIEP_TRUOC_THAY_DOI}}`→`{{NGUOI_QUAN_LY_TRUC_TIEP}}`
- [x] ĐÍNH CHÍNH: KHÔNG verify được — Decision#511/#512 ĐÃ XOÁ MỀM (`deleted_at` có giá trị) + 0 bản ghi `accept_personnels` → không in được. Phân tích đầu thiếu lọc `deleted_at`. Sửa vẫn giữ (vô hại)

## Phase 5 — Verify

- [x] `php -l` sạch 3 file BE
- [x] Chạy lại 2 script rà soát → 0 biến sai loại, 0 biến chết
- [x] Picker Chấm dứt/Tạm hoãn: không còn 7 biến, biến thường còn nguyên
- [x] Runtime `print()` Decision#669 (Chấm dứt): `PHONG_BAN_TRUOC_THAY_DOI` VẪN ra giá trị (giữ fill)
- [x] Picker Nghỉ hưu/Kỷ luật: key mới có, key cũ mất
- [x] Runtime Kỷ luật #527: `PHONG_BAN` = 'Phòng Nhân sự hành chính' (key mới đổ đúng), `PHONG_BAN_TRUOC_THAY_DOI` rỗng
- [x] Runtime Nghỉ hưu: KHÔNG test được — 0 bản ghi `retirements` trong DB; code đối xứng Kỷ luật (cùng script đổi key), đã review tay
- [x] Picker loại gộp: chỉ còn biến chung
- [x] 29 QĐ Điều chuyển KHÔNG bị ảnh hưởng
- [x] Khôi phục mọi template test đã sửa tạm

### Checkpoint — 2026-07-15
Vừa hoàn thành: Toàn bộ Phase 0-5. 3 file BE + data 2 QĐ (đã xoá mềm). Rà soát: 15 biến sai loại + 11 biến chết -> 0/0.
Đang làm dở: (không)
Bước tiếp theo: User verify picker trên browser 4 loại QĐ (Chấm dứt/Tạm hoãn/Nghỉ hưu/Kỷ luật).
Blocked: (không)

## Phase 6 — Bỏ hẳn loại gộp khỏi picker + bổ sung 3 biến nghĩa vụ/quyền lợi

### BE
- [x] Xác minh 0 `print_templates` + 0 `decisions` dùng `termination_and_suspend_labor_contracts` trước khi bỏ
- [x] `Decision.php`: bỏ dòng `TYPE` + const `TYPE_TERMINATION_AND_SUSPEND_LABOR_CONTRACT` (droplist màn thêm mẫu in build thẳng từ `Decision::TYPE`)
- [x] `PrintTemplateVariable.php`: bỏ nốt khối rỗng của loại gộp
- [x] `PrintTemplateVariable.php` — Chấm dứt HĐLĐ: thêm `NV_PHAI_THUC_HIEN_KHI_CHAM_DUT_HDLD` (nguồn `termination_labor_contracts.obligation`)
- [x] `PrintTemplateVariable.php` — Tạm hoãn HĐLĐ: thêm `NV_PHAI_THUC_HIEN_KHI_TAM_HOAN_HDLD` + `QUYEN_LOI_DUOC_HUONG_KHI_TAM_HOAN_HDLD` (nguồn `obligation` / `entitlement`)
- [x] `TerminationLaborContractController::print()`: fill `NV_PHAI_THUC_HIEN_KHI_CHAM_DUT_HDLD` (nl2br)
- [x] `SuspendLaborContractController::print()` + `printAgreement()`: fill 2 biến mới (nl2br) — 2 hàm dùng chung pool biến nên phải fill cả hai, tránh biến chết ở mẫu thoả thuận

### Verify
- [x] `php -l` sạch
- [x] `getSubTypes` không còn loại gộp; 20 loại còn lại nguyên
- [x] Picker Chấm dứt/Tạm hoãn có biến mới
- [x] Runtime `print()` ra đúng nội dung nghĩa vụ/quyền lợi (có control: biến phải rỗng trước khi fill)
- [x] `grep` toàn repo: không còn tham chiếu const đã xoá
- [x] Browser thật `/decision/category/print_templates/add`: droplist 20 loại, KHÔNG còn loại gộp; bảng biến render `NV_PHAI_THUC_HIEN_KHI_CHAM_DUT_HDLD` (Chấm dứt) và 2 biến mới (Tạm hoãn)
- [x] Runtime Tạm hoãn: 0 bản ghi thật → dựng bản ghi trong `DB::transaction` + `rollBack`, gọi `print()` + `printAgreement()` THẬT, cả 2 ra đúng nội dung, `nl2br` giữ xuống dòng, biến control ra rỗng; rollback sạch (bảng về 0 bản ghi)

### Checkpoint — 2026-07-15 (Phase 6)
Vừa hoàn thành: Bỏ loại QĐ gộp khỏi droplist mẫu in + thêm 3 biến nghĩa vụ/quyền lợi (Chấm dứt 1, Tạm hoãn 2), fill ở 3 hàm in.
Đang làm dở: (không)
Bước tiếp theo: User verify trên browser màn thêm mẫu in + dựng mẫu in dùng biến mới.
Blocked: (không)

### Sự cố đã xử lý
Script sửa PrintTemplateVariable.php lần đầu dùng "khối kế tiếp" làm mốc kết thúc -> khối CUỐI (loại gộp) nuốt luôn dấu đóng mảng + phần còn lại class -> PHP Parse error "Unclosed '['". Khôi phục từ backup (đã cp trước khi chạy), sửa script cắt khối theo dấu `],` đúng indent.
