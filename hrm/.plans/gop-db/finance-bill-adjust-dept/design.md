# Design (tóm tắt) — Phiếu kế toán (ERP `bill_adjust_dept` → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo, code thẳng trên nhánh này — không tách nhánh riêng) · Ngày: 2026-08-28
> **Spec đầy đủ**: `docs/superpowers/specs/gop-db/2026-08-28-finance-bill-adjust-dept-design.md`
> Feature tiền nhiệm: `.plans/gop-db/finance-bill-adjust-dept-request/` (màn Đề nghị — đã port xong)

---

## Mục tiêu

Port màn ERP `admin/income-expenditure/bill_adjust_dept?_type=all` — menu ERP gọi là
**"Phiếu kế toán"** — sang HRM, phân hệ **Tài chính**, route `/finance/bill-adjust-depts`.

Đây là chứng từ **ghi bút toán vào sổ cái**: kế toán chốt các cặp Nợ/Có theo nhóm định khoản, bấm
*Lưu và duyệt* → hệ thống ghi vào `account_details` + `account_detail_refs`. Là mắt xích cuối của
luồng đã port dở:

```
Đề nghị điều chỉnh công nợ ─┐
   (đã có ở HRM)            ├─ (duyệt) → PHIẾU KẾ TOÁN → ghi sổ cái account_details
Đề nghị hạch toán bổ sung ──┘              (feature này)
   (đã có ở HRM)
```

**Nguyên tắc user chốt: "cứ làm hệt như ERP, vì giờ đã dùng chung DB rồi nên dữ liệu vẫn lấy được hết."**

## Scope

**Trong**: 5 cửa vào tạo phiếu · danh sách 11 cột + 12 ô lọc · tạo/sửa/xóa · **Lưu và duyệt ⇒ ghi sổ
cái** · nghiệp vụ điều chỉnh **số dư lẻ** · 3 popup chọn (đối tượng / hợp đồng / phiếu YC xuất hàng)
· in khổ ngang · xuất Excel phiếu + danh sách · thông báo chuông.

**Ngoài**: không port 2 màn nguồn còn thiếu (Hạch toán hoa hồng tháng, Chi phí giao nhanh) — chỉ
nhận deep-link · không đụng repo ERP · không thêm bảng DB nào.

## Quyết định lớn (user chốt 2026-08-28)

| # | Quyết định |
| --- | --- |
| 1 | Port **hệt ERP**, đủ **5 cửa vào** tạo phiếu |
| 2 | Ô chọn hợp đồng bán tìm **cả `hrm_contracts` lẫn `firm_contracts`**, lưu đúng morph tương ứng |
| 3 | Phân quyền xem **2 cấp như ERP** (tổng công ty / công ty); ngoài ra chỉ xem phiếu mình lập |
| 4 | Sửa/Xóa = **Đang tạo VÀ đúng người lập** (hệt `canEdit`/`canDelete` ERP) |
| 5 | **Dùng chung 2 bảng ERP** `bill_adjust_depts` + `bill_adjust_dept_details` — **0 migration** |
| 6 | **Duyệt ⇒ HRM ghi thẳng vào sổ cái `account_details`** — gỡ ràng buộc "HRM không ghi sổ" của feature tiền nhiệm |
| 7 | Màn in **tự dựng khung Vue** theo bố cục mẫu ERP `report_templates` id 208, không render HTML mẫu |

## Khác biệt có chủ đích so với ERP (9 điểm — chi tiết ở spec §11)

1. Sinh mã bọc transaction + `lockForUpdate` (2 cổng cùng sinh dễ trùng).
2. "Đang tạo" đổi từ **đỏ → xám** (ERP gán `danger`, sai bảng màu SRS).
3. Số dư lẻ: tra tài khoản theo `identify_number = 1311` thay vì hard-code `account_id == 22` (ERP thiếu TK là nổ 500).
4. Ghi sổ: kiểm null từng mắt xích khi tra `billable_*` (ERP deref thẳng, thiếu 1 bảng là 500).
5. `date_accounting` nhận **ISO**, không nhận `dd/mm/yyyy` (luật `date` của Laravel hiểu `m/d/Y` → form chết từ ngày 13).
6. Validate chi tiết **trước** khi tạo phiếu (ERP tạo phiếu rồi mới validate → để lại phiếu rác).
7. Route đọc không gắn `checkPermission` (spatie bỏ sót role `model_type='App\Employee'`), gate trong service.
8. Letterhead lấy theo **`company_id` trên chứng từ**, không theo người tạo phiếu (ERP sai, CLAUDE.md cấm).
9. Chặn nhảy cóc trạng thái ở BE (ERP gán thẳng `$request->status` từ FE).

## Rủi ro đã biết

- 🔴 **Ghi sổ cái dùng chung với cổng ERP** — sai hoặc trùng là lệch số kế toán thật, không hoàn tác.
  Giảm thiểu: tách hàm thuần `buildEntries()` để unit test, đối chiếu với bút toán phiếu ERP có sẵn,
  mọi thao tác thử bọc transaction rồi rollback.
- 🟡 Nhánh `exportable_*` có **0/33.409 dòng** dữ liệu thật → port theo code ERP, không kiểm chứng được.
- 🟡 Cửa vào 4 (hoa hồng tháng) & 5 (giao nhanh) chưa có màn nguồn ở HRM → chỉ nhận deep-link, chưa bấm thật được.
- 🟡 Chỉ **2 phiếu** đang ở trạng thái *Đang tạo* → phải seed dữ liệu test mới thử được luồng sửa/xóa.
- 🟢 Phiếu HRM gắn `hrm_contracts` mở bên ERP lỗi *Class not found* — hệ quả đã biết, chấp nhận từ màn Đề nghị.

## Số liệu nền (DB `gop_db`, 2026-08-28)

**12.628 phiếu** · 33.409 dòng chi tiết (2025: 5.663 · 2026: 6.965).
Trạng thái: Đã duyệt 12.626 · Đang tạo 2 · Hủy 0.
Nguồn tạo: Phiếu YCĐC **10.002** · Hạch toán bổ sung **1.817** · nhập tay **809** · hoa hồng tháng **0**.
`objectable_type`: Customer 25.472 · Supplier 6.870 · Employee 674 · Department 60 — **cả 4 chưa có
trong morphMap**, phải bổ sung. `exportable_type`: **0 dòng**.

## Kết quả triển khai (2026-08-28) — CODE DONE 52/54 task

| Lớp | Sản phẩm |
| --- | --- |
| BE | **20 file mới** + 4 file sửa · **17 route** · 2 quyền id 1551-1552 · 4 morphMap bổ sung |
| FE | **9 file mới** + 1 file sửa (menu) · danh sách 11 cột / 12 ô lọc · form 18 cột · 3 popup · chi tiết · màn in khổ ngang |
| DB | **0 bảng mới, 0 migration** — dùng nguyên 2 bảng ERP |

**Đã chứng minh bằng số liệu thật:**
- Ghi sổ cái: **150 phiếu ERP ngẫu nhiên / 403 dòng bút toán / 33 cột + toàn bộ tài khoản đối ứng
  khớp tuyệt đối** với sổ cái cổng ERP đã ghi.
- Phạm vi quyền 3 nhánh + Super admin khớp SQL tuyệt đối trên 6 nhân viên thật.
- Vòng đời lưu nháp → sửa → duyệt → chặn sửa/xoá phiếu đã duyệt: đúng hết, bọc transaction rollback.
- 4/5 luật validate nhóm định khoản chặn đúng; 10 endpoint smoke test 200; FE 9/9 compile sạch.

**2 lỗi thật do vòng đối chiếu sổ cái bắt được (đã sửa):**
1. `optional(null)` trong PHP trả về OBJECT chứ không phải null → nhánh dự phòng "lấy người lập
   phiếu khi hợp đồng không có người lập" không bao giờ chạy (58/359 dòng lệch `company_id`).
2. Entity hợp đồng của HRM **không có quan hệ `employee_create`** như `App\BaseModel` của ERP, mà
   Eloquent trả `null` im lặng cho thuộc tính không tồn tại → `created_by` của bút toán lấy nhầm
   người lập phiếu thay vì người lập hợp đồng (280/411 dòng lệch). Đã đổi sang tra thẳng theo
   `created_by`, gom 1 query, không đụng 9 entity hợp đồng dùng chung.

**Thêm 2 sửa lỗi ERP có chủ đích ngoài danh sách ban đầu:**
- Ô lọc "STK ngân hàng" của ERP lọc cột `account_number` — **cột không tồn tại** trên
  `bill_adjust_dept_details` (cột thật là `bank_account_number`) → ô lọc đó của ERP không bao giờ ra kết quả.
- ERP xoá phiếu kế toán **không trả trạng thái** cho Yêu cầu hạch toán bổ sung → đề nghị kẹt ở
  *Đang duyệt* vĩnh viễn. HRM trả về *Chờ duyệt*.

**Còn lại (không chặn):** seeder dữ liệu test (DB chỉ có 2 phiếu *Đang tạo*) và toàn bộ FE chưa mở
trình duyệt bấm thật. Danh sách phần **chưa kiểm chứng được** nằm ở cuối `plan.md`.


## Kiểm thử Playwright + đối chiếu ERP (2026-08-28)

Chạy thật 2 cổng song song (HRM `:3000` ↔ ERP `:8002`, cùng tài khoản, cùng DB).
**20/20 bộ lọc khớp tuyệt đối**; danh sách, sort, phân trang, ghi nhớ bộ lọc, 3 popup, cửa vào từ
Phiếu YCĐC, duyệt-ghi-sổ, xoá, in và xuất Excel đều bấm thật.

**Tìm và sửa 7 lỗi** (chi tiết ở `plan.md` Phase 10) — đáng chú ý nhất:
- ô lọc **NVKD chết hoàn toàn** (ERP 84 phiếu / HRM 0) do lọc id trên cột chứa tên;
- **Excel danh sách mất 9/11 cột** do helper `buildQueryString()` serialize mảng không có `[]`;
- cột **Phòng ban** lấy sai nguồn; **bản in** lệch ERP 6 điểm.

Ngoài ra chứng minh được **ô lọc "STK ngân hàng" của ERP nổ HTTP 500** (`Unknown column
'account_number'`) — HRM lọc đúng cột.

⚠️ Có duyệt 1 phiếu TEST qua giao diện để kiểm luồng ghi sổ, **đã dọn sạch**: `account_details`
trở về đúng 972.053 dòng / max id 1001536 như trước khi test.
