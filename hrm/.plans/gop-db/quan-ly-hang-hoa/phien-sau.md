# Bàn giao phiên sau — Chuyển đổi hàng hoá (ghi 13/10/2026)

> Đọc file này + mục "ĐIỂM DỪNG 13/10" đầu `SO-CHOT-VA-TON.md` trước khi làm tiếp. Checklist tổng: `viec-con-lai.md`.

## 0. Trạng thái code (đã push hết, cây sạch)

| Repo | Nhánh | Commit trên origin |
|---|---|---|
| hrm-api | `feat/chuyen-doi-hang-hoa` | `5d109a505` (+ C-b N32, ĐÃ PUSH 13/10) |
| hrm-client | `feat/chuyen-doi-hang-hoa` | `dc793189e` |
| ERP | `feat/2d1-erp-khong-loi` | origin `43c8a09fbf` (kéo gop_db 13/10) · `3432ca97ac` = + đợt C-a (ĐÃ PUSH 13/10) · `3f017e66dd` = + C-a2 · **`42bbe92ae2` = + C-b + N81 (ĐÃ PUSH 13/10)** |

- Worktree: HRM `websites/wt-chuyen-doi-hang-hoa/{hrm-api,hrm-client}` (đang ở nhánh chung), ERP `websites/wt-erp-2d1`. `.env` cả 2 trỏ DB **`hrm_erp_giacty`**.
- Server dev đang chạy: API 8031 (`php@7.4 artisan serve`), Nuxt 3031 (node 12, heap 8192). Muốn tắt thì kill đúng PID theo cổng.
- e2e: Phase 6 + hàng hoá ở `wt-chuyen-doi-hang-hoa/e2e`; Phase 7 ở `ERP-HRM/HRM/e2e` (cả 2 ngoài git). Lệnh: `BASE_URL=http://127.0.0.1:3031 API_BASE=http://127.0.0.1:8031 API_REPO=<wt>/hrm-api PATH=node20 npx playwright test <spec> --project=chromium|api --no-deps --workers=1 --reporter=line` (spec `*.api.spec.ts` dùng `--project=api`).
- Bảng quyền mốc: `roles` 129 · `role_has_permissions` 18.418 · `employee_has_roles` 1.720 (kiểm sau mọi lần cấp role tạm).

## 1. Việc tiếp theo (theo thứ tự đề xuất)

0. 🔜 **13/10 wrap up 6**: C-a + C-a2 + C-b (+N81) ĐÃ PUSH; **C-d plan `ngoai-luong/cd-plan.md` + mockup `mockup-doi-xe.html` chờ user duyệt + "làm"** (hỏi chạy e2e); thứ tự sau: C-c (kèm đo lại bố cục chi tiết hàng hoá sau N51) · C-e (N1) · C-f · A7. Ghi riêng làm sau: N64 (lịch sử tài chính), N80 (YC xuất hàng lộ tài chính HĐ).
1. ✅ 13/10: **soát xong + chốt đủ 16 câu** ⇒ `ngoai-luong/soat-bang-c.md` (6 đợt C-a…C-f, thêm N76; đóng N31/N66/N64, bỏ N47/N48). TIẾP: viết plan đợt C-a ⇒ xin "làm". ~~**Việc ngoài luồng — `viec-con-lai.md` bảng C** (~38 mục ⬜). User chốt 12/10: **sửa HẾT trước khi update prod**, kể cả lỗi cũ ERP có sẵn trên gop_db. Đề xuất: soát lại từng mục (mục nào đã tự hết do 2-D/G6/T7/P6 chặn route) ⇒ chia đợt ⇒ plan ⇒ xin "làm". Mục nặng/nhạy: N1 (bảo hành/tồn tối thiểu theo công ty ở ERP), **N61 `getData` lộ giá vốn** (bảo mật), N64 route catalog-histories không gate, N27 khoá dòng lấy về/khoá.~~
2. ✅ **A7 — user chốt 13/10: cả 4 phase THUỘC lần lên prod này** (cần mở lần lượt) — user 13/10: **để làm SAU**, làm bảng C trước. ~~chốt phạm vi~~: Phase 2c (3 danh mục xe còn lại) · 3 (phân quyền theo công ty) · 4 (popup tìm hàng dùng chung) · 5 (gỡ 5 danh mục) có thuộc lần lên prod này không — hỏi user.
3. **2-E**: Excel hàng hoá + nghiệm thu "ERP không vỡ" 14 bước (`hop-dong-tuong-thich-erp.md`).
4. **A5 bỏ hệ số giá**: N34 (2 cron giá + 3 màn xem giá ERP ⇒ HRM), N36 (Cập nhật giá theo hãng) — user để "sau".
5. **A8**: 5 ca e2e "không quyền" đỏ sẵn do spec chèn `roles.company_id` (cột không còn trên DB gộp): take.api A5, lifecycle.api A6, take-ui N1, read.api "1. Gate quyền" (tài khoản nocost), write.api E14 — cần 1 đợt sửa spec riêng.

## 2. Điều kiện CHẶN go-live (nghiệp vụ / dữ liệu)

| # | Việc | Ghi chú |
|---|---|---|
| B6 | **Nhập cây phân loại hàng hoá** (Tính chất · Nhóm chức năng · Nhóm SP · Loại SP) | đo 12/10: Loại SP 0 ⇒ HRM không tạo được hàng hoá nào (thường lẫn tạm) |
| B5 | **Nhập danh mục Đặc tính** | 0 dòng; hàng tạm bắt buộc Đặc tính (A12) |
| B1 | Tick cờ `product_natures.is_auto_parts` cho Tính chất phụ tùng ô tô | N10 |
| B2 | Công ty 5/6/8 sẽ loại bỏ: tắt cờ duyệt hàng mới Cty 8, mốc tắt tài khoản | N69/N70 |
| B4 | Dọn 30 phiếu hỏi giá chéo công ty còn dở ở ERP (phải = 0 trước deploy) | runbook phần 2 mục 8 |
| — | Dọn 1 hàng tạm ERP đang chờ duyệt (`tmp_products.status=2`) | runbook phần 3 |
| — | Gán quyền 1656/1657/1658/1662/1663/1664 cho vai trò nghiệp vụ; PTKD duyệt hàng tạm bằng 1662 | runbook |

Runbook triển khai: `gia-theo-cong-ty/runbook-trien-khai.md` (Phần 1 giá theo công ty · Phần 2 luồng tính giá · Phần 3 hàng tạm).

## 3. Đang treo — cần user cho phép

- Migration mới kéo từ gop_db: `2026_10_12_000000_change_exchange_rate_decimal_addition_accounting_requests` (tỉ giá phiếu đề nghị kế toán, không thuộc feature) — **chưa chạy** trên `hrm_erp_giacty` lẫn `hrm_erp`. Chỉ cần nếu thử màn đó trên dev.

## 4. Điểm nhỏ Phase 6 đã hoãn (review toàn nhánh xếp "để sau được")

Đã sửa trong lượt sửa cuối (không còn tồn): spec e2e màn Hàng tạm · test payload đồng bộ HĐ · ô ghi chú phiếu YC hàng tạm ERP · comment `TmpProductSyncService` (QuotationService :2308, :2548).

Còn tồn:
- Khoá / đồng thời: deadlock tiềm ẩn `detachFromOldRequests` (phiếu→nhóm) vs `PriceCalculateFinalizer` (nhóm→phiếu); `lockForXnk` vs Finalizer ngược thứ tự từ trước Phase 6; race hẹp đọc phiếu cũ trước khi khoá.
- `Product::editableAt` xét pcc công ty đang xem, `assertNotTemp` xét pcc công ty chủ — nên dùng chung 1 nguồn.
- Câu `MSG_GROUP_KEY` (viết cho PTKD) nay cũng hiện cho người lập ở popup sửa — cân nhắc câu riêng.
- `QuotationService.php:2557` comment "pullStatus…" luồng cũ; `ProductProjectController :233-238, :691` nhánh `erp_tmp_product_id` cũ; dấu `}` lệch thụt lề `ProspectiveProjectQuotationsTab` (watch projectId).
- `priceCompanyOf` / `pricingCompanyId` (QuotationService :5161, :5204) fallback công ty người đăng nhập ≠ khái niệm "công ty báo giá" của cổng C3.
- Tab Tái sử dụng tải `per_page=1000` lọc client (>1000 dòng thiếu im lặng); route `assign/product-projects` không gate quyền (có sẵn).
- `useReuseRow` để trống ĐVT nếu danh sách ĐVT chưa tải xong.
- Màn Hàng tạm: `openRequests()` parse 3 lần/dòng; `group_concat` giới hạn 1024 byte cần comment.
- Lý do không duyệt tra theo tiền tố mã hàng trong `note` log (bảng log không có product_id).
- Hàng tạm thiếu Thương hiệu/Hãng không sửa được ở form duyệt (hiếm — reader YCHG join cứng brands/manufactures).
- ERP: 2 link menu "Duyệt hàng tạm (HRM)" / "Hàng tạm chờ duyệt (HRM)" cùng URL; import thừa `HomeController`.
- Test: `SET FOREIGN_KEY_CHECKS` không bọc try/finally (TempProductApiTest); `actingAsSameUser` dễ vỡ; fixture `ProspectiveProjectVisibleIdsTest` created_by = nhân viên đầu tiên; 2 endpoint CustomerCare chưa test gọi thật; FQCN inline (ServiceService :61, DeviceErrorController :34).
- Luật xem dự án TKT có 2 bản (`ProspectiveProject::visibleIdsQuery` chép `ProspectiveProjectService::index`) — có test đối chiếu; muốn gom 1 chỗ phải sửa hàm dùng chung ⇒ hỏi user.

## 5. Quyết định user đã chốt trong phiên (để không hỏi lại)

- Hàng tạm = hàng hoá thật, trạng thái theo công ty 6 Hàng tạm / 7 Đã duyệt / 8 Không duyệt; không bảng riêng, không migration.
- Lập hàng tạm trong YCHG (dùng lại popup BOM/Báo giá); ai cũng tạo được; Phân loại bắt buộc đủ 5 ô (kể cả Đặc tính); Tiểu mục KHÔNG bắt buộc.
- PTKD duyệt từng hàng (form như form tạo hàng hoá + tab Quản trị), **đổi được Đồng ý ↔ Không duyệt tới khi Duyệt phiếu** (có ⓘ giải thích 6 nút); duyệt phiếu khoá khi còn hàng 6.
- **Không đổi Thương hiệu/Hãng khi phiếu Chờ PTKD** (sai hãng ⇒ Không duyệt hàng ⇒ sale sửa ⇒ YCHG khác).
- Xoá mềm hàng tạm đã từng vào YCHG; nhóm đóng ⇒ hàng về 1; lập HĐ ERP chỉ khi mọi hàng Đang kinh doanh; câu banner "Còn N hàng hoá chưa sẵn sàng kinh doanh (hàng tạm chưa tính giá xong / chưa lấy về)".
- Form hàng hoá THƯỜNG cũng sẽ bắt buộc Đặc tính — tạm bỏ vì dữ liệu cũ chưa có (A11).
- ERP: định kỳ merge một chiều `origin/gop_db` ⇒ nhánh chung (không bao giờ ngược lại); đề xuất làm đầu mỗi đợt ERP.
- Dev local: được cấp role tạm để chạy e2e / kiểm UI (gỡ khi xong). e2e chỉ chạy khi user bảo.
