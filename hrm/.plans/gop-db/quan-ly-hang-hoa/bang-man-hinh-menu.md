# Bảng vị trí menu — feature Chuyển đổi hàng hoá (để nghiệm thu)

Lập lại 12/10/2026 theo **nhãn đọc từ giao diện đang chạy** (HRM worktree cổng 3031, nhánh `feat/chuyen-doi-hang-hoa` api `1e194fe5c` /
client `58965aa63`, tài khoản DNS Admin, màn rộng 1440). Mục bị ẩn vì tài khoản đo thiếu quyền thì lấy nhãn + vị trí từ file menu
(ghi rõ ở cột Ghi chú).
12/10: đã cấp đủ 817 quyền api cho DNS Admin (vai trò riêng T1_UAT_NAMDANG, công ty 1 + 4) ⇒ mọi mục trong bảng đã đo thấy trên DOM.

## Cách đi tới 1 màn (4 bước)

```
① Nút ⊞ "Chuyển phân hệ" (góc trên bên phải, cạnh chuông thông báo) → chọn PHÂN HỆ
② Menu trái (cột xanh đậm) → bấm NHÓM  ⇒ bảng trượt mở ra bên phải
③ Bảng trượt: cột giữa → bấm NHÓM CON   (phân hệ Danh mục dùng chung KHÔNG có bước này — bảng trượt ra thẳng danh sách chức năng)
④ Bấm CHỨC NĂNG ở cột phải
```

Menu chỉ hiện mục người dùng có quyền (cột "Quyền để thấy menu"). Super admin không được miễn — thiếu quyền là không thấy.

---

## A. Màn mở thẳng từ menu

### A1. Phân hệ **Danh mục dùng chung** (đầu menu trái ghi "DANH MỤC")

| # | Đã kiểm | ① Phân hệ | ② Menu trái | ③ Nhóm con | ④ Chức năng | URL | Quyền để thấy menu | Phase |
|---|---|---|---|---|---|---|---|---|
| 1 | ☐ | Danh mục dùng chung | **Hàng hoá** | — | Kho dữ liệu hàng hoá | `/master-data/products/warehouse` | Không cần | 2 |
| 2 | ☐ | Danh mục dùng chung | **Hàng hoá** | — | Dữ liệu hàng hoá công ty | `/master-data/products/company` | 1652 Xây dựng thông tin hàng hoá *hoặc* 1653 Xem dữ liệu hàng hoá công ty | 2 |
| 3 | ☐ | Danh mục dùng chung | **Hàng hoá** | — | Hàng hoá nhập thông tin | `/master-data/products/entering` | 1652 | 2 |
| 4 | ☐ | Danh mục dùng chung | **Hàng hoá** | — | Hàng đang kinh doanh | `/master-data/products/trading` | Không cần | 2 |
| 5 | ☐ | Danh mục dùng chung | **Phân loại hàng hóa** | — | Tính chất hàng hóa | `/master-data/product-natures` | 1574 \| 1575 | 0 |
| 6 | ☐ | Danh mục dùng chung | **Phân loại hàng hóa** | — | Nhóm chức năng | `/master-data/product-function-groups` | 1576 \| 1577 | 0 |
| 7 | ☐ | Danh mục dùng chung | **Phân loại hàng hóa** | — | Nhóm sản phẩm | `/master-data/product-families` | 1578 \| 1579 | 0 |
| 8 | ☐ | Danh mục dùng chung | **Phân loại hàng hóa** | — | Loại sản phẩm | `/master-data/product-types` | 1580 \| 1581 | 0 |
| 9 | ☐ | Danh mục dùng chung | **Phân loại hàng hóa** | — | Chính sách kinh doanh | `/master-data/business-policies` | 1582 \| 1583 | 0 |
| 10 | ☐ | Danh mục dùng chung | **Phân loại hàng hóa** | — | Đặc tính sản phẩm | `/master-data/product-characteristics` | 1584 \| 1585 | 0 |
| 11 | ☐ | Danh mục dùng chung | **Danh mục hàng hóa** | — | Thuế suất | `/master-data/tax-rates` | 1610 \| 1611 | 1 |
| 12 | ☐ | Danh mục dùng chung | **Danh mục hàng hóa** | — | Mã màu | `/master-data/color-codes` | 1608 \| 1609 | 1 |
| 13 | ☐ | Danh mục dùng chung | **Danh mục hàng hóa** | — | File đính kèm | `/master-data/attachment-types` | 1606 \| 1607 | 1 |
| 14 | ☐ | Danh mục dùng chung | **Danh mục hàng hóa** | — | Code đặt hàng | `/master-data/order-codes` | 1592 \| 1593 | 1 |
| 15 | ☐ | Danh mục dùng chung | **Danh mục hàng hóa** | — | Hãng sản xuất | `/master-data/manufacturers` | 1602 \| 1603 | 1 |
| 16 | ☐ | Danh mục dùng chung | **Danh mục hàng hóa** | — | Thương hiệu | `/master-data/brands` | 1600 \| 1601 | 1 |
| 17 | ☐ | Danh mục dùng chung | **Danh mục hàng hóa** | — | Thuộc tính | `/master-data/attributes` | 1596 \| 1597 | 1 |
| 18 | ☐ | Danh mục dùng chung | **Danh mục hàng hóa** | — | Đơn vị tính | `/master-data/units` | 1594 \| 1595 | 1 |
| 19 | ☐ | Danh mục dùng chung | **Danh mục hàng hóa** | — | Model | `/master-data/product-models` | 1590 \| 1591 | 1 |
| 20 | ☐ | Danh mục dùng chung | **Danh mục hàng hóa** | — | Đơn vị thuộc tính | `/master-data/attribute-units` | 1598 \| 1599 | 1 |
| 21 | ☐ | Danh mục dùng chung | **Danh mục hàng hóa** | — | Xuất xứ | `/master-data/origins` | 1604 \| 1605 | 1 |
| 22 | ☐ | Danh mục dùng chung | **Xe** | — | Hãng xe | `/master-data/vehicle-manufacts` | 1640 \| 1641 | 2b |
| 23 | ☐ | Danh mục dùng chung | **Xe** | — | Loại xe | `/master-data/vehicle-brands` | 1642 \| 1643 | 2b |
| 24 | ☐ | Danh mục dùng chung | **Xe** | — | Model xe | `/master-data/vehicle-models` | 1644 \| 1645 | 2b |
| 25 | ☐ | Danh mục dùng chung | **Xe** | — | Đời xe | `/master-data/vehicle-life` | 1646 \| 1647 | 2b |
| 26 | ☐ | Danh mục dùng chung | **Xe** | — | Dòng xe | `/master-data/vehicle-categories` | 1648 \| 1649 | 2b |
| 27 | ☐ | Danh mục dùng chung | **Xe** | — | Tải trọng xe | `/master-data/vehicle-payloads` | 1650 \| 1651 | 2b |
| 28 | ☐ | Danh mục dùng chung | **Catalog kinh doanh** | — | Chương | `/master-data/chapters` | 1670 \| 1671 | 2d |
| 29 | ☐ | Danh mục dùng chung | **Catalog kinh doanh** | — | Mục | `/master-data/job-groups` | 1672 \| 1673 | 2d |
| 30 | ☐ | Danh mục dùng chung | **Catalog kinh doanh** | — | Tiểu mục | `/master-data/job-clusters` | 1674 \| 1675 | 2d |

Thứ tự nhóm trên menu trái: Tổng quan · Địa lý · Ngân hàng · **Hàng hoá · Phân loại hàng hóa · Danh mục hàng hóa · Xe · Catalog kinh doanh** ·
Lĩnh vực Công ty kinh doanh *(gốc cây catalog, màn có sẵn — không thuộc feature)* · Đối tác · Ngân hàng câu hỏi khảo sát.
"a \| b" = có 1 trong 2 quyền (Xem \| Quản lý) là thấy menu.

### A2. Phân hệ **Tài chính**

| # | Đã kiểm | ① Phân hệ | ② Menu trái | ③ Nhóm con | ④ Chức năng | URL | Quyền để thấy menu | Phase | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|
| 31 | ☐ | Tài chính | **Quản lý giá - CTKM** | Giá bán | Phiếu tính giá | `/finance/price-calculates` | 1663 XNK xử lý yêu cầu hỏi giá \| 1664 Tính giá bán hàng hoá \| 1092 Xem giá vốn hàng hoá | T5 | Đứng ĐẦU nhóm Giá bán (đo DOM sau khi cấp quyền 12/10) |
| 32 | ☐ | Tài chính | **Quản lý giá - CTKM** | Giá bán | Cập nhật giá bán | `/finance/product-prices` | 1657 Cập nhật giá bán hàng hoá | G4 | |
| 33 | ☐ | Tài chính | **Quản lý giá - CTKM** | Giá bán | Duyệt giá bán | `/finance/product-price-approvals` | 1658 Duyệt giá bán hàng hoá | G5 | Lối chính |
| 33b | ☐ | Tài chính | **Chờ duyệt** | Giá bán chờ duyệt | Hàng hoá chờ duyệt giá bán | `/finance/product-price-approvals` | 1658 | G5 | Lối phụ — cùng màn #33 |

Menu trái Tài chính: Tổng quan · Khai Quy chế – Cấu hình · Khởi tạo · Khai báo đầu kỳ · Quản lý tiền · Hàng hoá - Dịch vụ - Vận chuyển · Kiểm kê ·
Kế toán bán hàng · Kế toán công nợ · **Quản lý giá - CTKM** · Kết chuyển cuối kỳ · Sổ tổng hợp · Báo cáo tài chính · **Chờ duyệt**.
Nhóm Giá bán còn 3 mục không phải màn mới: *Cập nhật giá theo hãng* (xám, không link — ERP đã ngừng), *Trạng thái cập nhật giá* và
*Hàng sắp điều chỉnh tăng giá* (mở ERP ở tab mới).

### A3. Phân hệ **Bán hàng**

| # | Đã kiểm | ① Phân hệ | ② Menu trái | ③ Nhóm con | ④ Chức năng | URL | Quyền để thấy menu | Phase | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|
| 34 | ☐ | Bán hàng | **Yêu cầu** | Hàng hóa | YC hỏi giá | `/sale/price-asking-requests` | Không cần (Q11) | T3 | Mục thứ 15/24 của nhóm Hàng hóa, ngay sau *YC duyệt hàng tạm* |
| 35 | ☐ | Bán hàng | **Yêu cầu** | Hàng hóa | YC tính giá | `/sale/price-calculate-requests` | 1663 \| 1664 \| 1092 | T4 | Ngay sau *YC hỏi giá* (đo DOM sau khi cấp quyền 12/10) |
| 36 | ☐ | Bán hàng | **Quy chế - Thiết lập** | Quy chế kinh doanh | Chính sách giá bán nội bộ | `/sale/internal-price-policies` | 1656 Cấu hình chính sách giá bán nội bộ | T1 | Mục cuối của nhóm (sau 3 mục Quy chế có sẵn) |

Menu trái Bán hàng: Tổng quan · Bán hàng · Bán dịch vụ · **Yêu cầu** · Báo cáo · Kế hoạch · Phê Duyệt · Danh mục · **Quy chế - Thiết lập**.

> Mục A: **36 màn**, 37 lối menu (#33b là lối thứ hai của #33).

---

## B. Màn KHÔNG có menu — mở từ màn khác (12 màn)

| # | Đã kiểm | Màn | URL | Vào từ đâu (bấm gì) | Quyền |
|---|---|---|---|---|---|
| 37 | ☐ | Tạo hàng hoá | `/master-data/products/create` | #3 Hàng hoá nhập thông tin → nút **Tạo mới** | 1652 (trang tự chặn) |
| 38 | ☐ | Chi tiết hàng hoá | `/master-data/products/:id` | Bấm mã / tên hàng ở #1–#4; hoặc mã hàng ở #32 / #33 (mở tab mới) | Xem không chặn; nút Sửa / Xoá / Khoá cần 1652 |
| 39 | ☐ | Sửa hàng hoá | `/master-data/products/:id/edit` | Nút **Sửa** ở danh sách #2–#4 hoặc chân màn #38 | 1652 (trang tự chặn) |
| 40 | ☐ | Tạo YC hỏi giá | `/sale/price-asking-requests/add` | #34 → **Tạo mới**; hoặc #3 / #4 tick hàng → **Lập yêu cầu hỏi giá** | Không cần |
| 41 | ☐ | Chi tiết YC hỏi giá | `/sale/price-asking-requests/:id` | Bấm số phiếu ở #34; hoặc link YCHG trong form YCTG / PTG | Chặn trong form + API |
| 42 | ☐ | Sửa YC hỏi giá | `/sale/price-asking-requests/:id/edit` | Chân màn #41 → **Sửa** | Chặn trong form + API |
| 43 | ☐ | Tạo YC tính giá | `/sale/price-calculate-requests/add` | #41 dòng nhóm → **Lập YCTG**; hoặc #34 dòng nhóm → nút ⊕ | Chặn trong form + API |
| 44 | ☐ | Chi tiết YC tính giá | `/sale/price-calculate-requests/:id` | Bấm số phiếu ở #35; hoặc link trong form YCHG / PTG | Chặn trong form + API |
| 45 | ☐ | Sửa YC tính giá | `/sale/price-calculate-requests/:id/edit` | Chân màn #44 → **Sửa** | Chặn trong form + API |
| 46 | ☐ | Tạo phiếu tính giá | `/finance/price-calculates/add` | #44 (YCTG Chờ tính giá) → **Tính giá**; hoặc #31 → **Tạo mới** → chọn YCTG | Chặn trong form + API (1664) |
| 47 | ☐ | Chi tiết phiếu tính giá | `/finance/price-calculates/:id` | Bấm số phiếu ở #31; hoặc #44 → **Xem phiếu tính giá** | Chặn trong form + API |
| 48 | ☐ | Sửa phiếu tính giá | `/finance/price-calculates/:id/edit` | Chân màn #47 → **Sửa** (phiếu Đang tạo / Giá bị từ chối) | Chặn trong form + API |

⚠️ Lớp chặn URL của HRM đọc theo menu, nên 9 màn #40–#48 không bị chặn ở bước mở trang (#37 / #39 trang tự chặn) — nên gõ thẳng URL
bằng tài khoản thiếu quyền để kiểm form + API chặn đúng.

**Tổng: 36 + 12 = 48 màn.**

---

## C. Nút / popup gắn vào màn có sẵn

| Đã kiểm | Ở màn | Nút / popup | Quyền |
|---|---|---|---|
| ☐ | #2 Dữ liệu hàng hoá công ty | **Xây dựng catalog** (đầu lưới) · tick hàng → thanh xanh **Xếp catalog** ⇒ popup *Xây dựng catalog kinh doanh* | 1655 |
| ☐ | #1 Kho dữ liệu hàng hoá | Tick hàng → **Lấy về công ty**; hành động dòng **Lấy về** | 1652 |
| ☐ | #3, #4 | **Lập yêu cầu hỏi giá** (đầu lưới + thanh hàng loạt) | Không cần |
| ☐ | #2, #3, #4 | Hành động dòng **Xoá / Khoá / Mở khoá** theo công ty | 1652 |
| ☐ | #38 Chi tiết hàng hoá | Tab *Phân loại xe* (chỉ hàng xe) · tab *Quản trị hàng hoá* có catalog. **Không có tab Giá** | — |
| ☐ | #32 Cập nhật giá bán | Popup Lịch sử giá · Công thức · Gửi duyệt giá bán | 1657 |
| ☐ | #33 Duyệt giá bán | Duyệt / Không duyệt từng dòng + hàng loạt · Lịch sử giá | 1658 |
| ☐ | #34/#41, #35/#44, #31/#47 | Nút **In** (popup xem trước) ở chân màn chi tiết + hành động dòng **In** ở danh sách | Theo quyền xem |
| ☐ | #41 (dòng nhóm đã tính giá), #47 | **In kết quả** | Theo quyền xem |
| ☐ | #31 danh sách PTG | Hành động dòng **Xem giá bán mới** (phiếu đã duyệt) | Theo quyền xem |
| ☐ | #46 / #48 form PTG | Popup *Tạm tính giá mua từ công ty quản lý* | 1664 |

## D. Phía ERP (đối chiếu)

| Đã kiểm | Menu ERP | Hiện trạng |
|---|---|---|
| ☐ | Hàng hóa › Quản lý hàng hóa › **Danh mục hàng hóa (HRM)** | Mở #2 ở tab mới |
| ☐ | Kế toán › Quản lý giá - CTKM › **Cập nhật giá bán (HRM)** | Mở #32 ở tab mới |
| ☐ | Chờ duyệt › **Duyệt giá bán (HRM)** | Mở #33 ở tab mới |
| ☐ | 5 link luồng tính giá (Phiếu YC hỏi giá ×2, YC hỏi giá chờ duyệt, Phiếu YC tính giá, Phiếu tính giá hàng hóa) | **Vẫn mở màn ERP** — đợt T7 sẽ trỏ HRM + chặn |

---

## E. Phase 6 — Hàng tạm (thêm 13/10/2026, merge LOCAL chưa push)

| # | Đã kiểm | Màn / nút | Vị trí | URL | Quyền |
|---|---|---|---|---|---|
| 49 | ☐ | **Hàng tạm** (danh sách hàng tạm 6/7/8 của công ty: lọc Yêu cầu hỏi giá, tick + Lập YCHG hàng loạt, Sửa / Xoá / Lập YCHG) | Danh mục dùng chung › **Hàng hoá** › Hàng tạm (mục thứ 5) | `/master-data/products/temp` | Không cần (Sửa/Xoá: người tạo hoặc 1652) |
| 50 | ☐ | Nút **"Thêm hàng tạm"** trên form YCHG ⇒ popup 2 tab (Tái sử dụng dòng tạm BOM/báo giá · Thêm mới thủ công), Phân loại 5 ô bắt buộc | #34 YC hỏi giá › Tạo / Sửa phiếu, trái nút "Chọn hàng hoá" | `/sale/price-asking-requests/add` | Không cần |
| 51 | ☐ | **Form duyệt hàng tạm** (PTKD): tab Thông tin hàng hoá + Quản trị hàng hoá, nút Lưu · Đồng ý · Không duyệt · Hủy | #41 chi tiết YCHG Chờ PTKD duyệt › nút **"Duyệt"** trên dòng hàng tạm | `/sale/price-asking-requests/{id}/temp/{productId}` | 1662 (công ty phiếu) |
| 52 | ☐ | Nút **Duyệt phiếu** khoá khi còn hàng tạm chưa duyệt; dòng không duyệt mờ + lý do | #41 chi tiết YCHG | — | 1662 |
| 53 | ☐ | **Hàng tạm dự án** (đổi nhãn từ "Danh sách hàng tạm") | menu Giao việc | `/assign/product-project` | như cũ |
| 54 | ☐ | ERP: tạo / sửa / duyệt hàng tạm + phiếu YC duyệt hàng tạm ⇒ trang "Chức năng đã chuyển sang HRM" (xem danh sách cũ vẫn được) | ERP menu Danh mục hàng tạm, Hàng tạm - Hỏi giá | `/admin/tmp_products/*`, `/admin/sale/tmp_product_requests/*` | — |

⚠️ Muốn thử tạo hàng tạm trên DB dev phải có **Loại sản phẩm + Đặc tính** (hiện danh mục rỗng — nhập ở Danh mục dùng chung › Phân loại hàng hóa).
