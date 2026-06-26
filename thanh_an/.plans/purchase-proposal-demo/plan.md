# Plan — Demo "Tạo đề xuất nhập hàng"

> Phụ trách: @khoipv · Ngày: 2026-06-25
> Spec: `docs/superpowers/specs/2026-06-25-purchase-proposal-demo-design.md`

## Phase 1 — Dựng file demo HTML
- [x] 1.1 Copy design system từ `bbnt_demo` (CSS biến màu, step card, bảng, modal, footer)
- [x] 1.2 Brand header "Tạo đề xuất nhập hàng"
- [x] 1.3 Bước 1: 3 type card (badge cấp duyệt) + field chung (mã ĐX, người ĐX, ngày, bộ phận, diễn giải)
- [x] 1.4 Hardcode data: DU_AN → HĐ bán đã duyệt → items; DANH_MUC hàng hóa chung
- [x] 1.5 Bước 2 config theo loại (L1: dự án→HĐ + info; L2: lý do mua; L3: nước NK + kho đích)
- [x] 1.6 Bước 3 bảng L1 (liệt kê hàng HĐ, cột SL theo HĐ/đã ĐX/còn lại/SL đề xuất)
- [x] 1.7 Bước 3 bảng L2 + modal chọn hàng từ danh mục (SL đề xuất)
- [x] 1.8 Bước 3 bảng L3 + modal (SL đề xuất + Hạn dùng)
- [x] 1.9 Validate L1 cảnh báo vượt SL còn lại (ô đỏ + banner, không chặn)
- [x] 1.10 Footer tổng hợp (số mặt hàng + tổng SL) + actions Lưu/Tải/Đẩy Excel (mock)

## Phase 2 — Hoàn thiện tài liệu (khi wrap up)
- [x] 2.1 Cập nhật design.md + spec đầy đủ
- [x] 2.2 Cập nhật STATUS.md

## Phase 3 — Rà soát & sửa lỗi nhỏ
- [x] 3.1 Sửa `colspan` group row Loại 1: 13 → 12 (đúng số cột thực tế)
- [x] 3.2 Bỏ field "Bộ phận đề xuất" ở Bước 1 (theo yêu cầu)
- [x] 3.3 Đổi nhãn "Diễn giải chung" → "Lý do đề xuất"
- [x] 3.4 Strip info HĐ theo kiểu BBNT/Thanh lý (nền trắng + viền + vạch ngăn; thêm địa bàn, nhà cung cấp, thời hạn thực hiện)
- [x] 3.5 Bỏ vạch ngăn dọc trong strip info HĐ
- [x] 3.6 Bỏ 2 nút "Tải Excel" / "Đẩy Excel", chỉ giữ "Lưu đề xuất"
- [x] 3.7 Đổi nhãn "Lý do đề xuất" → "Diễn giải chung"
- [x] 3.8 Loại "Mua hàng tồn kho": ẩn hẳn Bước 2 (bỏ Nước NK + Kho đích)
- [x] 3.9 Dồn số bước khi ẩn Bước 2 (1→2), Bước 3 đổi số động
- [x] 3.10 Bỏ cột "Hạn dùng" ở Loại 3 → bảng Loại 2 & 3 dùng chung bộ cột
- [x] 3.11 Đổi chọn loại đề xuất từ 3 type-card → `<select>` (label trên + `*`, convention màn thêm HĐ)
- [x] 3.12 Bỏ ô "Cấp duyệt" cạnh select loại đề xuất
- [x] 3.13 Dòng 1 (Loại/Mã/Người/Ngày) thành grid 4 cột bằng nhau (col-md-3), Diễn giải chung xuống dòng dưới
- [x] 3.14 Gộp "Thông tin theo loại" vào Bước 1 → còn 2 bước (1: chung+theo loại, 2: hàng hóa)
- [x] 3.15 Sắp lại bố cục Bước 1 (4 field → config theo loại → diễn giải chung); bỏ nền teal khối config; config L1/L2 dạng grid
- [x] 3.16 Bỏ các dòng hint thừa (L1, L2)
- [x] 3.17 Thông tin HĐ (L1) chuyển sang base input readonly (grid 4 cột) thay cho strip `.info`
- [x] 3.18 Loại 2: chọn "Hàng cho/tặng" → hiện thêm select Khách hàng (nhận hàng)
- [x] 3.19 Đổi toàn bộ field Bước 1 sang col-md-4 (grid 3 cột/hàng), đồng bộ cả config L1/L2 + info HĐ
- [x] 3.20 Sắp lại bố cục Bước 1: hàng 1 (Loại/Mã/Người), hàng 2 (Ngày/Diễn giải span2), config xuống dưới
- [x] 3.21 L1: đưa "Khách hàng (chủ đầu tư)" readonly lên cạnh "Hợp đồng bán" (auto-fill); info còn lại 3 cột hàng dưới
- [x] 3.22 L2: ô "Khách hàng (nhận hàng cho/tặng)" chèn ngay sau "Lý do mua" cùng hàng (display:contents)

## Phase 4 — Gom thư mục demos vào hrm-claude-config
- [x] 4.1 Chuyển `bc_dutoan_demo.html` (từ client) → `demo-bc-vong-doi-du-toan-hop-dong.html`
- [x] 4.2 Tạo `README.md` (index liệt kê file demo + quy ước đặt tên)
- [x] 4.3 Chuyển thư mục `demos/` vào `hrm-claude-config/thanh_an/demos/` (để đẩy chung repo config)
- [x] 4.4 Tạo symlink `dns/demos` → `thanh_an/demos` (giống `.plans`/`docs`/`CLAUDE.md`)
- [x] 4.5 Xác nhận `demos/` không bị `.gitignore` chặn → track được trong hrm-claude-config

## Checkpoint — 2026-06-26
Vừa hoàn thành: Sắp lại bố cục Bước 1 + bỏ nền teal khối config (dùng vạch ngăn)
Đang làm dở: (không)
Bước tiếp theo: Mở file trên trình duyệt review UX; nếu OK thì lên plan build thật (BE/FE)
Blocked: (để trống)
