# Design Phase 7 — Luồng tính giá 4 chứng từ (HRM) — ✅ USER DUYỆT 11/10/2026

> Viết 11/10/2026. Nguồn chốt: `ton.md` (Q1–Q20, D1–D13) · mockup đã DUYỆT `mockup-luong-tinh-gia.html` + `mockup-ghi-chu.md` ·
> khảo sát `khao-sat-be-erp.md`, `khao-sat-fe-erp.md`, `khao-sat-hrm.md`, `khao-sat-csdl-chan-erp.md`.
> Tiền đề: feature lên production MỘT lần (không cờ / đường lui) · giá RIÊNG theo công ty (G0–G6 xong) · code ở worktree
> `wt-chuyen-doi-hang-hoa` (nhánh chung `feat/chuyen-doi-hang-hoa`) + ERP `wt-erp-2d1` (`feat/2d1-erp-khong-loi`), DB dev `hrm_erp_giacty`.
> ⛔ Tài liệu này KHÔNG phải lệnh code — mỗi đợt phải xin "làm" riêng kèm phạm vi.

---

## 1. Mô hình

```
YCHG (1 công ty) ──gom nhóm Thương hiệu–Hãng──► nhóm 1..n ──(mỗi nhóm 1)──► YCTG ──1–1──► PTG ──giá áp──► KQ (bản chụp)
   lập: ai cũng được          PTKD duyệt CẢ phiếu     XNK phụ trách hãng      KTMH duyệt/trả   KTMH tính giá     drill trong YCHG/YCTG
```

- Cả luồng thuộc **công ty phiếu** = công ty đang làm việc của người lập (Q4). Giá áp cho đúng công ty đó, không đụng công ty khác.
- MỌI hàng qua YCHG: hàng **Đang nhập thông tin** (đổi trạng thái theo §2.3) và hàng **Đang kinh doanh** (hỏi lại giá, giữ trạng thái) (Q1a, Q15).
- Phân vai như ERP (Q2): XNK nhập giá NCC / tiền tệ / tỉ giá / thuế NK / chi phí ở YCTG · KTMH duyệt (= bấm Tính giá) hoặc trả YCTG · KTMH lập PTG kế thừa YCTG, nhập hệ số / giá bán, Lưu & duyệt.
- PTKD duyệt cả phiếu theo quyền, mọi phiếu trong công ty, không xét phân công (Q19).
- XNK của nhóm = **phân công hiện hành** `assign_histories` (`employee_date_to IS NULL`, `buy_employee_id`) theo (thương hiệu × hãng × công ty phiếu) (D3) — chỉ cho nhóm chưa có YCTG; YCTG đã lập thuộc người lập (đổi người qua Bàn giao công việc). Nhóm chưa có phân công ⇒ **chặn gửi** (Q3).
- Mọi ĐVT: YCHG chọn hàng, YCTG/PTG tự bung đủ ĐVT đã khai (Q9).
- Duyệt giá theo quy chế công ty như G5 (Q5), **theo từng dòng** (D5).
- Kết quả: không có màn riêng; drill giá bán mới dưới mã hàng trong YCHG / dòng trong YCTG + chế độ "Chi tiết kết quả" (Q20). Vẫn ghi `price_calculate_results*` làm bản chụp + bản in.

## 2. Trạng thái

### 2.1 Mã chứng từ (thêm mã MỚI, không đè mã cũ ERP)

| Chứng từ | Mã | Nhãn | Ghi chú |
|---|---|---|---|
| YCHG (phần đầu) | 3 · 2 · 8 | Đang tạo · Chờ PTKD duyệt · Không duyệt | giữ |
| | **10** | **Đang hỏi giá** | mới — PTKD đã duyệt, còn nhóm chưa đóng. Phiếu cũ mã 1/5/7 hiện "Đang hỏi giá" (lọc `IN (1,5,7,10)`) |
| | 4 | Đã tính giá | mọi nhóm đóng, ≥ 1 nhóm có giá |
| | 9 | Không có giá | mọi nhóm đóng, không nhóm nào có giá |
| | 6 | Huỷ duyệt | chỉ phiếu cũ |
| Nhóm (`price_asking_request_groups.status`) | NULL · 5 · 1 · 7 · 4 · 9 · 6 | chưa tới XNK · Chờ XNK duyệt · Chờ lập YCTG · Đang tính giá · Đã tính giá · Không có giá · Huỷ duyệt | trùng số mã YCHG cũ cùng nghĩa ⇒ backfill chép mã; 9/6 là nhóm **đóng** (không gửi lại — D7) |
| YCTG | 3 · 2 | Đang tạo · Chờ tính giá | giữ |
| | **5** | **Không duyệt** | mới — KTMH trả, XNK sửa gửi lại |
| | 1 | Đang tính giá | giữ mã, đổi nhãn (đã có PTG) |
| | **6** | **Chờ duyệt giá** | mới |
| | 4 | Đã tính giá | giữ |
| PTG | 3 · 1 | Đang tạo · Đã duyệt | giữ |
| | **5** · **6** | **Chờ duyệt giá** · **Giá bị từ chối** | mới |
| Dòng PTG `approval_status` | NULL · 1 · 2 · 3 | không qua duyệt · chờ · đã duyệt · bị từ chối | mới (D5) |

### 2.2 Chuyển trạng thái

```
YCHG: 3 ─gửi─► 2 ─PTKD duyệt─► 10 ─(mọi nhóm đóng)─► 4 | 9
          └─PTKD không duyệt─► 8 ─sửa, gửi lại─► 2
Nhóm: NULL ─PTKD duyệt─► 5 ─XNK duyệt─► 1 ─lập YCTG─► 7 ─giá áp─► 4
                           └─Không có giá─► 9        └─Huỷ duyệt─► 6   (chỉ khi chưa có YCTG)
YCTG: 3 ─gửi─► 2 ─KTMH Tính giá (PTG lưu)─► 1 ─PTG gửi duyệt─► 6 ─mọi dòng duyệt─► 4
          ▲       └─KTMH không duyệt─► 5 ─sửa, gửi lại─┘           (tắt quy chế: 1 ─► 4)
PTG:  3 ─Lưu & duyệt─► (tắt quy chế) 1  |  (bật) 5 ─mọi dòng duyệt─► 1
                                              └─có dòng từ chối─► 6 ─sửa dòng bị từ chối, gửi lại─► 5
```

### 2.3 Trạng thái hàng × công ty (`product_company_coefficients.status`)

Thêm **mã 5 Đang tính giá** (D4). Chỉ hàng MỚI đổi; hàng Đang kinh doanh giữ 3.

| Sự kiện | Hàng mới |
|---|---|
| Gửi YCHG | 1 ⇒ 2 Chờ tính giá bán |
| PTKD không duyệt / nhóm đóng không giá | 2·5 ⇒ 1 |
| PTG lưu (nháp) có dòng của hàng | 2 ⇒ 5 |
| Mọi ĐVT của hàng được áp giá | 2·5 ⇒ 3 Đang kinh doanh |

⚠️ Rà mọi chỗ đọc `pcc.status` để mã 5 được xử như 2: `ProductCompany::STATUS_*` + nhãn/màu (Đang tính giá `#2563EB`), bộ lọc 4 màn hàng hoá (2-C), popup lấy về, `assertTradingAt`, đếm menu/dashboard, cron ERP 14:30 + đọc ERP (2-D1). Kiểm bằng `grep -rn "status" ProductCompany` + test.

## 3. CSDL (migration HRM, khuôn G1: guard `hasTable/hasColumn`, cột mới NULL được, không đổi nghĩa / không xoá cột cũ)

### 3.1 Luồng chứng từ

| Bảng | Thay đổi |
|---|---|
| **`price_asking_request_groups`** (mới) | id · price_asking_request_id FK · company_id · brand_id · manufacture_id (chụp lúc lưu) · sort_order · xnk_employee_id (người XNK **lúc gửi**, chỉ để tra cứu — gate theo phân công hiện hành, D3) · status · xnk_note · xnk_approved_by/at · close_reason · closed_by/at · priced_at · audit. UNIQUE(price_asking_request_id, brand_id, manufacture_id); index (company_id, status) |
| `price_asking_requests` | phiếu mới: `brand_id/manufacture_id/send_company_id` = NULL; `company_id` = công ty đang làm việc; dùng `comment/approver_id/approved_time` cho PTKD; index (company_id, status) |
| `price_asking_request_products` | + `group_id` (FK, index); `unit_id`, `unit_name` ⇒ NULL được (NULL = mọi ĐVT) |
| `price_asking_request_approve_histories` | + `group_id` NULL (log theo nhóm); + index price_asking_request_id |
| `price_calculate_requests` | + `group_id` UNIQUE (1 nhóm – 1 YCTG); + rejected_by/at (lý do dùng `comment`) |
| `price_calculates` | UNIQUE(price_calculate_request_id) (1 YCTG – 1 PTG) |
| `price_calculate_products` | + chụp chính sách (Q13): policy_owner_company_id · policy_manufacture_id · policy_base_type · policy_percent_import_lot · policy_percent_stock · policy_owner_cost_price (chỉ trả khi có 1092) · policy_owner_prices json · policy_captured_at; + approval_status · approval_comment · approval_decided_at (D5). `note` đã có — ghi chú dòng, KHÔNG ghi đè `products.note` (Q10) |
| `price_calculate_results` | UNIQUE(price_calculate_id) |
| `product_approves` (G5) | + `price_calculate_id` NULL + index — G5 báo ngược PTG |
| `product_company_coefficients` | không đổi cột; thêm giá trị status 5 |

Kiểm trùng trước khi thêm UNIQUE (local đã 0 trùng; chạy lại SQL trên production trong runbook).

### 3.2 Chính sách giá bán nội bộ (T1, §28 + D13)

| Bảng | Cột |
|---|---|
| `internal_price_policies` (cha) | id · owner_company_id (công ty BÁN = công ty đang làm việc) · manufacture_id · base_type (1 giá vốn · 2 giá bán) · audit. UNIQUE(owner_company_id, manufacture_id) |
| `internal_price_policy_targets` (con) | id · policy_id FK · target_company_id · percent_import_lot · percent_stock (decimal(5,2), 0–100) · audit. UNIQUE(policy_id, target_company_id) |
| `internal_price_policy_settings` | owner_company_id UNIQUE · coefficient_mode (riêng theo công ty / chung) — tuỳ chọn toàn cục §28d-quater |

Lịch sử: khuôn entity-history (`catalog_histories` như §28a-6) — ghi cả "Xoá" kèm tỷ lệ cũ (D13c). Công ty chỉ thấy/sửa cấu hình của mình (chặn BE).

### 3.3 Backfill phiếu cũ (D2) — lệnh `price-asking:backfill-groups` (`--dry-run`, chạy lại ghi 0)

Theo `khao-sat-csdl-chan-erp.md` §2.8: 1 phiếu = 1 nhóm (hãng ở phần đầu; 20 phiếu thiếu hãng lấy theo dòng đầu; 4 phiếu hàng đổi hãng vẫn 1 nhóm) · status nhóm = mã đầu phiếu nếu ∈ {5,1,7,4,9,6} (6 phiếu st1 có YCTG nháp ⇒ 7) · gán `group_id` dòng hàng / YCTG / log · 21 YCTG bị KTMH trả ⇒ 3 → 5 · phần đầu phiếu cũ không ghi lại.
Lệnh `price-asking:close-stale --before=2026-06-01` (`--dry-run`): đóng phiếu dở trước mốc, lý do "Chuyển hệ thống". Nháp giữ nguyên.

## 4. Quyền (D9, type 8 Tài chính; seeder riêng idempotent, không chạy cả seeder chính, kiểm `uniq -d` + DB ngay trước merge)

| Id | Quyền | Gate |
|---|---|---|
| — | (không cần quyền) | lập / sửa / gửi / xoá YCHG của mình; xem YCHG + drill kết quả trong công ty |
| **1662** | PTKD duyệt yêu cầu hỏi giá | Duyệt / Không duyệt YCHG Chờ PTKD duyệt, mọi phiếu công ty phiếu |
| **1663** | XNK xử lý yêu cầu hỏi giá | (kèm là XNK phân công hiện hành của nhóm) XNK duyệt / Không có giá / Huỷ duyệt nhóm · lập / sửa / gửi YCTG |
| **1664** | Tính giá bán hàng hoá | Tính giá / Không duyệt YCTG · lập / sửa / Lưu & duyệt PTG |
| 1092 | Xem giá vốn hàng hoá | giá vốn công ty quản lý ở khối Chính sách / Tạm tính / cột chụp (Q12) |
| 1656 | Cấu hình chính sách giá bán nội bộ | vào + sửa màn Chính sách (seed cùng đợt T1) |
| — | Xem YCTG / PTG | có 1663 hoặc 1664 hoặc 1092 (Q11); không ⇒ ẩn menu, endpoint 403, số phiếu hiện chữ thường |

Mọi quyền xét **tại công ty phiếu** (`isCurrentEmployeeHasPermission` theo công ty phiếu). Super admin không bypass. Gate ở BE; FE chỉ ẩn nút.

## 5. Giá — tích hợp G4/G5 (refactor bắt buộc)

Hiện chỉ `ProductPriceUpdateService::update()` public, gắn công ty đang làm + chỉ hàng status 3; hàm ghi là private (`khao-sat-hrm.md` §1).

1. Tách lõi ghi giá thành service dùng chung: `ProductPriceWriter::apply(productId, unitId, companyId, resolvedPrices, meta)` — ghi `product_unit_prices` + `product_expected_prices` + `product_company_units.cost_price` (= giá nhập kho PTG) theo công ty truyền vào, không kiểm trạng thái hàng. G4 gọi lại (giữ nguyên hành vi G4 — chạy lại PHPUnit MasterData 332 ca + e2e giá).
2. PTG Lưu & duyệt:
   - Công ty tắt quy chế ⇒ `apply()` từng dòng ngay ⇒ §2.3 chuyển hàng ⇒ PTG 1, YCTG 4, nhóm 4 (`priced_at`), sinh KQ, cập nhật YCHG, thông báo.
   - Bật quy chế (`approvalRule/needsApproval`) ⇒ `ProductPriceApprovalSubmitter::submit()` từng (hàng × ĐVT) kèm `price_calculate_id` ⇒ dòng `approval_status = 1`, PTG 5, YCTG 6.
3. G5 `approve()/reject()` (sửa code G5): nếu `pa.price_calculate_id` ⇒ ghi `approval_status/comment/decided_at` lên dòng PTG **trước khi** xoá pa; dòng duyệt ⇒ áp giá dòng đó (đường áp của G5) + chuyển hàng khi đủ ĐVT; mọi dòng duyệt ⇒ PTG 1 → bước sau như tắt quy chế; có dòng từ chối (và không còn dòng chờ) ⇒ PTG 6, chỉ mở lại dòng bị từ chối (D5). Bổ sung nhánh G5 cho công ty KHÔNG quản lý hàng (hiện ghi "chốt ở Phase 7").
4. Chặn chéo (D6): G4 không lưu dòng có `pa` thuộc PTG đang chờ ("Giá đang chờ duyệt ở PTG-xxxx"); PTG không gửi duyệt dòng đang có `pa` của G4. Hàng chỉ nằm trong YCHG/PTG chưa gửi duyệt ⇒ G4 vẫn sửa.
5. Công thức (K12): giá nhập kho = giá NCC × tỉ giá × (1 + thuế NK%) + Σ chi phí (% tính trên đơn giá chưa thuế) + chi phí khác; giá bán theo `Calc` của `productPriceModel.js` (Q6). BE **tính lại** giá nhập kho và kiểm giá bán khi lưu (ERP chỉ lưu số FE gửi — không chép). Hệ số TMĐT đọc `configs.coefficient_ecommerce_price` của công ty phiếu, trả trong payload form.
6. Chụp chính sách (Q13) lúc lưu PTG; phiếu đã duyệt hiện số chụp.

## 6. BE (Laravel, module đề xuất `Modules/Sale` cho YCHG/YCTG, `Modules/Finance` cho PTG — chốt khi plan T2)

| Nhóm | Endpoint chính |
|---|---|
| Chính sách (T1) | list theo công ty bán · chọn hãng (1.071, kèm số mã hàng của công ty bán — D13b) · lưu theo hãng · xoá · xem trước · lịch sử · import/export Excel · tra chính sách cho (hàng, công ty mua) |
| YCHG (T3) | list (Đang tạo/Không duyệt chỉ người lập thấy) · show (nhóm + drill KQ) · nguồn chọn hàng (status 1 + 3 công ty phiếu, kèm XNK + cảnh báo đang hỏi giá) · store/update/delete · gửi (chặn nhóm chưa phân công) · PTKD duyệt/không duyệt · XNK duyệt / không có giá / huỷ duyệt nhóm · print-data |
| YCTG (T4) | list · show (+ drill) · nhóm chờ lập của tôi · tạo từ nhóm (bung mọi ĐVT, thuế NK mặc định `products.import_tax`, chi phí mặc định `manufactures.costs`) · update · gửi · KTMH không duyệt · danh mục chi phí type 8 / tiền tệ (`/finance/currencies/getAll`) · print-data |
| PTG (T5) | list · show · YCTG chờ tính giá · tạo từ YCTG · update · Lưu & duyệt · Tạm tính (gate 1092) · print-data |
| KQ | đọc qua show YCHG/YCTG (chỉ giá bán) · print-data |

Chỉ dùng connection mặc định (KHÔNG `mysql2` — worktree trỏ `erp2326`). Lỗi validate báo đồng thời mọi ô.

## 7. FE (hrm-client)

| Màn | Vị trí (D10, D13d) | URL đề xuất |
|---|---|---|
| Yêu cầu hỏi giá | phân hệ **Bán hàng** (gắn link mục 'YC hỏi giá' có sẵn `sale-hub.js:165`, giữ nhãn) | `/sale/price-asking-requests` |
| Yêu cầu tính giá | phân hệ **Bán hàng** | `/sale/price-calculate-requests` |
| Phiếu tính giá | phân hệ **Tài chính** (mục 'Phiếu tính giá' có sẵn `finance.js:444`) | `/finance/price-calculates` |
| Chính sách giá bán nội bộ | menu **Cấu hình** cuối sidebar phân hệ Bán hàng ⇒ trang cấu hình dạng hub, khuôn `pages/meeting/settings/index.vue` | `/sale/settings` (hub "Chính sách giá bán nội bộ") |

- Page hub phải khai layout đúng (memory topbar 2 cấp vs hub 3 cấp); tên file route không dùng `_ten-co-gach.vue`.
- Dùng `Calc` của `productPriceModel.js`; dựng bảng PTG mới (không nhúng `ProductPriceTable.vue`).
- Danh sách theo khuôn `pages/finance/product-prices` (nhớ 2 lỗi bộ lọc âm thầm). Form: unsaved-changes mixin, validate đồng thời, V2Base*.
- Drill KQ + chế độ "Chi tiết kết quả" đúng mockup (bảng mini, sticky trong YCTG).
- Nút Lập yêu cầu hỏi giá ở màn Hàng hoá nhập thông tin + Hàng đang kinh doanh; màn Dữ liệu công ty: "Tiến độ tính giá".

## 8. Thông báo (D8, khuôn `ProductPriceNotifier`, gửi sau commit, chỉ trong công ty phiếu — Q16)

| Mốc | Người nhận | Nội dung |
|---|---|---|
| Gửi YCHG | có 1662 tại công ty | `[YCHG] Chờ duyệt: PYCHG-xxxxx. Người lập: …` |
| PTKD duyệt | XNK phân công từng nhóm | `[YCHG] Chờ XNK duyệt: PYCHG-xxxxx. Nhóm: Launch.` |
| PTKD không duyệt / XNK không có giá / huỷ duyệt | người lập | `[YCHG] Không duyệt: … Lý do: …` |
| Gửi YCTG | có 1664 tại công ty | `[YCTG] Chờ tính giá: YCTG-xxxxx.` |
| KTMH không duyệt | XNK lập YCTG | `[YCTG] Không duyệt: … Lý do: …` |
| Giá áp (từng nhóm) | người lập YCHG + XNK | `[YCHG] Đã có giá: PYCHG-xxxxx. Nhóm: Launch.` (link về nhóm, bật Chi tiết kết quả) |
| Đủ nhóm | người lập YCHG | `[YCHG] Đã tính giá: PYCHG-xxxxx.` |
| Giá bị từ chối (G5) | người lập PTG | `[PTG] Giá bị từ chối: PTG-xxxxx. Lý do: …` |

Tên ≤ 50, câu ≤ 120 ký tự (skill notification-convention).

## 9. Bản in (Q17) — popup `ReportPrintPreviewModal` + endpoint `print-data`

YCHG (mẫu 98) · YCTG (mẫu 99) dùng `report_templates` sẵn có; PTG + KQ dựng blade `prints/_layout` (không thêm dòng `report_templates`). Letterhead theo công ty phiếu. Theo skill print-page.

## 10. ERP (chặn — đợt T7)

- Mở rộng middleware `ProductMovedToHrm` (G6): đích HRM theo loại phiếu; gắn **41 route** 4 nhóm + `product.getDataForPriceAsking`, **giữ tên route**. Link KQ cũ ⇒ tra YCHG chứa nó.
- `topmenubar` 5 link (dòng 327, 931, 1534, 1536, 2383) trỏ HRM như G6. **Bỏ 3 thẻ dashboard** (D12).
- Gỡ `PriceCalculate.*` khỏi danh sách miễn audit `ProductWriteAuditObserver`. Cron `product:update_price` 01:00 giữ, không sửa.
- `Product::checkPriceAsked()` chỉ gọi từ route bị chặn — để nguyên.

## 11. Runbook bổ sung (vào `gia-theo-cong-ty/runbook-trien-khai.md`)

1. Trước 7 ngày: báo nghiệp vụ dọn phiếu dở; SQL kiểm **30 phiếu chéo công ty** còn 0 (D1) — chưa 0 thì không deploy.
2. Kiểm trùng trước UNIQUE (§3.1). 3. migrate. 4. seed quyền 1656/1662–1664. 5. `price-asking:backfill-groups --dry-run` ⇒ chạy thật ⇒ chạy lại ghi 0.
6. `price-asking:close-stale --before=2026-06-01`. 7. Deploy ERP chặn cùng lần. 8. Gán quyền mới cho vai trò (nghiệp vụ).
9. Nhắc: công ty 2/5/6/7/8 chưa có phân công XNK ⇒ không gửi được YCHG tới khi khai.

## 12. Các đợt

| Đợt | Phạm vi | Repo | DB | Xong khi |
|---|---|---|---|---|
| **T1** | Chính sách giá bán nội bộ: 3 bảng + API + trang `/sale/settings` (hub) + menu Cấu hình + lịch sử + import/export + quyền 1656 | api + client | migration + seed 1656 vào giacty | PHPUnit + Playwright màn; e2e có/không quyền |
| **T2** | Nền CSDL luồng: migration §3.1 + `pcc.status=5` (rà §2.3) + seeder 1662–1664 + model/entity + lệnh backfill/close-stale (dry-run) | api (+client nhãn trạng thái 5) | migration + seed giacty; backfill chạy thật trên giacty | PHPUnit MasterData xanh; dry-run khớp §3.3 |
| **T3** | YCHG: BE + 2 màn (list, form/show) + nút ở màn hàng hoá + thông báo | api + client | — | luồng gửi/duyệt/đóng nhóm; Playwright đo DOM; e2e |
| **T4** | YCTG: BE + 2 màn + KTMH duyệt/trả + drill (đọc KQ) | api + client | — | như trên |
| **T5** | PTG + refactor ghi giá G4/G5 (§5) + KQ + drill + G5 báo ngược | api + client | `product_approves.price_calculate_id` | PHPUnit giá (332 + mới), e2e G4/G5 chạy lại xanh |
| **T6** | Bản in 4 chứng từ | api + client | — | in thử 4 mẫu, đo bản in |
| **T7** | Chặn ERP + nghiệm thu tổng + chạy thử runbook trên bản sao tạm rồi DROP | ERP + api | bản sao tạm | checklist §10, §11 |

Thứ tự: T1 → T2 → T3 → T4 → T5 → T6 → T7. Mỗi đợt nhánh con từ nhánh chung, merge LOCAL về nhánh chung, push khi user cho.

## 13. Rủi ro / để ý

| # | Rủi ro | Xử lý |
|---|---|---|
| R1 | Refactor lõi ghi giá G4/G5 đã nghiệm thu | T5 chạy lại 332 PHPUnit + e2e giá; giữ chữ ký `update()` |
| R2 | pa bị xoá cứng ⇒ PTG mất dấu | ghi kết quả lên dòng PTG trước khi xoá (§5.3) |
| R3 | Mã 5 `pcc.status` sót chỗ đọc ⇒ hàng "biến mất" khỏi màn | rà grep + test 4 màn hàng hoá + ERP 2-D1 |
| R4 | Công ty không có phân công XNK ⇒ không dùng được luồng | runbook nhắc khai; thông báo lỗi nêu rõ hãng |
| R5 | id quyền bị nhánh khác chiếm | kiểm `uniq -d` + DB ngay trước merge (memory) |
| R6 | `mysql2` trỏ DB khác ở worktree | chỉ dùng connection mặc định |
| R7 | UNIQUE trên production lỗi do dữ liệu trùng | SQL kiểm trong runbook |

Ngoài luồng ghi nhận (không vá trong Phase 7): các lỗi ERP cũ ở `ton.md` §1 — tự hết khi ERP chặn 4 chứng từ.
