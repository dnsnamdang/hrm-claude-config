# Tồn Phase 6 — Danh mục hàng tạm (gộp 12/10/2026)

> ⛔ **BỊ THAY 12/10/2026** — user gạt hướng "chép ERP", brainstorm phương án mới ⇒ xem `design.md` (D1–D10). Bảng dưới chỉ để tra cứu.

> Nguồn: `khao-sat-be-erp.md` (H1–H13) + `khao-sat-fe-erp.md` (F1–F14). Gộp câu trùng, đánh số lại Q1…; hỏi user **lần lượt từng câu**.
> Đã xác nhận lại trong code (12/10): ERP `TmpProductsController@approve:567` ⇒ `Product::createRecord()` sinh đủ bộ giá + `pcc.status = 3`
> ngay (`app/Product.php:7163-7167`, mốc `@TODO-PHASE6`) ⇒ hàng tạm là **cửa thứ hai đặt giá**, lệch §29a-1 "mọi hàng qua chứng từ tính giá".

| # | Câu (gộp từ) | Đề xuất ⭐ | Chốt |
|---|---|---|---|
| Q1 | **Duyệt hàng tạm xong: hàng ra trạng thái gì, còn tự đặt giá không?** (H1, H9, F3) | ⭐ Không đặt giá. Duyệt ⇒ sinh hàng hoá HRM ở **Chờ tính giá (2)** tại công ty đích, đi luồng YCHG→YCTG→PTG như mọi hàng. Form hàng tạm bỏ bảng giá; giữ 1 ô **Giá dự kiến** chỉ tham khảo (sale cần để báo giá) | |
| Q2 | Duyệt có nối thẳng sang luồng tính giá không? (H2) | ⭐ Không tự sinh YCHG; hàng vào màn Chờ tính giá như hàng tự tạo, PTKD lập YCHG từ đó (nút "Lập yêu cầu hỏi giá" đã có) | |
| Q3 | Hàng sinh ra thuộc công ty nào? (H3, H4) | ⭐ Công ty **của người lập hàng tạm** (khớp mô hình theo công ty, HRM tạo hàng ở công ty đang làm việc); không thêm cột `company_id` cho `tmp_products` — suy từ phiếu YC (có `company_id`?) hoặc công ty người tạo. Phương án B: công ty quản lý hãng như ERP | |
| Q4 | Ai duyệt, phạm vi xem? (H5, F13) | ⭐ Quyền HRM mới "Duyệt hàng tạm" **trong công ty phiếu** + giữ người phụ trách Thương hiệu–Hãng; lọc theo công ty (ERP không lọc) | |
| Q5 | Ai tạo hàng tạm / lập phiếu? (H6) | ⭐ Quyền HRM mới "Thêm hàng tạm" (ERP đang mượn "Thêm báo giá" — 460 NV) | |
| Q6 | Giữ Phiếu YC duyệt hàng tạm (1 phiếu – n hàng)? (H7, F7) | ⭐ Giữ làm "gói gửi duyệt" + in; duyệt / không duyệt từng dòng ngay trong chi tiết phiếu | |
| Q7 | Lối tạo hàng tạm sau Phase 6 (H8, F5, F6) | ⭐ (a) nút Thêm mới ở danh mục HRM; (b) báo giá dự án HRM gọi **service nội bộ** thay API ERP `sync-from-hrm`; (c) Báo giá thường ERP nút "➕ Hàng tạm" ⇒ trỏ sang HRM (ERP chặn tạo). Không làm popup thêm nhanh riêng | |
| Q8 | Đặt tên / menu (F2) | ⭐ "Danh mục hàng tạm" (phân hệ Danh mục dùng chung › Hàng hoá); đổi nhãn mục dự án hiện có thành "Hàng tạm dự án" | |
| Q9 | Form hàng tạm theo cây phân loại mới? Chi tiết tách khỏi form? (F1, F4) | ⭐ Dùng `ProductForm` HRM (cây mới); tách chi tiết chỉ đọc `/{id}` + form `/{id}/edit`; Duyệt mở form ở chế độ duyệt (người duyệt hay sửa trước khi duyệt) | |
| Q10 | "Hàng tạm của tôi" (F8) | ⭐ Gộp vào danh sách: lọc nhanh Của tôi / Chờ tôi duyệt / Tất cả | |
| Q11 | Xoá (F10) | ⭐ Có hộp xác nhận; người tạo xoá được hàng tạm Đang tạo / Không duyệt của mình; người duyệt xoá được Chờ duyệt | |
| Q12 | Xuất file (F12) | ⭐ Chỉ Xuất Excel theo bộ lọc | |
| Q13 | Thông báo + dashboard (H12, F11) | ⭐ 1 thông báo / phiếu, lọc theo công ty, link chi tiết HRM; thẻ dashboard ⇒ danh sách lọc "Chờ tôi duyệt" | |
| Q14 | Chặn duyệt khi có hàng mượn/giữ quá hạn (`checkDueConfigs`) (H10) | ⭐ Không port; ghi việc ngoài luồng | |
| Q15 | Dữ liệu cũ (H11) — 1.957 hàng tạm, `products.tmp_product_id` bẩn 7.057/8.931 | ⭐ Giữ nguyên, không sửa; HRM nối hàng tạm ↔ hàng hoá phải kèm `p.created_at >= t.created_at` | |
| Q16 | Màn "Làm lại báo giá" ERP (F14) | ⭐ Ngoài Phase 6; chỉ đảm bảo hàng duyệt ở HRM vẫn ghi `products.tmp_product_id` | |
| — | Lỗi sẵn có ERP (H13, F mục 6) | ✅ đã có chốt chung 12/10: **sửa hết trước khi update prod** ⇒ ghi vào `viec-con-lai.md` bảng C (không vá trong luồng) | ✅ |
