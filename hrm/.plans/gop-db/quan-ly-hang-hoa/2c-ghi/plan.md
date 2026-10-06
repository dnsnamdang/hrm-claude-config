# Đợt 2-C — Ghi: plan

> 04/10/2026 · @namdangit · chốt: `chot.md` (T6, H1', H1'', G1–G11) · khảo sát: `yeu-cau-ghi.md`, `erp-ghi-hang-hoa.md`.
> Mỗi đợt con: nhánh con từ `feat/chuyen-doi-hang-hoa`, xin "làm" RIÊNG (nêu repo · file · DB), xong merge về nhánh chung. ⛔ không `gop_db`.

## 0. Thứ tự

| Đợt con | Nội dung | Trạng thái |
|---|---|---|
| **2-C3 Catalog** | popup *Xây dựng catalog kinh doanh* + *Xếp vào tiểu mục…* ở màn Dữ liệu hàng hoá công ty; giỏ chờ + `sync` (B1); quyền 1655 | 🔄 đang làm (nhánh `feat/p2c3-catalog`) |
| 2-C1 Tạo + sửa (công ty tạo) | sinh mã (`ProductCodeGenerator` nhánh cũ) · form tạo/sửa 2 tầng tab · 1 nút Lưu (G3) · `products.status = 1` (G1) · đơn vị cơ bản + 6 dòng giá 0 (G2) · dòng công ty `coefficient 1, status 1` · Hệ số công nghệ chung (T6) · cờ "Phụ tùng ô tô" ở Tính chất hàng hoá + ẩn/hiện tab xe (G11) · Sửa ở menu dòng + chi tiết (G9a) | ⬜ |
| 2-C2 Lấy về + sửa mức Quản trị | lấy về 1/nhiều (≤100, chỉ `products.status = 1` — G9b), upsert dòng công ty (dòng hệ số cũ `status NULL` ⇒ UPDATE) · công ty lấy về chỉ sửa tab Quản trị (BE chặn lớp chung) · hàng cũ chưa có dòng ⇒ sinh dòng status 3 (G4) | ⬜ (tồn nhỏ: lọc hàng ERP đã xoá ở Kho dữ liệu) |
| 2-C4 Vòng đời | Xoá (G7: kiểm như ERP + xoá cứng / gỡ dòng công ty) · Khoá/Mở khoá theo công ty status 4 (G6) | ⬜ |
| — | KHÔNG làm: Lưu nháp (G3), nút Chuyển kinh doanh (H1''), Sao chép (G8), lịch sử (§14b), Excel (2-E), giá | |

## 1. Đợt 2-C3 Catalog — chi tiết

### Phạm vi xin phép
| | |
|---|---|
| Repo · nhánh | `hrm-api` + `hrm-client`, nhánh `feat/p2c3-catalog` từ `feat/chuyen-doi-hang-hoa` |
| BE | quyền **1655** *Xây dựng catalog kinh doanh* (seeder) · endpoint danh sách hàng cho popup (hàng có trạng thái tại công ty, kèm thông số cơ bản tóm tắt — eager load) · `POST master-data/products/catalogs/assign` + `/unassign` (product_ids ≤100 × job_cluster_id; chỉ Tiểu mục thuộc cây mới H3; chỉ hàng có trạng thái tại công ty mình; idempotent theo UNIQUE 3 cột) · PHPUnit có/không quyền |
| FE | popup *Xây dựng catalog kinh doanh* (cây 4 cấp mở/thu toàn bộ + từng lĩnh vực §36f, bảng hàng 12 cột, lọc 8 ô) · nút *Xây dựng catalog* + thanh chọn dòng *Xếp vào tiểu mục…* ở màn Dữ liệu hàng hoá công ty (gate 1655) · Playwright MCP + e2e |
| DB local | INSERT quyền 1655 + gán role 18 + `cache:clear` — hỏi riêng |

### Task
- [x] C3.1 Đọc kỹ mockup §33 (popup) + §36f, ghi bộ cột/lọc/hành vi vào `2c-ghi/c3-popup.md`
- [x] C3.2 BE: quyền 1655 + `GET catalogs/products` (tab add|in, `target_cluster_id`) + `GET catalogs/counts` + `POST catalogs/sync` (1 transaction, ≤1.000 cặp, khoá 4 cấp B2, Ngừng KD B3) + `JobCluster::childrenCount()` đếm hàng đã xếp (chặn xoá, không chặn khoá) + PHPUnit `ProductCatalogApiTest` 6/6 · hồi quy Read 8/8, Tree 12/12, Foundation 5/5 · DB local: INSERT quyền 1655 + role 18 (user cho phép)
- [x] C3.3 FE: `components/product/catalog/ProductCatalogBuilderModal.vue` + `ProductCatalogTree.vue`; `ProductListPage.vue` thêm nút *Xây dựng catalog*, cột tick dòng, thanh *Xếp catalog* (chỉ màn công ty + quyền 1655). Nhãn nút rút 3 chữ theo skill (user chốt): *Thêm hàng hoá* · *Gỡ hàng hoá* · *Xếp catalog*, câu đủ ở tooltip. Lỗi tự bắt: `V2BaseCheckbox` bắn lại `change` khi đổi prop từ code ⇒ bỏ tick 1 dòng mất cả trang (100 → 80) — thêm cờ chặn như discount-types
- [x] C3.4 Playwright MCP (agent đo đủ luồng trên nhánh mẫu E2EC3, đã dọn sạch: 0 nút E2EC3, counts `{}`; lead đo lại: popup 1460px, không còn tên cấp cũ, ô tick dòng có) + spec `products-catalog-popup-ui.spec.ts` 7 ca (`--list` OK, **chưa chạy**); sửa `products-read-ui.spec.ts` cho phép nút *Xây dựng catalog* ở màn công ty

### Lệch mockup (UI) đã ghi
Không làm "Dán danh sách mã" (chưa có endpoint) · nút Lưu/Thêm/Gỡ ẩn khi chưa dùng được · tổng số khi giỏ đầy là xấp xỉ (API không nhận danh sách loại trừ) · câu cảnh báo chưa lưu theo mixin chuẩn · dòng mô tả nằm đầu thân popup

### Checkpoint — 2026-10-04 (wrap up)
Vừa hoàn thành: đợt 2-C3 Catalog code xong C3.1–C3.4 trên `feat/p2c3-catalog` (api + client + e2e). PHPUnit `ProductCatalogApiTest` 6/6, hồi quy Read 8/8 · Tree 12/12 · Foundation 5/5. DB local: quyền 1655 + role 18. Dữ liệu mẫu E2EC3 đã dọn.
Đang làm dở: CHƯA commit (api 7 file sửa + 5 file/thư mục mới; client 3 file sửa + `components/product/catalog/`); spec `products-catalog-popup-ui.spec.ts` (7 ca) + sửa `products-read-ui.spec.ts` chưa chạy.
Bước tiếp theo: user duyệt (1) commit + merge `feat/p2c3-catalog` → `feat/chuyen-doi-hang-hoa` + push (⛔ không gop_db); (2) có chạy 2 spec e2e không → rồi mở đợt 2-C1 (Tạo + sửa, công ty tạo).
Blocked: chờ user cho phép commit.
