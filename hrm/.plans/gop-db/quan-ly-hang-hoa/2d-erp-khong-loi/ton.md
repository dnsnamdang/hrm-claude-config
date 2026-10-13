# Đợt 2-D "ERP không lỗi" — Tồn trước khi lập plan

> 09/10/2026 · gộp từ `khao-sat-a-chan-ghi.md` §9 (A-Q1–Q9) + `khao-sat-b-doc.md` §7 (B-Q1–Q5). Không trùng câu.
> Luật cao nhất: `../2c-ghi/chot.md` + `SO-CHOT-VA-TON.md`. Hỏi LẦN LƯỢT; chưa trả lời hết thì không lập plan.

## A. Kỹ thuật — không hỏi

- Chặn ghi **theo từng route** bằng middleware mới (GET ⇒ trang "đã chuyển sang HRM" + link HRM; POST/AJAX ⇒ JSON), ẩn menu/nút. Không chặn ở model.
- Chặn cả `product_templates/*` ghi (🔴 `UpdateGenerateProduct` ghi đè 29.813 hàng), `product2/*`, `product-infos`/đồng bộ (0 dữ liệu).
- N2 Hãng SX: bỏ khối lặp `products` ở `update()` + ẩn thẻ "Hệ số giá theo công ty". N3 Thương hiệu: gỡ 2 lời gọi (đã chết).
- Danh sách trắng giữ: `updateEnglishName`, `updateHSCode`, `addEquipment`, mọi route đọc; luồng giá giữ tới Phase 8; hàng tạm giữ tới Phase 6.
- Đọc không lỗi M1–M7 (~38 dòng, 11 file ERP): `??` tại chỗ (PHP 7.4), N9 `whereNull OR != 'service_product'` (0 đổi với dữ liệu cũ).
- `productDelete` khai trùng ⇒ chặn cả 2. Không migration, không seeder.
- Việc ngoài luồng mới N28–N33 (A §7) ghi vào `chot.md`, không vá trong 2-D.

## B. Hỏi user

| # | Nguồn | Câu | ⭐ | Trả lời |
|---|---|---|---|---|
| Q1 | A-Q1 | Màn Danh mục hàng hoá ERP sau 2-D: giữ chỉ-xem hay đổi menu sang HRM | giữ chỉ-xem + link "Quản lý trên HRM" | 🔄 **đổi menu sang HRM** (09/10) — hệ quả: mất màn lịch sử cũ ERP; lối vào luồng giá ERP (`editPrices`, Cập nhật giá nhanh, Hàng chưa có công khoán) phải đặt chỗ khác ⇒ hỏi thêm Q1b |
| Q1b | — | Lối vào luồng giá khi bỏ menu HH ERP | menu riêng "Giá hàng hoá" ở ERP | 🔄 **chuyển hết luồng giá sang HRM, làm màn giá HRM NGAY trong 2-D** rồi mới chặn ERP (09/10). ⚠️ Phạm vi 2-D phình lớn (Cập nhật giá nhanh, Duyệt giá, Hàng chưa có công khoán…, kéo phần Phase 8 lên) ⇒ cần khảo sát riêng luồng giá ERP trước khi plan; Q13 (N5 cron) xem lại theo hướng này |
| Q2 | A-Q2 | Hãng SX/Thương hiệu ERP: chỉ bỏ ghi lan hay chặn luôn CRUD 2 danh mục | chỉ bỏ ghi lan | 🔄 **chặn luôn thêm/sửa Hãng SX + Thương hiệu ở ERP** (09/10) — vẫn bỏ ghi lan N2/N3; giữ route 3 màn con KPI/Cấu hình NV của Hãng SX (chỉ có ở ERP); sửa danh mục chỉ còn ở HRM Phase 1 |
| Q3 | A-Q9 | "Cập nhật nhanh hàng hoá" ERP: chặn? HRM cần màn tương đương? | chặn, màn sửa nhanh HRM vào backlog | ✅ theo ⭐ (09/10) |
| Q4 | A-Q3 | Nút tạo hàng dịch vụ trong Báo giá dịch vụ (`storeService`) | chặn + ẩn nút | ✅ theo ⭐ (09/10) |
| Q5 | A-Q6 | 6 route sửa dữ liệu một lần: middleware hay gỡ route | gỡ route | ✅ theo ⭐ (09/10) |
| Q6 | A-Q4 | Gọi route ghi đã chặn: 403 hay 200 + câu báo | 403 | ✅ theo ⭐ (09/10) |
| Q7 | A-Q5 | Observer chỉ ghi log các lần ghi `products` ngoài danh sách trắng | có | ✅ theo ⭐ (09/10) |
| Q8 | A-Q7 | Gỡ quyền Thêm/Xóa/Khôi phục hàng hóa khỏi role ERP | để nguyên | ✅ theo ⭐ (09/10) |
| Q9 | B-Q1 | N1 bảo hành/tồn tối thiểu theo công ty: 2-D hay sau | để sau, trước merge prod | ✅ theo ⭐ (09/10) |
| Q10 | B-Q2 | Mẫu tem hàng HRM (không có nhóm) | theo Tính chất hàng hoá | 🔄 **theo Loại SP (`product_types`) — thêm cột mới `barcode_template_type`** (09/10): migration HRM + ô chọn mẫu tem ở form Loại SP; ERP in tem + phiếu nhập JOIN `product_types`; phải điền mẫu cho từng Loại SP (chưa điền ⇒ mặc định mẫu 1 — chốt ở plan) |
| Q11 | B-Q3 | N8 hàng khoá theo công ty vẫn chọn được ở ERP | làm 2-D, chỉ ở popup | ✅ theo ⭐ (09/10) |
| Q12 | B-Q4 | Hàng HRM không vào Báo giá dịch vụ/phụ kiện theo thiết bị (enum cũ) | chấp nhận, để đợt 3 cờ | ✅ theo ⭐ (09/10) |
| Q13 | B-Q5 | N5 cron giá về 0 + N6 CRM | để Phase 8 | 🔄 **N5: ghi vào danh sách việc xử lý SAU khi xong các chức năng hàng hoá; N6 (CRM): BỎ** (09/10) |
| Q14 | A-Q8 | Nhánh ERP + DB kiểm | nhánh mới từ ERP `gop_db`, kiểm trên `hrm_erp` | ✅ theo ⭐ (09/10) — tạo nhánh/worktree/đổi `.env` vẫn xin riêng |

**09/10/2026: user chốt đủ Q1–Q14 (+Q1b, Q10 làm rõ).** Đổi so với ⭐: Q1 (bỏ menu HH ERP), Q1b (màn giá HRM làm trong 2-D), Q2 (chặn CRUD Hãng SX/Thương hiệu ở ERP), Q10 (mẫu tem theo Loại SP — thêm cột), Q13 (N5 để sau xong chức năng hàng hoá, N6 bỏ).

⚠️ **Phạm vi mới:** Q1b kéo luồng giá ERP (Cập nhật nhanh giá, Duyệt giá, Phiếu tính giá, giá theo hãng, công khoán, cron giá) sang HRM ngay trong 2-D ⇒ cần **khảo sát luồng giá** trước khi plan; đề xuất tách 2-D1 (chặn ghi + đọc không lỗi, phần không phải giá) và 2-D2 (màn giá HRM rồi chặn giá ERP). Q10 thêm migration HRM `product_types.barcode_template_type`.

## C. Hỏi user — luồng giá (từ `khao-sat-c-gia.md` §5, 09/10)

> Đính chính tiền đề Q1b: giá ERP có menu riêng *Kế toán → Quản lý giá - CTKM → Giá bán*; bỏ menu HH ERP chỉ mất 2 nút (Cập nhật giá — trùng màn ở Kế toán; Hàng chưa có công khoán).

| # | Câu | ⭐ | Trả lời |
|---|---|---|---|
| QC-0 | Màn giá HRM có chặn production không | tách 2-D1/2-D2; 2-D2 làm ngay sau, không chặn go-live | ✅ theo ⭐ (09/10) |
| QC-1 | "Chuyển hết" có gồm Phiếu tính giá | không, ở ERP tới Phase 7 | ✅ theo ⭐ (09/10) |
| QC-2 | Giá theo công ty trong 2-D2 hay sau | Phase 8; 2-D2 ghi bảng giá chung | ✅ theo ⭐ (09/10) |
| QC-3 | Hệ số giá đóng băng sau 2-D1 | khối hệ số theo hãng trên HRM, làm trong 2-D1 | 🔄 **đóng băng tới Phase 8** (09/10) — chấp nhận hàng mới của hãng ở HP/Vinh/SG bán giá TPE tới khi có giá riêng |
| QC-4 | Ai được sửa giá mã nào | giữ luật ERP (hãng SX + công ty tạo = công ty đang làm) | ✅ theo ⭐ (09/10) |
| QC-5 | Hàng "Đang nhập thông tin" có nhập giá | cho, không đổi trạng thái | 🔄 **không cho nhập** (09/10) — hàng HRM tạo giá 0 tới Phase 7 (luồng Tính giá) ⇒ chưa bật HRM tạo hàng thật để bán được trước Phase 7 |
| QC-8 | Công khoán + ghi chú | màn giá chỉ hiển thị; chặn Import công lắp đặt; xuất "Hàng chưa có công khoán" giữ route ERP, link ở menu Kế toán | ✅ theo ⭐ (09/10) |
| QC-9 | Lịch sử thay đổi giá | khuôn entity-history HRM, ngừng ghi `product_versions` | ✅ theo ⭐ (09/10) |
| QC-6 | Duyệt giá | bỏ | 🔄 **port sang HRM trong 2-D2** (09/10) — thêm bảng/luồng duyệt + màn + thông báo; cần khảo sát chi tiết luồng duyệt ERP (`approve*`, `is_company_price`) khi lập plan 2-D2 |
| QC-7 | Cập nhật giá theo hãng | bỏ | ~~port sang HRM trong 2-D2~~ ⇒ 🔄 **09/10 user đổi: chưa port HRM đợt này + KHOÁ bên ERP** — chặn tạo/lưu phiếu (chặn ở 2-D1 cùng middleware), giữ màn xem phiếu cũ; port HRM để sau (N36) |
| QC-10 | 2 cron + 3 màn chỉ xem | giữ ERP, chỉ chặn nút cập nhật thủ công | 🔄 **giữ ERP lúc này, ghi việc "chuyển sang HRM" để làm SAU** (09/10, N34). Chặn nút `manualUpdatePrices` (GET có ghi, N30) hay không — nêu trong plan 2-D2 |

**09/10/2026: user chốt đủ QC-0…QC-10.** Đổi so với ⭐: QC-3 (đóng băng hệ số tới Phase 8), QC-5 (không cho nhập giá hàng "Đang nhập thông tin"), QC-6 (port Duyệt giá), QC-7 (Cập nhật giá theo hãng: khoá ERP, chưa port), QC-10 (note chuyển sau).

**Phạm vi chốt:**
- **2-D1** (điều kiện production): chặn ghi hàng hoá ERP theo từng route + bỏ menu HH ERP + chặn CRUD Hãng SX/Thương hiệu (giữ 3 màn con KPI/Cấu hình NV) + gỡ 6 route sửa 1 lần + chặn `storeService`, Cập nhật nhanh hàng hoá, Import công lắp đặt, hàng gốc/Product2/đồng bộ + observer ghi log + ERP đọc không lỗi M1–M7 + N8 popup + mẫu tem theo Loại SP (migration HRM `product_types.barcode_template_type` + ô ở form Loại SP). ERP: nhánh mới từ `gop_db`, kiểm `hrm_erp`.
- **2-D2** (ngay sau, không chặn go-live): màn giá HRM ghi bảng giá chung — Cập nhật giá nhanh (luật sửa = ERP; không cho hàng "Đang nhập thông tin"; norm/ghi chú chỉ hiện; lịch sử kiểu HRM) + **Duyệt giá** ⇒ cần khảo sát thêm luồng Duyệt giá trước plan 2-D2 (Cập nhật giá theo hãng: khoá ERP ở 2-D1, port HRM để sau — N36); rồi chặn ghi giá thủ công ERP. Phiếu tính giá ở ERP tới Phase 7; giá theo công ty Phase 8; cron + 3 màn xem giữ ERP (N34).
