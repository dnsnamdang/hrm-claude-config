# Design (tóm tắt) — Dọn biến mẫu in sai/thừa toàn bộ loại QĐ

- **Người phụ trách**: @manhcuong · **Ngày**: 2026-07-15
- **Spec đầy đủ**: `docs/superpowers/specs/2026-07-15-decision-print-cleanup-invalid-variables-design.md`

## Mục tiêu

Rà 21 loại QĐ, gỡ biến mẫu in mà bản chất loại đó không có (vd: QĐ chấm dứt HĐLĐ không có "phòng ban/bộ phận/chức vụ **trước thay đổi**").

## Cách rà (không đoán)

2 script đối chiếu tự động:
1. **Biến chết** = khai trong picker nhưng controller không fill → `clearNull()` xoá → luôn in rỗng. Bắt được **11** (loại gộp).
2. **Sai ngữ nghĩa** = hậu tố `_TRUOC/SAU_THAY_DOI` ở loại KHÔNG phải thay đổi. Bắt được **15** — đây mới là vấn đề user nêu (chúng vẫn được fill, chỉ vô nghĩa).

Rồi đối chiếu usage data thật (675 decisions + 55 print_templates) tách theo loại QĐ.

## 4 nhóm — xử lý KHÁC nhau

| Nhóm | Loại QĐ | Số biến | Chốt |
|---|---|---|---|
| 1 | Chấm dứt (4) + Tạm hoãn (3) | 7 | **Bỏ khỏi picker, GIỮ fill** — trùng biến thường (cùng nguồn); giữ fill để mẫu id=18 + Decision#669 không vỡ |
| 2 | Nghỉ hưu (5) + Kỷ luật (3) | 8 | **Đổi tên sang biến thường** — KHÔNG có biến thường thay thế, bỏ là mất thông tin |
| 3 | Loại gộp chấm dứt/tạm hoãn | 11 | **Bỏ cả khối** — 0 QĐ, 0 mẫu, không có `print()` |
| 4 | 2 QĐ tiếp nhận #511/#512 | 3 key | Sửa key sang `PHONG_BAN_TIEP_NHAN`/`CHUC_VU`/`NGUOI_QUAN_LY_TRUC_TIEP` |

## Phát hiện đáng chú ý

1. **QĐ tiếp nhận KHÔNG có biến `PHONG_BAN`** — biến đúng là `PHONG_BAN_TIEP_NHAN`. Nếu không kiểm tra thì đã thay biến rỗng bằng biến rỗng khác.
2. **ĐÍNH CHÍNH Nhóm 4**: Decision#511/#512 **đã bị xoá mềm** (`deleted_at` có giá trị) + không có bản ghi `accept_personnels` → không in được, không ảnh hưởng ai. Phân tích đầu THIẾU lọc `deleted_at`. Sửa vẫn giữ (vô hại, đúng nếu khôi phục).
3. **Usage đúng sau khi lọc QĐ đã xoá**: chỉ **1 QĐ còn sống** (Decision#669, Chấm dứt) chịu rủi ro → đã bảo vệ bằng "giữ fill".
4. 6/102 QĐ tiếp nhận mồ côi (không có bản ghi chi tiết) — vấn đề sẵn có, ngoài scope.

## Phạm vi

**3 file BE + data 2 QĐ. Không migration / permission / git.**

| File | Việc |
|---|---|
| `PrintTemplateVariable.php` | Nhóm 1 bỏ 7 dòng; Nhóm 2 đổi tên 8 dòng; Nhóm 3 làm rỗng khối loại gộp |
| `RetirementController.php` | đổi 5 key fill |
| `EmployeeDisciplineController.php` | đổi 3 key fill |
| data `decisions#511/#512` | thay 3 key |

**KHÔNG đụng**: Termination/Suspend controller (giữ fill), 3 QĐ thay đổi (Bổ nhiệm/Điều chuyển/Điều chỉnh lương — giữ đủ 18 biến trước/sau).

## Verify

Sau khi sửa: **0 biến sai loại** (trước 15), **0 biến chết** (trước 11). Runtime Decision#669 `PHONG_BAN_TRUOC_THAY_DOI` VẪN in "Phòng Kinh doanh upservice" = đúng `PHONG_BAN` (xác nhận trùng lặp + giữ fill hiệu quả). Runtime Kỷ luật #527 `PHONG_BAN` = "Phòng Nhân sự hành chính", key cũ đã rỗng. Nghỉ hưu KHÔNG test được (0 bản ghi trong DB) — code đối xứng với Kỷ luật.

---

## Đợt 2 — Bỏ loại gộp khỏi droplist + 3 biến nghĩa vụ/quyền lợi

**Bỏ loại gộp**: đợt 1 mới làm rỗng khối biến — chưa đủ, loại vẫn hiện trong droplist. Droplist build thẳng 1-1 từ `Decision::TYPE` nên phải cắt từ đó. Kiểm tra trước khi xoá: 0 mẫu in + 0 QĐ (kể cả xoá mềm) dùng loại này, grep repo 0 tham chiếu → xoá cả dòng `TYPE` lẫn const.

**3 biến mới** (nguồn có sẵn, chỉ thiếu khai báo + fill; đều là textarea → `nl2br()`):

| Loại QĐ | Biến | Nguồn |
|---|---|---|
| Chấm dứt HĐLĐ | `NV_PHAI_THUC_HIEN_KHI_CHAM_DUT_HDLD` | `termination_labor_contracts.obligation` |
| Tạm hoãn HĐLĐ | `NV_PHAI_THUC_HIEN_KHI_TAM_HOAN_HDLD` | `suspend_labor_contracts.obligation` |
| Tạm hoãn HĐLĐ | `QUYEN_LOI_DUOC_HUONG_KHI_TAM_HOAN_HDLD` | `suspend_labor_contracts.entitlement` |

**Bẫy**: QĐ tạm hoãn có 2 hàm in (`print()` mẫu QĐ + `printAgreement()` mẫu thoả thuận) dùng chung pool biến → fill cả hai, nếu không thì mẫu thoả thuận in rỗng.

**4 file BE. Không migration / permission / git.**

**Verify**: droplist 20 loại (hết loại gộp, 2 loại riêng nguyên); runtime Chấm dứt in đúng nội dung + biến control ra rỗng; Tạm hoãn 0 bản ghi thật → test qua transaction + rollback, cả 2 hàm in đúng; browser thật màn thêm mẫu in render đủ 3 biến.
