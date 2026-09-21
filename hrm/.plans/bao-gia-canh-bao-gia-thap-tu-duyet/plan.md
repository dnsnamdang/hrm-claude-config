# Plan — Báo giá: cảnh báo đơn giá ≤ 1.000 & tự động duyệt (#10797)

## Phase 1 — Logic phê duyệt (BE)

- [x] `QuotationService::LOW_PRICE_THRESHOLD = 1000`
- [x] `QuotationService::isAutoApprovable()` — không GG + không hàng/DV tạm + mọi đơn giá bán > 1.000 + báo giá không rỗng
- [x] `calculateLevel()` ép `level = 1` khi thoả TH1, trả thêm cờ `auto_approve` (submit() dùng lại nên tự chạy đúng)

## Phase 2 — Cảnh báo đơn giá thấp (FE)

- [x] Component mới `QuotationLowPriceWarningModal.vue` (bảng Mã/Tên/Đơn giá, 2 nút, footer ghim đáy)
- [x] `edit.vue`: computed `lowPriceItems` + `lowPriceKeySet`, cờ `lowPriceHighlight` / `lowPriceModalShow`
- [x] `edit.vue`: tô nền cam dòng vi phạm (class `.low-price-row`, áp cho cả dòng cha và dòng con)
- [x] `edit.vue`: `openSubmit()` chèn bước cảnh báo; `onLowPriceContinue()` mở popup gửi duyệt
- [x] `QuotationSubmitModal.vue`: hiển thị "Tự động duyệt" + câu giải thích khi `auto_approve`

## Phase 3 — Rà lại theo skill + test thật

- [x] `button-convention`: sửa nút "Tiếp tục gửi duyệt" → `primary status="warning"` + `ri-send-plane-line` (trước đó sai: `primary` teal + `ri-check-line`)
- [x] `button-convention` mục 4.2: đổi chữ nút theo bảng chuẩn — "Tiếp tục trình duyệt" → **Tiếp tục gửi duyệt**, "Quay lại chỉnh sửa" → **Quay lại**
- [x] `modal-popup` mục 0: triệt `margin-top`/`margin-bottom` khối đầu-cuối trong body popup
- [x] Sửa icon khoá ô GG bị ĐỎ: theme `custom-assign.scss` đặt `.text-muted { color: #dc3545 !important }` cho cả phân hệ Giao việc → dùng lớp riêng `.text-soft` (#6b7280), bám pattern `SummaryQuotationForm.vue`
- [x] Bổ sung quy tắc "skill thắng spec về hình thức UI" vào CLAUDE.md

## Kết quả test (2026-08-17, cổng 3000/8000, tài khoản DNS Admin)

**BE — `isAutoApprovable()` (chạy trong transaction rồi rollback, dữ liệu thật không đổi):**

| Ca | Kết quả |
| --- | --- |
| ERP + đơn giá 5.000.000 + không GG | TRUE — tự duyệt ✅ |
| Có 1 dòng đơn giá = 1.000 (biên) | false ✅ |
| Dòng đó = 1.001 | TRUE ✅ |
| Biến 1 dòng thành hàng tạm | false ✅ |
| Bật GG mặt hàng 50.000 | false ✅ |
| Báo giá rỗng / dòng chưa có giá | false ✅ |

**FE — luồng thật trên BG-2026-00240:** `lowPriceItems` bắt đúng 1 dòng 500đ · popup hiện đúng tiêu đề, số lượng, bảng Mã/Tên/Đơn giá · dòng vi phạm nền cam `rgb(255,237,213)` · "Quay lại" đóng popup giữ nguyên màn và giữ nền cam · "Tiếp tục gửi duyệt" sang popup phê duyệt, ra **Cấp 3** (đúng TH2 vì có dòng ≤ 1.000).

## Test lại đầy đủ trên nhánh `tpe-develop-assign` (2026-08-18)

| AC | Kết quả |
| --- | --- |
| AC1 | Báo giá sạch (2 dòng ERP 3tr + 5tr, không GG): **không** popup cảnh báo · popup ghi "Tự động duyệt" · bấm Xác nhận duyệt → status 1 → **4 Đã duyệt**, level=1, approved_by=13, lịch sử `self_approve` 1→4 ✅ |
| AC2 | 1 dòng 500đ → popup đúng nội dung, dòng vi phạm nền cam `rgb(255,237,213)`; nút `primary-warning` + `ri-send-plane-line` ✅ |
| AC3 | "Quay lại" → đóng popup, ở nguyên màn, dòng vẫn nền cam ✅ |
| AC4 | "Tiếp tục gửi duyệt" → sang popup phê duyệt ✅ |
| AC5 | Có GG tổng 200.000 → không tự duyệt, ra Cấp 3, Xác nhận gửi → status 1 → **2 Chờ TP duyệt**, lịch sử `submit` ✅ |

ERP sync sau khi tự duyệt fail mềm ("Khách hàng ERP chưa có địa chỉ giao hàng") → ghi
`erp_sync_status = failed`, không tạo bản ghi bên ERP. Dữ liệu test đã khôi phục nguyên trạng.

### Checkpoint — 2026-08-17
Vừa hoàn thành: BE + FE #10797, rà lại theo `button-convention` / `modal-popup`, test BE 6 ca + FE hết AC2/AC3/AC4.
Đang làm dở: không.
Bước tiếp theo: chưa test AC1 (báo giá sạch → tự duyệt) trên UI vì chưa có báo giá nào đủ điều kiện — cần 1 báo giá toàn hàng ERP có giá > 1.000.
Blocked:

## Test lại toàn diện (2026-09-14) — nhánh `tpe`/`tpe-develop-assign`, cổng 3005/8005, DB `hrm_prod_6_6`

Ảnh chụp: `anh-test-2026-09-14/`. BE 2 nhánh trùng nhau (`git diff` rỗng) nên kết quả áp cho cả hai.

### 4 tài khoản, 4 mức quyền

| TK | Vai trò | Quyền 1081 TP | 1082 BGĐ | 1092 Giá vốn |
| --- | --- | --- | --- | --- |
| sontv.da (1845) | NVKD phòng Dự án | – | – | – |
| Luyentq.kd1 (428) | NVKD phòng 42 | – | – | – |
| hieudd.da (148) | TP **quản lý phòng 55** | ✓ | – | – |
| tuannd.kd1 (24) | TP **quản lý phòng 42** | ✓ | – | – |
| cob@ (36) | BGĐ công ty 1 | – | ✓ | ✓ |

### A. Luồng AC theo Redmine

| AC | Ca | Kết quả |
| --- | --- | --- |
| AC1 | BG-2026-00182 sạch (1 hàng ERP, 75tr) | Không popup cảnh báo · popup ghi **"Tự động duyệt"** · nút **"Xác nhận duyệt"** · status 1→**4**, level=1, `approved_by=428` (chính NVKD), `tp_approved_by=NULL`, lịch sử `self_approve`, **`erp_sync_status=success`** ✅ |
| AC2 | BG-2026-00202 có 3 dòng ≤1.000 | Popup đúng tiêu đề, đúng số "**3 mặt hàng**", bảng Mã/Tên/Đơn giá khớp SQL · 3 dòng nền cam `rgb(255,237,213)`, dòng thường trong suốt ✅ |
| AC3 | Bấm "Quay lại" | Popup đóng, ở nguyên màn edit, 3 dòng **vẫn** nền cam ✅ |
| AC4 | Bấm "Tiếp tục gửi duyệt" | Sang popup phê duyệt, ra **Cấp 3** + sơ đồ 2 bước ✅ |
| AC5 | Luồng phân cấp đầy đủ | 1→2 (`submit`, actor 1845) → TP duyệt 2→3 (`tp_approve_forward`, actor 148) → BGĐ duyệt 3→4 (`bgd_approve`, actor 36) ✅ |
| – | Từ chối | Bỏ trống lý do → chặn "Vui lòng nhập lý do từ chối"; nhập rồi xác nhận → 2→**1**, lưu `rejected_reason`, level reset NULL, lịch sử `reject` ✅ |

### B. 11 ca biên `isAutoApprovable()` (qua API `calculate-level`)

| # | Ca | auto_approve | Cấp |
| --- | --- | --- | --- |
| 1 | 1 hàng ERP, 75.000.000, không GG | **true** | 1 |
| 2 | Đơn giá = **1.000** (biên dưới) | false | 3 |
| 3 | Đơn giá = **1.001** | **true** | 1 |
| 4 | Giá 75tr nhưng `erp_product_id=NULL` (hàng tạm) | false | 3 |
| 5 | Hàng ERP + **GG theo mặt hàng** (`discount_method=1`) | false | 1 |
| 6 | Hàng ERP + **GG tổng đơn** (`discount_method=2` + `quotation_discounts`) | false | 1 |
| 7 | Thêm **dịch vụ tạm** (`cost_id=NULL`) giá 5tr | false | 1 |
| 8 | Dịch vụ ERP nhưng đơn giá **800** | false | 1 |
| 9 | Hàng ERP + dịch vụ ERP đều > 1.000 | **true** | 1 |
| 10 | Báo giá **rỗng** | false | 3 |
| 11 | Cha 75tr (ERP) + **dòng con giá 0** (ERP) | false | 1 |

Ca 11 xác nhận quyết định đã chốt 2026-08-17: dòng con giá 0 **cố ý** chặn auto-approve. Hệ quả cần nhớ: mọi báo giá dùng combo có dòng con để giá 0 sẽ không bao giờ tự duyệt.
Ca 5/6/7/8/11 cho thấy `auto_approve=false` **không** đồng nghĩa phải qua TP — cấp vẫn có thể là 1 (NVKD tự duyệt) khi giá trị/tỷ suất thuộc cấp 1. Đúng spec TH2 ("theo luồng phân cấp hiện hành").

### C. Phân quyền

| Ca | Kết quả |
| --- | --- |
| NVKD mở `/quotations/pending-approval` | Bị đá về **404** ✅ |
| NVKD: popup gửi duyệt | **Ẩn** "Tổng giá nhập" + "Tỷ suất LN" (không có quyền 1092) ✅ |
| NVKD gọi thẳng API báo giá đang chờ duyệt | `submit` **422**, `self-approve` **422**, `tp-approve` **403**, `bgd-approve` **403** ✅ |
| NVKD mở màn sửa báo giá đang chờ duyệt | Chỉ còn nút "Quay lại", mọi ô nhập `disabled` ✅ |
| TP **không** quản lý phòng của báo giá (Tuân ↔ phòng 55) | Hàng đợi **rỗng** — đúng lọc `department_id ∈ getManagedDepartmentIds()` ✅ |
| TP **đúng** phòng (Hiếu ↔ phòng 55) | Thấy BG-2026-00202 badge "Cấp 3" ✅ |
| Sau khi TP chuyển BGĐ | Báo giá **rời** hàng đợi TP (6→5 mục) ✅ |
| TP gọi lại `tp-approve` | **422** "không ở trạng thái Chờ TP duyệt"; `bgd-approve` **403** ✅ |

### D. Lỗi UI phát hiện (KHÔNG thuộc #10797, chưa sửa)

1. `pages/assign/quotations/_id/index.vue:139,190` (và :135) dùng `.text-muted` → hiện **chữ ĐỎ** ("Bảng giá: Bán lẻ", "Không có", dòng tỷ giá) vì theme `custom-assign.scss` ép `color:#dc3545!important`. Trái quy tắc "đỏ chỉ dành cho lỗi validate" → đổi sang `#6b7280`.
2. Cùng file, dòng **1266 / 1448 / 1467** dùng `$bvModal.msgBoxConfirm()` cho Xoá / TP duyệt / BGĐ duyệt — CLAUDE.md cấm, phải chuyển sang `this.$confirm({...})` (`base-confirm-modal`). Biểu hiện: popup không có icon tròn header, nút "Huỷ" là text trần, không đúng khuôn nút chuẩn.
3. Màn danh sách chờ duyệt: cột "Dự án TKT" render bằng font monospace, lệch với các cột còn lại.

ERP sync: AC5 (BG-2026-00202) `failed` — "Không tìm thấy khách hàng ERP: code=29TPHXTR-66" (khách chưa có trong DB `dev_erp` local, lỗi môi trường). AC1 (BG-2026-00182) `success`.

**Dữ liệu đã khôi phục nguyên trạng**: BG-2026-00182 + BG-2026-00202 về `status=1`, level NULL, không `rejected_reason`, đủ 1/62 dòng hàng, lịch sử về đúng 1 bản ghi gốc; mật khẩu 5 tài khoản test trả lại hash cũ.

### Checkpoint — 2026-09-14
Vừa hoàn thành: test lại toàn bộ #10797 — 6 AC + 11 ca biên + 8 ca phân quyền trên 5 tài khoản. Không có lỗi thuộc phạm vi #10797.
Đang làm dở: không.
Bước tiếp theo: chờ user quyết 3 lỗi UI mục D (đều nằm ngoài #10797).
Blocked:
