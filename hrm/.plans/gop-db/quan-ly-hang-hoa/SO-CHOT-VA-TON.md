# Sổ chốt & tồn — feature Quản lý hàng hoá

> 🔄 **23/10/2026: BỎ tính bắt buộc của K1/§29a-1** ("mọi hàng phải qua 4 chứng từ tính giá") — thêm thao tác "Chuyển kinh doanh không tính giá" (giá 0 ⇒ Đang KD) cho mọi hàng ở màn Nhập thông tin. Chốt Q1–Q8 + Đ2: `chuyen-kd-khong-tinh-gia/`. ĐÃ CODE 23/10, commit 24/10 (api `17f76d1f9`, client `3940e0c1b`, chưa push).
> 🔄 **24/10/2026: BỎ nguyên tắc không hỏi giá chéo công ty** — kế thừa giá từ công ty quản lý theo hãng (màn *Giá bán theo hãng sx*, đồng bộ 6 giá + ĐMGG + giá hiệu lực, YCHG hàng kế thừa tách sang công ty quản lý). Chốt Q1–Q13: `ke-thua-gia-theo-hang/` — mockup + plan duyệt, ĐÃ CODE 24/10 (2 migration chạy local, 1 quyền chèn local), CHƯA commit.

> 🔒 **22/10/2026: màn Hàng hoá đang khoá ĐÃ CODE + PUSH gop_db** (api `7f6ae6e4d`, client `aea4d8983`, ERP `710d383568`) — `hang-hoa-dang-khoa/` (design + plan + `progress.md` ledger); 3 repo gop_db (hrm-api · hrm-client · ERP); PHPUnit MasterData 644 (2 đỏ sẵn), Playwright MCP đạt; e2e đã sửa 5 spec, CHƯA chạy (DB 21_10_prod không có tài khoản e2e).

> 📌 **BÀN GIAO PHIÊN SAU: `phien-sau.md`** (việc tiếp theo, điều kiện chặn go-live, việc treo, điểm nhỏ hoãn, quyết định đã chốt).
> 🧭 **ĐIỂM DỪNG 13/10/2026 (wrap up):** Phase 6 + Phase 7 xong & đã push. ERP nhánh chung đã kéo gop_db (`f941467a49`, push; migration gop_db `2026_10_12_000000_change_exchange_rate…` CHƯA chạy giacty/hrm_erp). **TIẾP:** bảng C đã soát + chốt 16 câu 13/10 (`ngoai-luong/soat-bang-c.md`, 6 đợt C-a…C-f) ⇒ plan + sửa từng đợt (user chốt sửa hết trước prod) · chặn go-live B5/B6 (nhập cây phân loại + Đặc tính) · ✅ A7: user chốt 13/10 phase **2c · 3 · 4 · 5 THUỘC lần lên prod này** (chưa mở phase nào) — **để làm sau**, trước mắt soát + sửa bảng C.
> ✅ **13/10/2026: PHASE 6 Hàng tạm XONG + ĐÃ PUSH** (api `657fa731f`, client `dc793189e`, ERP `396f42dd7c`) — hàng tạm = hàng thật status 6/7/8, lập trong YCHG, PTKD duyệt từng hàng; ERP chặn. Sổ `danh-muc-hang-tam/p6-so-thuc-hien.md`.
> ✅ **12/10/2026: PHASE 7 Tính giá XONG (local)** — T7 ERP merge LOCAL `443c812553` chưa push; runbook Phần 2 chạy thử đạt.
> 📋 **12/10/2026: danh sách VIỆC CÒN LẠI gom 1 chỗ ⇒ `viec-con-lai.md`** (phase còn mở + việc ngoài luồng N1–N75 đã soát trạng thái).
> **File này là ĐẦU MỐI để quay lại làm tiếp.** Mở nó trước, rồi mới mở `design.md` / `plan.md`
> của phase cần làm.
> Cập nhật lần cuối: **11/10/2026 — Phase 7: P2 + T2 nền CSDL xong (local)** · trước đó: **10/10/2026 — mở Phase 7 Tính giá: chốt Q1–Q18, T0 mockup DUYỆT, T1 xong (local) 11/10 — tiếp T2** · trước đó: **10/10/2026 — đợt GIÁ THEO CÔNG TY G0–G6 xong + push** · trước đó: **04/10/2026 (wrap up) — cổng chặn đóng (§35a–§35h); Phase 2d cây catalog XONG (e2e 6/6, chưa push); TIẾP: màn hàng hoá chia 5 đợt (mục 2c) — user chưa chọn đợt đầu, đề xuất 2-A** · Phụ trách: @namdangit
> ⚠️ 04/10: 10 commit Phase 2 lỡ làm (hrm-api) **CHƯA lên `gop_db`** (cả local + origin); nhưng **4 migration đã chạy vào DB local `hrm_erp`** (batch 410–414) — `can_retail` đã bị drop trong khi code `gop_db` vẫn đọc/ghi cột này. User chốt **để nguyên** (04/10), xử lý cùng câu E1.
> 🌿 **NHÁNH CHUNG (04/10/2026): `feat/chuyen-doi-hang-hoa`** (cả 2 repo, đã push) — tạo từ `origin/gop_db` (api 706635ece / client 1ad497c05) + đã merge P2d (api 3bb89bc51 / client ca47614e6). Mỗi đợt mở nhánh con **từ nhánh chung**, xong thì merge về nhánh chung; ⛔ không merge vào `gop_db`.
> 🗂️ **WORKTREE (07/10/2026): `websites/wt-chuyen-doi-hang-hoa/{hrm-api,hrm-client}`** — làm MỌI việc của feature ở đây (checkout chính `ERP-HRM/HRM/*` đang ở `gop_db` cho session khác). Hiện checkout **`feat/chuyen-doi-hang-hoa`** (2-C3 đã merge + push 07/10: api `626113419` / client `e046aff2c`; e2e 13/13 — checkpoint `2c-ghi/plan.md`). Server worktree: api **8031**, Nuxt **3031**; e2e chạy bằng bản sao `wt-chuyen-doi-hang-hoa/e2e`. vendor/node_modules là bản sao `cp -c` (không symlink); `.env` → DB `hrm_erp`.
> Nhánh cũ: `feat/p1-danh-muc-hang-hoa` (cả 2 repo) — api +29 commit, client +28 commit **chưa merge**
> về `gop_db`.

---

## 1. Tiền đề không bao giờ được quên

| # | Tiền đề | Nguồn |
|---|---|---|
| 1 | **Chuyển NỀN CODE, không đổi CSDL.** Đọc/ghi thẳng bảng ERP, giữ nguyên `id`, không di trú. Mọi thay đổi schema là NGOẠI LỆ, phải nêu riêng và chờ duyệt | `quan-ly-hang-hoa/design.md` mục "Tiền đề" |
| 2 | **Bám ERP đang chạy, KHÔNG bám mockup.** Thứ tự ưu tiên: spec đã chốt → ERP đang chạy → mockup. Lệch thì DỪNG, báo user quyết | §17 |
| 3 | **Chốt spec + mockup TRƯỚC, không động source dự án** cho tới khi user yêu cầu. Mockup không tính là source | §22 |
| 4 | Không `mysql2`/`DB_CONNECTION_SECOND`; bảng trùng tên ưu tiên bản ERP | `.plans/gop-db/design.md` |
| 5 | **Không bảo mật thông tin hàng hoá và giá bán** — quyền chỉ kiểm soát ai được THAO TÁC dữ liệu và ai được xem GIÁ VỐN | user chốt 04/10/2026, `design.md` §35b |
| 7 | **Tuyệt đối KHÔNG merge code nào vào `gop_db`** — `gop_db` đang là nhánh production; xong việc chỉ push nhánh feature | user chốt 04/10/2026 |
| 9 | **Vấn đề phát sinh NGOÀI luồng hàng hoá: note lại, xử lý tại chức năng đó sau; fix HẾT rồi mới merge vào nhánh prod** (danh sách: `2c-ghi/chot.md` mục *Việc ngoài luồng*) | user chốt 04/10/2026 |
| 8 | **Hệ số giá (`product_company_coefficients.coefficient`) sẽ KHÔNG dùng nữa** sau khi xong toàn bộ luồng chuyển đổi hàng hoá — bỏ hẳn cách công ty khác lấy giá công ty tạo × hệ số (làm tròn) ra giá bán của mình; **mỗi công ty tự xây giá riêng, tham khảo Cấu hình chính sách giá bán nội bộ (§28)**. ⇒ hệ quả "sinh dòng coef 1 làm tròn nghìn ở popup ERP" (G4, G6) chỉ là tạm thời | user chốt 04/10/2026, nhắc lại 08/10/2026 |
| 6 | **Mọi việc implement vào source phải hỏi user và nhận "làm" rõ ràng** — chốt tồn / duyệt plan / "làm X trước" KHÔNG phải lệnh code | user chốt 04/10/2026, CLAUDE.md gốc ERP-HRM |

---

## 2. Trạng thái các phase

| Phase | Nội dung | Trạng thái |
|---|---|---|
| 0 | 6 danh mục phân loại (cây 4 cấp + 2 phẳng) | 🟢 xong (@junfoke, #11421) |
| 1 | 11 danh mục liên quan | 🟢 code xong, **chờ nghiệm thu** |
| **2** | **Quy trình xây dựng hàng hoá: các màn theo trạng thái + form** | ✅ **MOCKUP ĐÃ CHỐT 30/09** (§34) |
| **2-tg** | **Yêu cầu tính giá + Phiếu tính giá** | ✅ **ĐÃ CHỐT 30/09** — quan hệ **1 – n** theo nhóm Thương hiệu – Hãng SX (§33p), gom nhóm + người tiếp nhận (§33o) |
| **2-lv** | **Cây 4 cấp** trong tab *Quản trị hàng hoá* | ✅ **ĐÃ CHỐT 30/09** — chọn bằng **4 cột kiểu ERP** (§33v); 2 cấp đổi tên **Mục / Tiểu mục** (§33w); data cũ bỏ hết, 11 vấn đề ở §30e |
| **2-cat** | **Xây dựng catalog kinh doanh**: 2 màn kho + popup xếp hàng vào Tiểu mục | ✅ **ĐÃ CHỐT 30/09** — §33 (13 vòng góp ý); ⚠️ **đảo 2 điểm của §30f/§30g**: nhiều nhánh + bắt buộc đủ 4 cấp; **8 tồn** ở §33i chưa chốt |
| **2d** | **Cây catalog kinh doanh** (Chương · Mục · Tiểu mục) — `chuyen-cay-catalog/` | 🟢 **code xong 04/10, chờ nghiệm thu** — nhánh `feat/p2d-cay-catalog` (api 7 commit, client 3 commit, **đã push nhánh 04/10; ⛔ KHÔNG merge vào gop_db (nhánh production)**; review cuối đã sửa 4 lỗi); quyền **1670–1675**; e2e 6/6 passed. ✅ **13/10: thêm Import Excel 3 màn** (api `5389ada7b`, client `096a2af8e`; PHPUnit 20/20, Playwright MCP đạt) + **user cho MERGE + PUSH vào `gop_db`** (api `5f3a78f60`, client `40f6be80f`) + push nhánh. ✅ Đã merge vào nhánh chung `feat/chuyen-doi-hang-hoa` LOCAL 13/10 (api `65cb94491` — xung đột JobClusterService: giữ cả 2 trait; client `881d3b404`); PHPUnit MasterData 459/459 trên giacty, Playwright MCP 3 màn đạt (validate, không ghi DB) — CHƯA push. Ca e2e "không quyền → 403" của `business-catalog-tree.api.spec.ts` sẽ đỏ vì `user-nocost` đã được cấp đủ 6 quyền catalog (không do code) |
| **2-bc** | **Báo cáo hàng hoá theo công ty** (ma trận mã × công ty) | ⏸ **ĐỂ SAU** (04/10) — ra khỏi Phase 2; mockup riêng §27, chưa nối vào mockup luồng |
| **2-cf** | **Chính sách giá bán nội bộ** — lưới hãng × công ty mua, nhập tại chỗ | ✅ **MOCKUP ĐÃ CHỐT 30/09** — §28 |
| 2b | 6 danh mục Xe | 🟢 code xong, **chờ nghiệm thu** |
| 2c | 3 danh mục xe còn lại (biển số · lái xe ngoài · danh mục xe) | ⬜ chưa mở |
| 3 | Phân quyền hàng hoá theo công ty | ⬜ chưa mở |
| 4 | Popup tìm kiếm hàng hoá dùng chung | ⬜ chưa mở |
| 5 | Gỡ 5 danh mục — ⚠️ với `groups` **chỉ gỡ MÀN, GIỮ BẢNG** | ⬜ chưa mở |
| 6 | Danh mục hàng tạm — `danh-muc-hang-tam/` | 🔎 **MỞ 12/10** (user "mở để làm luôn"): khảo sát xong; brainstorm ⇒ **phương án mới** `danh-muc-hang-tam/design.md` (hàng tạm = hàng thật status 6, gộp duyệt vào YCHG, tái dùng popup BOM/Báo giá) — spec + **mockup DUYỆT 12/10** (duyệt từng hàng tạm Đồng ý/Không duyệt, status 6/7/8, form duyệt có tab Quản trị, Phân loại bắt buộc đủ 5 ô) ⇒ plan `danh-muc-hang-tam/p6-plan.md` (9 task) ⇒ **user cho "LÀM" 12/10** (nhánh `feat/p6-hang-tam` 2 repo HRM + `feat/p6-chan-hang-tam` ERP, không migration/seeder/quyền mới). 🔴 10/10: chuyển hết sang HRM trong lần cập nhật này |
| 7 | Luồng Tính giá — `luong-tinh-gia/` | 🔎 **MỞ 10/10**: khảo sát BE/FE ERP xong; user chốt Q1–Q18 (`luong-tinh-gia/ton.md`) — **giữ đủ 4 chứng từ** YCHG→YCTG→PTG→KQ, YCHG gom nhóm hãng (1 YCHG–n YCTG, 1 YCTG–1 PTG), vai như ERP (XNK lập YCTG, KTMH duyệt + lập PTG), cả luồng trong 1 công ty, duyệt giá qua G5, 3 quyền mới, in cả 4, dùng lại 15 bảng. T0 mockup ✅ **USER DUYỆT 11/10** (`luong-tinh-gia/mockup-luong-tinh-gia.html` + `mockup-ghi-chu.md`; thêm Q19 PTKD duyệt theo quyền mọi phiếu công ty, Q20 kết quả hiện trong YCHG/YCTG dạng drill + chế độ "Chi tiết kết quả"; 6 điểm tự chốt còn hiệu lực duyệt cùng mockup). Chốt thêm D1–D13 (`luong-tinh-gia/ton.md` §4). **Design ✅ 11/10** `luong-tinh-gia/design.md` (7 đợt T1 Chính sách → T2 nền CSDL → T3 YCHG → T4 YCTG → T5 PTG + refactor ghi giá G4/G5 → T6 in → T7 chặn ERP). **Design user DUYỆT 11/10.** P1: hãng đã lưu dùng Khoá (xoá mềm). Plan T1 ✅. **T1 ✅ XONG 11/10** (user cho "làm"): 3 bảng + quyền 1656 chạy giacty, API + trang `/sale/internal-price-policies` (menu Bán hàng › Quy chế - Thiết lập › Quy chế kinh doanh — user đổi 11/10, bỏ hub Cấu hình), PHPUnit MasterData 358/358, Playwright BE thật đạt có/không quyền; merge LOCAL api `d50ccd8b5`, client `0450fc8f7` — chưa push; e2e 8/8 passed (11/10). ✅ **P2 XONG 11/10** (≥ 1 công ty mua; merge LOCAL api `6b7388ebb`, client `8dbd35ec1`). ✅ **T2 XONG 11/10** (`luong-tinh-gia/t2-plan.md`; module MasterData — T2-Q1; hàng 2/5 ở màn Nhập thông tin — T2-Q2): 9 migration + backfill 4.029 nhóm trên giacty, quyền 1662–1664, mã 5 (vá lỗ G4 sửa giá hàng mã 5), PHPUnit 372/372; merge LOCAL api `ee6928c96`, client `fd7a87d4d` — chưa push. close-stale CHẠY THẬT giacty 45 nhóm (user duyệt T2-C1 + phần đầu phiếu 4/6). TIẾP: user đánh giá close-stale (log created_by = 0) → plan T3 (YCHG); push chờ user báo; role tạm T1_UAT_NAMDANG giữ |
| **8** | **Quản lý giá hàng hoá** + bảng giá theo công ty | 🔴 **KÉO LÊN 09/10** — thành nội dung chính, làm trước màn giá 2-D2 |

---

## 2c. 🔜 MÀN HÀNG HOÁ — CHIA 5 ĐỢT (đề xuất 04/10/2026; user chọn **2-A làm đầu** 04/10)

Mỗi đợt: khảo sát → plan riêng ở `quan-ly-hang-hoa/<thư-mục-đợt>/` → nêu phạm vi (repo · nhánh · file/bảng · DB)
→ user nói "làm" mới code (CLAUDE.md gốc). Phạm vi đã trừ: tính giá, chính sách giá nội bộ, báo cáo (để phase sau).

| Đợt | Nội dung | Rủi ro |
|---|---|---|
| **2-A Nền CSDL** *(đề xuất làm trước)* | `product_company_coefficients` + `status` + UNIQUE(product_id, company_id) + 4 cột quản trị (A1, §24) · `product_suppliers` + `company_id` · bảng `product_business_catalogs` (A6) · backfill 45.890 hàng cũ → dòng trạng thái cho công ty tạo (A3) | 🔴 ghi hàng loạt vào bảng ERP; phải đo trùng cặp hàng × công ty + hàng mồ côi TRƯỚC |
| **2-B Đọc** | API + FE 4 màn: Kho dữ liệu · Dữ liệu hàng hoá công ty · Hàng hoá nhập thông tin · Hàng đang kinh doanh (không bắt buộc catalog, C5) + form chỉ xem | thấp |
| **2-C Ghi** | tạo/sửa 6 tab, 3 mức quyền §26c-bis · sinh mã (§16) · lấy về · xoá (B4) · nút tạm "Chuyển kinh doanh" (H1) · popup Xây dựng catalog (bắt buộc ≥1 nhánh, C5-a) · quyền 1652–1655 | trung bình |
| **2-D ERP không lỗi** | chặn route ghi hàng hoá ERP (QĐ13) · null-safe `->group->` (SearchController 11 chỗ, popup 338 màn) — `man-danh-muc-hang-hoa/sua-erp-de-khong-loi.md` | 🔴 bắt buộc trước production |
| **2-E** | Excel (Catalog chỉ ghi Tiểu mục, D1-a) + nghiệm thu "ERP không vỡ" 14 bước (`hop-dong-tuong-thich-erp.md`) | — |

🔎 **2-A khảo sát (04/10): `2a-nen-csdl/khao-sat.md`** — 🔴 phát hiện A1 xung đột với cách ERP đọc `product_company_coefficients` (có dòng = nhân hệ số giá; ERP lưu hàng/lưu hãng xoá sạch dòng) ⇒ user chốt (04/10) GIỮ A1, hệ số giá gỡ ở phase sau, 2-A chỉ thêm cột — KHÔNG backfill. 📋 Plan `2a-nen-csdl/plan.md` — ✅ XONG 04/10 — commit `15610ea2a`, đã vào nhánh chung `feat/chuyen-doi-hang-hoa` (đã push), 3 migration đã chạy vào `hrm_erp`, PHPUnit 5/5, giá popup 231/231 không đổi.

🔎 **2-B khảo sát + plan (04/10): `2b-doc/`** — chốt Q1 suy ra trạng thái lúc đọc · Q2 ẩn hoàn toàn giá · Q3 thêm 2 cột phân loại ở 2-B · Q4 seed 1652/1653. ✅ XONG 04/10 — đã vào nhánh chung (api `40d3e9028`, client `e9d46129b`), PHPUnit 8/8, e2e 4/4 + 6/6.

🔎 **2-C (04/10): `2c-ghi/`** — chốt G1–G11 (`chot.md`) + danh sách *việc ngoài luồng* N1–N8; plan 4 đợt con 2-C3 → 2-C1 → 2-C2 → 2-C4. **2-C3 Catalog ✅ XONG 07/10 — đã merge nhánh chung + push, e2e 13/13 (ca không quyền đã làm chặt). TIẾP: 2-C1.** 2-C1 ✅ XONG 08/10 — đã merge nhánh chung (api 35c4aa971, client 81f38f36d), e2e 32 xanh + 1 skip; đã push 08/10. Trước go-live: N10 tick cờ Phụ tùng ô tô. **2-C2 (08/10): khảo sát `2c-ghi/c2-khao-sat-be.md` + `c2-khao-sat-fe.md`, user chốt L1–L7 (`chot.md`, `c2-ton.md`) — Plan `c2-plan.md`; user cho "làm" → nhánh `feat/p2c2-lay-ve` (api `2739d0379` PHPUnit 127/127, client `3a9eae100`), Playwright MCP đạt; e2e take.api 7/7 + take-ui 10/10 + read-ui 8/8 (chạy worktree cần `API_REPO`); DB đã dọn. ✅ Đã merge nhánh chung LOCAL 08/10 (api `d3c6496a1`, client `5c2cfb823`) — CHƯA push (user chọn). TIẾP: push khi user cho phép.** **2-C4 (08/10): khảo sát `c4-khao-sat-be.md` + `c4-khao-sat-fe.md`, user chốt V1–V9 (`chot.md`, `c4-ton.md`) — V9 đổi: KHÔNG xoá S3. Code xong trên `feat/p2c4-vong-doi` (api `006d0585f` PHPUnit 147/147, client `9ca80b35a`); Playwright đo D1–D11+N1 đạt; e2e lifecycle.api 6/6 · lifecycle-ui 10/10 · form-ui 17+1skip · read-ui 8/8; DB đã dọn. CHƯA merge nhánh chung. Cột "Hành động" rỗng khi không quyền 1652 đã sửa (client `2bf90d755`, lifecycle-ui 10/10, read-ui 8/8). ✅ Đã merge nhánh chung LOCAL 09/10 (api `488269eed`, client `07e829014`) — CHƯA push (cùng 2-C2). **Đợt 2-C XONG** (C1·C2·C3·C4). TIẾP: push khi user cho phép; đợt kế: 2-D (ERP không lỗi — bắt buộc trước production) hoặc 2-E.** **2-D (09/10): khảo sát `2d-erp-khong-loi/khao-sat-a-chan-ghi.md` + `khao-sat-b-doc.md`; user chốt đủ tồn `2d-erp-khong-loi/ton.md` Q1–Q14 (09/10) — đổi ⭐: bỏ menu HH ERP, **màn giá HRM làm trong 2-D**, chặn CRUD Hãng SX/Thương hiệu ở ERP, mẫu tem theo Loại SP (thêm cột), N5 để sau, N6 bỏ; ERP code ở nhánh mới từ `gop_db`, kiểm `hrm_erp`. Khảo sát luồng giá `khao-sat-c-gia.md`; user chốt QC-0…QC-10 ⇒ **tách 2-D1** (điều kiện production) / **2-D2** (màn giá HRM + port Duyệt giá, không chặn go-live; Cập nhật giá theo hãng khoá ERP ở 2-D1, port để sau — N36). Plan `2d-erp-khong-loi/d1-plan.md` + user chốt T1–T6 (09/10). P1 HRM ✅ 09/10 trên `feat/p2d1-mau-tem` (api `f73d733d0`, client `612f9735e`; migration mẫu tem đã chạy hrm_erp) — chưa merge. P2 ERP ✅ code 09/10 (worktree `wt-erp-2d1`, nhánh `feat/2d1-erp-khong-loi`, 6 commit) — chưa merge/push; hrm_erp đã chạy 22 migration chờ. P3 kiểm ✅ 09/10 (`2d-erp-khong-loi/d1-kiem-p3.md`: K1–K3, K5, K6, K9–K17, K19 đạt; K4/K7/K18 một phần; K8 vướng lỗi cũ N47/N48; dữ liệu test đã dọn, mốc khớp). Lỗi cũ N41–N51, điểm 2-D1 N52/N53. N52/N53 đã sửa (ERP `b2f1761789`). ✅ HRM merge nhánh chung LOCAL 09/10 (api `a862fbeef`, client `9b05f7b42`) — CHƯA push (cùng 2-C2/2-C4). ERP giữ nhánh `feat/2d1-erp-khong-loi` (worktree `wt-erp-2d1`). ✅ **PUSH 09/10**: HRM nhánh chung (api `a862fbeef`, client `9b05f7b42`) + ERP `origin/feat/2d1-erp-khong-loi` (upstream đổi khỏi gop_db). TIẾP: khảo sát + plan 2-D2 (màn giá HRM + port Duyệt giá) — thư mục `2d-erp-khong-loi/`. 🔴 **09/10 user ĐẢO QC-2: bảng giá RIÊNG theo công ty (Hướng B, A4/A5) là nội dung chính, làm TRƯỚC; màn Cập nhật giá + Duyệt giá dựng trên logic giá mới** (`2d-erp-khong-loi/d2-ton.md`). Khảo sát `gia-theo-cong-ty/khao-sat-erp.md` + `khao-sat-du-lieu-hrm.md`; user chốt P1–P14 (`gia-theo-cong-ty/ton.md`, 09/10). 🔴 **Feature lên production MỘT LẦN khi xong hết các phase** (không thiết kế giai đoạn tạm). D1–D12 màn giá đã chốt đủ (`2d-erp-khong-loi/d2-ton.md`; menu ở phân hệ **Tài chính**; làm mockup trước). Design `gia-theo-cong-ty/design.md` ✅ 09/10 (chốt đủ T1–T8; T5: chạy thẳng `hrm_erp` chung); 7 đợt con G0 mockup · G1 nền CSDL + backfill · G2 HRM đọc giá · G3 ERP đọc giá · G4 màn Cập nhật giá · G5 Duyệt giá · G6 chặn ERP + nghiệm thu. G0 mockup `gia-theo-cong-ty/mockup-gia.html` ✅ dựng xong 09/10 (Playwright đạt; Q1/Q2 đã chốt). ✅ user chốt mockup 09/10. **G1 user cho "làm" 09/10** — phạm vi: hrm-api nhánh `feat/gia-cty-g1-nen`; M1–M3 + model + lệnh backfill/compare + PHPUnit; CHỈ chạy M1+M2 vào hrm_erp (sao lưu trước); backfill thật + M3 hỏi riêng khi G2/G3 xong; gỡ @TODO-BACKFILL dời G2. Checkpoint `gia-theo-cong-ty/g1-plan.md`. ✅ **G1 XONG 10/10** — api `36dd43546`, M1/M2 chạy hrm_erp (batch 430/431, sao lưu trước), dry-run khớp §3.4, PHPUnit mới 10/10; đã merge nhánh chung LOCAL (`c87221dc6`), chưa push. User chốt: FK pcu vào `ProductUsageGuard` sửa ở G2; **sửa fixture PHPUnit hàng hoá (roles.company_id không có trên DB gộp, 116/256 ca đỏ sẵn) TRƯỚC G2** — chưa có "làm". ✅ **Sửa fixture 10/10** (api `e39d67520`, merge LOCAL `98afafb05`): MasterData 256 ca còn 1 đỏ có chủ đích (FK pcu ⇒ G2). Nguyên nhân: migration `2026_09_25_000002` gỡ `roles.company_id` (batch 429) + fixture Regulation dùng id ảo + test cũ hơn registry. Ngoài luồng: `[fix-fk]` 09/10 dựng lại hỏng 10 FK trên hrm_erp local (devices, distribution_rules, salary…). **G2 user cho "làm" 10/10** — hrm-api nhánh `feat/gia-cty-g2-doc-hrm`: lớp đọc giá + 20 file/37 điểm + đường ghi hàng hoá + FK pcu + cờ `PRICE_PER_COMPANY` (mặc định tắt; bật ⇒ đọc theo công ty + gỡ CASE @TODO-BACKFILL); không migration/seeder/backfill; merge LOCAL. Checkpoint `gia-theo-cong-ty/g2-plan.md`. ✅ **G2 XONG 10/10** — 5 commit (`347501f32`…`890dc9da6`), merge LOCAL `1409a38e7` (nhánh chung +10 commit chưa push). PHPUnit MasterData 280/280 xanh; Assign/Finance/Human đỏ sẵn không đổi. Lệch: cờ tắt chỉ ghi giá công ty chủ + lệnh mới `product-price:complete-sets` (runbook: migrate → backfill → complete-sets → compare → M3 → bật cờ). Tồn Q-G2-1…4, N71–N75 (`g2-plan.md`). 🔴 **10/10 user BỎ CỜ** (không feature flag — feature chỉ chạy local tới khi xong hết) ⇒ **G2b** (cho "làm"): gỡ cờ, giá luôn theo công ty, gỡ hẳn @TODO-BACKFILL, N71 + N72 (backfill chép 4 ô quản trị). Sau G2b: tạo DB bản sao **`hrm_erp_giacty`**, trỏ 2 worktree sang, chạy backfill + compare + M3 (user cho). Chưa push. ✅ **G2b XONG** (merge LOCAL `61d1b215d`). ✅ **DB `hrm_erp_giacty`** (bản sao hrm_erp 10/10, 1.869 bảng) — 2 worktree `.env` trỏ sang (bản cũ `.env.bak-hrm_erp`); backfill thật 1.042.374 dòng = dry-run, compare **0 lệch**, chạy lại ghi 0; **M3 lỗi MySQL 1832** ⇒ sửa gỡ/gắn FK (api `742eea2b4`, merge `d23479b8c`), up→down→up đạt. PHPUnit MasterData trên giacty: 31 đỏ (fixture viết cho DB trước backfill) ⇒ ✅ sửa fixture (api `627f16f3a`, merge LOCAL `98a59deff`): MasterData 280/280 trên giacty; code không lỗi. **G3 user cho "làm" 10/10**: ERP `wt-erp-2d1` nhánh `feat/gia-cty-erp` từ `feat/2d1-erp-khong-loi`; R1–R8 + `ProductPriceService` + cron 14:30 + snapshot; đường ghi cũ (PTG ⇒ công ty quản lý hàng, hàng tạm ⇒ công ty hàng tạm) sửa tối thiểu cho có company_id; không migration, không push. Checkpoint `gia-theo-cong-ty/g3-plan.md`. ✅ **G3 code xong 10/10** — 8 commit / 132 file (`fe334ef9f4`…`30540fe9d7`), PHPUnit 56 (chỉ ExampleTest đỏ sẵn), snapshot chỉ lệch nhóm chấp nhận, Playwright popup × 4 công ty đạt. User chốt: W5/W6/W7 (Cập nhật giá nhanh ERP) chặn ở G6 — tới lúc đó KHÔNG dùng màn này trên giacty; chấp nhận lệch R3/R4; cho kiểm P8 UI trên giacty (xoá/trả 1 dòng pcu); merge LOCAL vào `feat/2d1-erp-khong-loi`. ✅ P8 UI đạt (toast chặn, HĐ 27684 không đổi, dòng pcu 11184 trả đủ 21 cột, role tạm gỡ); ERP merge LOCAL `5b3cdd032c`, chưa push. **G4 user cho "làm" 10/10**: hrm-api + hrm-client nhánh `feat/gia-cty-g4-cap-nhat`; màn Cập nhật giá bán theo mockup + lịch sử + menu Finance; quyền 1657 chèn riêng vào hrm_erp_giacty (không chạy cả seeder); merge LOCAL. Checkpoint `gia-theo-cong-ty/g4-plan.md`. ✅ **G4 XONG 10/10** — api `218f80436`+`494837d87` merge `8b2c96aea`; client `dcccb38a7` merge `2454cd867` (chưa push: api +20, client +2). MasterData 310/310 trên giacty; Playwright 1440/1280 đạt. DB giacty: quyền 1657 + role tạm 105473 cho e2e_assign. User chốt 10/10: quyền 1657 (và 1658) thuộc **type 8 Tài chính** (đổi ở G5); chấp nhận lệch G4 (423 tới G5, đủ 6 loại giá, Lưu xoá ghi chú không duyệt, lọc duyệt ~2,5s ⇒ cần index ở đợt có migration); e2e `product-prices-ui.spec.ts` chạy SAU G5 cùng spec duyệt; giữ role tạm 105473 tới hết G6. **G5 user cho "làm" 10/10**: nhánh `feat/gia-cty-g5-duyet` 2 repo; gửi duyệt + màn Duyệt + Excel + thông báo [GIA] + quyền 1658 + D4; quyền 1657/1658 type 8; bật tạm cờ duyệt 1 công ty trên giacty rồi trả; chạy e2e 2 spec giá cuối đợt; merge LOCAL. Checkpoint `gia-theo-cong-ty/g5-plan.md`. ✅ **G5 XONG 10/10** — api merge `1952c2ee0`, client `1bef3ce9d` (chưa push); MasterData 332/332 giacty; e2e duyệt 8/8 + G4 6/6. User 10/10: **Tính giá (Phase 7) + hàng tạm (Phase 6) cũng chuyển hết sang HRM trong lần cập nhật này** ⇒ điểm lệch 1–2 G5 (xử lý riêng pa do PTG/hàng tạm ERP sinh) **gỡ trong G6**; giữ điểm 3–9. **G6 user cho "làm" 10/10**: ERP `feat/gia-cty-g6-chan` (chặn W5/Duyệt giá/manualUpdatePrices/W6/W7, menu/dashboard/link sang HRM; KHÔNG chặn PTG/hàng tạm tới Phase 7/6) + HRM `feat/gia-cty-g6` (gỡ điểm 1–2 G5) + nghiệm thu tổng trên giacty (compare, snapshot, PHPUnit, e2e) + chạy thử runbook trên bản sao tạm `hrm_erp_runbook` rồi DROP; runbook `gia-theo-cong-ty/runbook-trien-khai.md`. Checkpoint `g6-plan.md`. ✅ **G6 XONG 10/10** — ERP merge `027fb570a2` (10 route chặn), api `0feda6059`, client `06ec3a1e1` (đều LOCAL, chưa push: ERP +11, api +25, client +6). Nghiệm thu giacty: compare 0 lệch, snapshot chỉ nhóm chấp nhận, PHPUnit ERP 62 (1 đỏ sẵn) / MasterData 332, e2e giá 6/6 + 8/8, read 8/8, form 17+1skip; đỏ sẵn 4 ca (roles.company_id trong spec, nocost, E14); **5 ca "lấy về" đỏ do backfill** (mất tiền điều kiện hàng sạch). Runbook chạy thử đạt (kỹ thuật ~2 phút). ✅ Tồn G6 xử lý 10/10: 5 ca e2e "lấy về" viết lại fixture (`createProductOfCompany`, xanh); menu/thẻ dashboard ERP đo DOM đạt (role tạm 105600 đã gỡ); seeder riêng `ProductPricePermissionSeeder` (api `5b327e085`, merge `b282d0829`) — chỉ chèn 1657/1658 type 8, idempotent; observer giữ. Còn: 5 ca e2e "không quyền" đỏ sẵn do spec chèn `roles.company_id` (cần đợt riêng); cache quyền ERP không xoá được (redis). **ĐỢT GIÁ THEO CÔNG TY G0–G6 XONG (local, chưa push: ERP +11, api +27, client +6).** ✅ **PUSH 10/10**: ERP `origin/feat/2d1-erp-khong-loi` @ `027fb570a2`, hrm-api `origin/feat/chuyen-doi-hang-hoa` @ `b282d0829`, hrm-client @ `06ec3a1e1`. User dừng phiên 10/10. **TIẾP (phiên sau): chọn đợt kế — Phase 7 Tính giá (đề xuất) / Phase 6 hàng tạm / sửa 5 ca e2e "không quyền".** Môi trường dev: 2 worktree `.env` trỏ `hrm_erp_giacty` (bản cũ `.env.bak-hrm_erp`).**

Code cũ lỡ làm (nhánh `feat/p1-danh-muc-hang-hoa`, E1): KHÔNG merge, chỉ tra cứu khi mở nhánh mới từ gop_db.

## 2a. ✅ MOCKUP ĐÃ CHỐT — 30/09/2026

Giai đoạn mockup của Phase 2 **kết thúc**. Bản chốt: `man-danh-muc-hang-hoa/mockup-luong-xay-dung-hang-hoa.html`
(448 KB — **11 màn + 13 popup**) và `mockup-bao-cao-hang-hoa.html` (69 KB). Console **0 lỗi** cả hai.
Danh mục màn + bảng nghiệm thu: **`man-danh-muc-hang-hoa/design.md` §34**.

Từ đây **không sửa giao diện nữa** — muốn đổi thì mở vòng mới và ghi rõ, để bản chốt này làm mốc
đối chiếu khi code.

~~`man-danh-muc-hang-hoa/mockup-hang-hoa.html`~~ **đã xoá 04/10/2026**. (Ghi chú cũ: bản 21/09 **đã lỗi thời**: có tab *Giá bán*
(đã gỡ ở §29g), form một tầng tab (đã đổi ở §30g), chưa có gì của §33.)

## 2b. 🚧 CỔNG CHẶN TRƯỚC KHI CODE (user chốt 23/09/2026)

> **Không mở bất kỳ phần code nào khi bảng tồn dưới đây còn câu chưa trả lời.**
> Quy trình: mockup được duyệt → Claude đưa **đủ** danh sách tồn ra hỏi → user trả lời hết →
> ghi đáp án vào `design.md` + sổ này → **rồi mới** viết migration / BE / FE.
> Lý do: mỗi tồn ở đây đều đổi **cấu trúc dữ liệu** (bảng chủ trạng thái, chép hay tham chiếu,
> tầng giá) — code trước rồi sửa sau là phải đập đi làm lại, chưa kể 171 bảng FK trỏ vào `products`.

📋 **DANH SÁCH HỎI CHỐT (bản chính, 30/09/2026): `man-danh-muc-hang-hoa/ton-chot-truoc-code.md`** — 22 câu nhóm A–E + 6 câu đã suy ra đáp án chỉ cần xác nhận + 2 câu phụ. Trả lời vào cột *Chốt* của file đó — hoặc bản Excel cùng nội dung `ton-chot-truoc-code.xlsx` (cột CHỐT nền vàng).

**Danh sách đầy đủ nay là 26 câu** = mục 3 dưới đây (6 câu) + `man-danh-muc-hang-hoa/design.md`
§26g (8 câu) + **§29f (4 câu)** + **§33i (8 câu — mới 29/09/2026)**.

⚠️ **§33 (29/09) đã ĐẢO 2 điểm đã chốt ngày 28/09** — ai đọc §30f/§30g phải đọc tiếp §33b:
catalog của (hàng hoá × công ty) nay là **NHIỀU nhánh** và **bắt buộc đủ 4 cấp tới Cụm công việc**;
chỗ lưu chuyển từ *4 cột trên `product_company_coefficients`* sang **bảng nối**
`product_id × company_id × job_cluster_id` (tên bảng chưa chốt — tồn §33i-1).

## 3. 🔴 ĐANG CHẶN — phải trả lời mới đi tiếp được

> **Cập nhật 23/09/2026 — user đưa "Logic xây dựng hàng hoá" (§26).** Cách làm đã đổi:
> **dựng MOCKUP trước**, các câu chặn dưới đây **tạm gác**, xong mockup mới quay lại giải quyết
> từng cái. Riêng §3.1 coi như **đã có đáp án** (xem ngay dưới).
>
> ✅ **§3.1 có đáp án:** §26e ghi rõ phạm vi theo công ty gồm *"Giá bán, giá vốn"* ⇒ **giá vốn
> NẰM TRONG** ⇒ đi Phương án 1 (tách tầng giá khỏi `product_units`). Còn chờ user xác nhận **một
> câu** trước khi viết migration.
>
> 🟡 **8 tồn MỚI từ §26** (chi tiết `man-danh-muc-hang-hoa/design.md` §26g):
> (1) trùng "luồng hỏi giá" của ERP? · (2) trạng thái theo công ty lưu bảng nào ·
> (3) quyền màn "Danh mục hàng hoá kinh doanh" · (4) "chưa dùng" xét theo công ty đăng nhập ·
> (5) lấy hàng công ty khác = chép hay tham chiếu · (6) sửa thông tin chung có ảnh hưởng công ty
> gốc *(đã trả lời một nửa ở §26c-bis: công ty đi mượn KHÔNG sửa được lớp chung)* ·
> (7) quay lui trạng thái · (8) 45.890 hàng hoá cũ gán trạng thái nào.

### 3.1. Câu quyết định cả đợt migration (§25d)

> **"Bảng giá độc lập theo công ty" có gồm GIÁ VỐN / GIÁ MUA NGOÀI không, hay chỉ 6 loại giá bán?**

Vì `product_units` (46.560 dòng) đang **trộn 2 loại dữ liệu**: cấu trúc ĐVT (dùng chung) và
giá vốn/giá mua ngoài (phải theo công ty).

| Trả lời | Hệ quả |
|---|---|
| **Có** | tách tầng giá khỏi `product_units` → thêm bảng `product_company_units`; sửa **34 file ERP** |
| **Không** | chỉ thêm `company_id` vào `product_unit_prices`; giá vốn vẫn dùng chung cho 8 công ty |

### 3.2. Hai hướng đang ngược nhau (§24f)

| | §19 giá | §24 dữ liệu quản trị |
|---|---|---|
| `company_id` | nullable, `NULL` = giá chung *(đề xuất)* | **NOT NULL** *(đã chốt)* |
| Cột cũ | giữ làm giá trị chung | **xoá cột chung** |
| ERP phải sửa | **0 file** | **71 file** |

⇒ Cần chốt **một hướng duy nhất** cho cả hai.

### 3.3. ~~Ô "Đời xe" hiển thị thế nào~~ — ✅ ĐÃ CHỐT 23/09/2026 (§26d-bis)

Đối chiếu ERP thì đoạn ô *Đời xe* phẳng **đã bị comment**; cấu trúc thật là **bảng bộ ba**
Hãng xe (gộp dòng) | Loại xe | Model xe | **Đời xe chọn nhiều riêng từng model**. Đi theo ERP.
Nội dung cũ giữ lại bên dưới để tra:

### 3.3. Ô "Đời xe" hiển thị thế nào (§15d)

Dữ liệu là **bộ ba** hàng hoá × Model xe × Đời xe (`product_vehicle_model_has_life`, 48.736 dòng /
91 hàng hoá), không phẳng. Mockup đang tạm để **một ô chọn nhiều**.
→ Bảng con dưới mỗi Model đã chọn *(đúng cấu trúc, ERP có sẵn 2 hàm để port)* / một ô chọn nhiều
áp chung / chỉ đọc đợt này?

### 3.4. Việc đã lỡ làm vào source thật TRƯỚC khi có §22 — giữ hay gỡ?

Tất cả đều đã chạy thật, e2e xanh:
2 cờ khai báo trên màn Loại sản phẩm (kèm migration) · 2 màn Dòng xe/Tải trọng xe · 6 màn danh mục
Xe (kèm migration `vehicle_life.status`) · Task C1 sinh mã hàng hoá.

### 3.5. Cột `status` thêm vào `vehicle_life` — giữ hay trả về đúng ERP?

Bảng gốc không có `status`. Thêm cột thì Đời xe có Khoá/Mở khoá; bỏ thì nút Xoá là **xoá cứng**
trên danh mục đang bị 48.736 dòng tham chiếu, không FK nào chặn.

---

## 4. ✅ Đã chốt — 25 quyết định

Chi tiết ở `man-danh-muc-hang-hoa/design.md`, mục § tương ứng.

### 4.1. Phạm vi & dữ liệu

| § | Chốt |
|---|---|
| 1 | 8 trường ERP tài liệu không liệt kê → **GIỮ**, xếp vào tab hợp lý |
| 3 | `product_cate` → **đóng băng**, thay bằng **Chính sách kinh doanh** ⚠️ *(cột lưu chưa tồn tại — xem §24a)* |
| 4 | `can_retail` → **bỏ hẳn** (đã gỡ cột + 2 registry) |
| 5 | Quy chế `regulation_product_types` → không phải ràng buộc, bỏ qua |
| 6 | `product_type` (enum cũ 16 giá trị) → **KHÔNG ánh xạ** sang cây mới |
| 9 | Đơn vị tính ↔ Giá bán → giữ nguyên logic ERP, chỉ **bỏ đồng bộ CRM** |
| 14a | Thuộc tính nối lên **Loại sản phẩm** (đảo ngược 8c) |
| 16 | **Mã hàng hoá sinh MỘT LẦN, giữ mãi mãi** — kể cả khi hãng SX / code đặt hàng / model đổi |
| 20 | Phase 2 chỉ còn phần **THÔNG TIN** hàng hoá; giá sang Phase 8 |
| 21 | **Giữ bảng `groups`** với vai trò Nhóm máy; Phase 5 chỉ gỡ **MÀN** |
| 26c-bis | **3 mức quyền sửa trên cùng form**: công ty TẠO RA sửa cả 6 tab · công ty LẤY HÀNG VỀ chỉ sửa tab *Dữ liệu quản trị* · vai TÍNH GIÁ khoá cả 6 tab, chỉ làm tab *Giá bán*. Thông tin dùng chung chỉ có MỘT chủ là công ty tạo ra hàng hoá — BE phải chặn, không chỉ khoá FE |
| 27 | **Báo cáo hàng hoá theo công ty** = **ma trận** 29 mã × 8 công ty, ô là trạng thái · "đang sử dụng" tính theo **có bản ghi trạng thái** (đếm tách *Khai thác* / *Kinh doanh*) · dùng lại bộ cột màn danh sách · **không có kỳ**, là ảnh chụp hiện trạng |
| 28 | **Cấu hình giá bán nội bộ**: khoá theo **Hãng sản xuất** × **một công ty mua** (khai nhiều hãng một lượt bằng popup chọn nhiều; màn là MỘT LƯỚI nhập tại chỗ, không có popup form) · 2 nguồn hàng hard-code *nhập khẩu nguyên lô / tồn kho* · theo giá vốn `×(1+%)`, theo giá bán `×(1−%)` áp cả 6 loại giá · **chỉ là số GỢI Ý**, không ghi vào bảng giá · mỗi công ty tự khai bộ của mình · không có ngày hiệu lực, có lịch sử · hãng chưa cấu hình thì cảnh báo lúc lấy hàng về · độc lập với `manufacture_expect_prices` + `company_price_types` |
| 26 | **Quy trình 3 bước**: Đang nhập thông tin → Chờ tính giá bán → (Đang tính giá) → Đang kinh doanh; **trạng thái theo TỪNG CÔNG TY**; 3 màn + 2 quyền; nút **"Xem hàng hoá Công ty khác"** để công ty B lấy hàng của A về khai tiếp |

### 4.2. Giao diện

| § | Chốt |
|---|---|
| 2 → 23 | Tab Dữ liệu quản trị **bỏ tab lồng theo Công ty** — công ty nào khai của công ty đó |
| 15 | Tab **Phân loại xe** — chuyển nguyên khối "Phụ tùng ô tô" của ERP, bỏ bắt buộc |
| 18a | **Giá tách khỏi form** → màn quản lý giá riêng (Phase 8) |
| 18b | 2 cờ khai báo (Phân loại xe · Nhóm máy) đặt ở **Loại sản phẩm** (cấp lá) |
| 21a | Khối Nhóm máy giữ **2 tầng** như ERP: chọn nhóm → rồi chọn máy |
| — | Mockup: bỏ **ghi chú logic** khỏi giao diện (giữ trong comment nguồn) |

### 4.3. Luồng & thứ tự

| § | Chốt |
|---|---|
| 10 | ERP **chỉ ĐỌC** hàng hoá; toàn bộ luồng GHI sang HRM |
| 11 | Luồng Tính giá sang HRM · lịch sử làm theo cách HRM · **bỏ version** |
| 12 | Thứ tự chuyển + tiêu chí nghiệm thu |
| 13 | **Chặn route ERP** + tập trung làm "ERP không lỗi" |
| 14b | **Hoãn** lịch sử hàng hoá |

### 4.4. Quyền & bảo mật

| § | Chốt |
|---|---|
| 23c | Chỉ thấy dữ liệu **công ty mình**; sửa chéo công ty **cấm tuyệt đối** → chặn ở **BE** |
| 23c | Công ty hiện tại lấy từ **`employee_infos.company_role`** *(KHÔNG phải `company_id`)*, lùi về `company_id` khi rỗng |
| — | 🔄 04/10: **giá (vốn + bán) ẩn HOÀN TOÀN khỏi các màn hàng hoá**, chỉ quản lý ở màn quản lý giá riêng (Phase 8) — thay ghi chú cũ "gate giá vốn theo `Quản lý giá`" (`2b-doc/khao-sat.md` Q2) |

### 4.5. CSDL — đợt migration đang chờ chốt (§24 + §25)

| # | Thay đổi | Bảng | Trạng thái |
|---|---|---|---|
| 1 | `+ company_id` | `product_unit_prices` | chờ §3.1, §3.2 |
| 2 | `+ company_id` **NOT NULL**, không chặn trùng | `product_suppliers` (1.741 dòng) | ✅ đã chốt cách làm |
| 3 | `+ business_policy_id` · `min_stock_qty` · `guarantee` · `guarantee_type` | `product_company_coefficients` | ✅ đã chốt cách làm |
| 4 | **XOÁ** 3 cột chung | `products` | ⚠️ **bước CUỐI**, sau khi rà xong file ERP |

❌ **KHÔNG** thêm `company_id` vào `product_expected_prices` — thừa hưởng qua `unit_price_id`.
📐 Quy tắc gán dữ liệu cũ: `company_id` = `products.company_id` của hàng hoá đó.
⚠️ **5 dòng giá mồ côi** (hàng hoá không có công ty) phải xử lý tay trước khi đặt NOT NULL.
⚠️ Sau khi gán: **7/8 công ty không có dòng giá nào** — phải chuẩn bị nhập liệu trước ngày bật.

---

## 5. 🔜 Để xử lý SAU — không thuộc Phase 2

| # | Việc | Ghi chú |
|---|---|---|
| 1 | **Quy đổi 45.890 hàng hoá sang cây phân loại mới** | Thứ tự bắt buộc: thêm cột → nhập cây → quy đổi → **rồi mới** bật lọc mới. Bật trước = 338 màn không tìm thấy hàng nào |
| 2 | Thay các chỗ lọc sang danh mục mới + **176 view** | |
| 3 | Xoá hẳn `product_cate` + 12 báo cáo + **11.372 dòng lịch sử** | |
| 4 | 3 cờ nghiệp vụ thay `product_type` | hàng hoá làm dịch vụ · báo giá dịch vụ · thiết bị của khách |
| 5 | Gỡ `group_id` khỏi form + **~116 chỗ** đọc thuộc tính nghiệp vụ của nhóm | ⚠️ KHÔNG xoá bảng `groups` (§21) |
| 6 | **Rà 29 file ERP** đọc `products.min_stock_qty` sau khi xoá cột | Đợt E |
| 7 | **Rà 42 file ERP** đọc `products.guarantee_type` | 🔴 giá trị được **chép sang 23 bảng chứng từ** — chép nhầm công ty là **đóng băng vĩnh viễn** |
| 8 | **Lỗi có sẵn ở 11 màn Phase 1**: bấm "Mở khoá" gọi nhầm `/lock` | so `Number(status) === 2` trong khi bảng ERP khoá bằng **0**. 11 file × 4 dòng. Chi tiết: `chuyen-danh-muc-xe/plan.md` |
| 9 | **Import** cho 6 màn danh mục Xe | màn import Model xe của ERP chưa chốt giữ hay bỏ |
| 10 | `VehicleLife::searchByFilter()` / `getForSelect()` của ERP **không lọc `status`** | bản ghi khoá ở HRM vẫn hiện bên ERP |
| 11 | "Cập nhật nhanh hàng hoá" chưa chốt thuộc phase nào | chạy trên `products` nhưng không nằm trong 2 màn của Phase 2 |
| 13 | **Bỏ sạch data catalog 4 cấp (§30e)** — 11 vấn đề phải xử lý | nặng nhất: `SearchController` (popup hàng hoá của **338 màn**) · `Product::searchByFilter` 4 nhánh · **129 chỗ/15 file** gọi `ProductGroupClassify` · 16 quyền `web` 100091–100106 |
| 12 | 3 điểm mockup tự quyết cần user duyệt | % giảm giá thanh lý xếp tab Mua hàng · Hệ số giá theo công ty dựng thành bảng · Trọng lượng/Kích thước/Serial xếp tab 1 |

---

## 6. 🐞 Bẫy đã trả giá — đọc trước khi code

| Bẫy | Hậu quả |
|---|---|
| **Bảng có ô tick vẽ lại theo từ khoá tìm** | tick xong gõ từ khoá khác là **mất tick im lặng** (tick 3 hãng, gõ tiếp ra 1). Phải giữ lựa chọn trong mảng tạm, cập nhật ngay mỗi lần tick |
| **`th rowspan=2` + `position:sticky`** | hàng tiêu đề tầng 2 tụt xuống **đè lên dòng dữ liệu đầu tiên**, ô nhập của dòng 1 biến mất — đếm DOM vẫn đủ ô, chỉ nhìn ảnh mới thấy. Bảng tiêu đề 2 tầng thì bỏ sticky cho `th`, chỉ giữ dính trái |
| **`iconv('ASCII//TRANSLIT')` khác nhau theo MÁY CHẠY** | `THANH ĐỒNG` → `THANHDONG` (Linux) vs `THANHDNG` (macOS). Mã không sinh lại khi sửa ⇒ lệch vĩnh viễn |
| **`products` KHÔNG dùng `SoftDeletes`** dù có `deleted_at` | 175 hàng hoá đang bán vẫn còn `deleted_at`. Bật trait là 175 mã biến mất im lặng |
| **`productables` gánh 5 loại quan hệ** | mọi thao tác phải kẹp `productable_type`; `sync(null)` xoá sạch 32.366 dòng Nhóm máy/Máy sử dụng |
| **KHÔNG `morphedByMany()`** cho `productables` | cột lưu tên class của ERP; khai quan hệ trỏ entity HRM = khớp 0 dòng |
| **Danh mục bảng ERP khoá bằng 0**, bảng mới #11421 khoá bằng 2 | chép khuôn nhầm ⇒ "Mở khoá" gọi `/lock` rồi báo "Khoá thành công" |
| **Menu hub lọc theo `subItems`** | khai `children` = cả nhóm biến mất, không lỗi nào báo |
| **`V2BaseIconButton` không có prop `icon`/`variant`** | icon qua slot, tông đỏ dùng `danger`. Sai ⇒ nút rỗng, Vue 2 im lặng |
| **id popup xác nhận phải = `confirm-<việc>-<catalogSlug>`** | lệch số ít/số nhiều ⇒ popup không mở, không lỗi |
| **`resetKeys` của SmartFilterPanel ≠ lọc dây chuyền** | nó là "xoá key khi field bị ẩn". Dùng sai ⇒ ô trống nhưng giá trị cũ vẫn gửi lên |
| **Trait PHP 7.4 không khai được hằng** | "Traits cannot have constants" |
| **`offsetParent` luôn null với `position: fixed`** | đo "đang hiện" bằng nó là luôn sai |
| **Grep thô đếm cả bảng khác trùng tên cột** | 42/86/44 → số thật 29/42/34 |
| **`table-layout:fixed` không khai tổng bề rộng** | trình duyệt co cột cho vừa khung: khai 44/52/150/250px ra thật 41/51/132/114px ⇒ toạ độ cột DÍNH TRÁI lệch, ô bị che. Phải cộng `tongW` rồi ghim `table.style.width` |
| **`max-height: calc(100vh - Npx)` ghim cứng cho vùng cuộn** | N đổi theo việc mở/đóng bộ lọc ⇒ sinh 2 thanh cuộn lồng nhau (đo: trang 975px trong khung 900px). Đo tại chỗ + nghe `resize` |
| **Nhãn nhóm căn giữa ô `colspan` rất rộng** | ô rộng 950px thì chữ căn giữa rơi ra ngoài khung nhìn, hàng tiêu đề trông như trống. Căn trái |
| **Không đoán tên bảng số nhiều** | `vehicle_life` số ít; dữ liệu thật hay nằm ở bảng NỐI |

---

## 7. Mở file nào khi quay lại

| Cần gì | Mở |
|---|---|
| Đầu mối tổng | **file này** |
| Spec chi tiết Phase 2 (25 mục §) | `man-danh-muc-hang-hoa/design.md` |
| Task + checkpoint Phase 2 | `man-danh-muc-hang-hoa/plan.md` |
| Phase 2b (6 màn Xe) | `chuyen-danh-muc-xe/design.md` + `plan.md` |
| Phạm vi & roadmap toàn feature | `quan-ly-hang-hoa/design.md` |
| Trạng thái toàn nhánh gộp DB | `.plans/gop-db/STATUS.md` |
| Mockup đang chạy | `/master-data/mockup-hang-hoa` · `/master-data/mockup-hang-hoa/form` |
| Mockup luồng 3 bước | `man-danh-muc-hang-hoa/mockup-luong-xay-dung-hang-hoa.html` |
| Mockup báo cáo (§27) | `man-danh-muc-hang-hoa/mockup-bao-cao-hang-hoa.html` |
| **Bảng danh mục hàng hoá cho nghiệm thu** | `danh-sach-danh-muc-hang-hoa.xlsx` (25/09/2026) — 6 làm mới · 11 + 6 chuyển ERP · 3 chưa mở · 5 sẽ bỏ |
| Mockup cấu hình giá nội bộ (§28) | cùng file mockup luồng 3 bước — menu trái *Cấu hình giá bán nội bộ* |
