# Design — Mockup màn Chi tiết Báo giá (thử nghiệm UI Bán hàng)

> Nhánh `gop_db`. Feature phụ trách: @namdangit.
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-08-06-mockup-chi-tiet-bao-gia-design.md`

## Mục tiêu

Tạo 1 file **mockup HTML tĩnh** mô phỏng màn **Chi tiết báo giá** (`/assign/quotations/{id}`) của phân hệ
Bán hàng, dùng làm sân thử nghiệm nhanh các thay đổi giao diện trước khi áp vào code thật
(`hrm-client/pages/assign/quotations/`). User note yêu cầu → sửa ngay trên mockup để duyệt, KHÔNG đụng code thật.

## Scope

- **Trong scope:** 1 file `chi-tiet-bao-gia-mockup.html` self-contained (không phụ thuộc CDN), tận dụng
  shell (topbar + sidebar) & palette teal từ `menu-ban-hang/menu-mockup.html`.
- **Ngoài scope:** không sửa code Vue thật, không tạo API, không đụng DB. Đây chỉ là mockup tĩnh để duyệt UI.
- Liên quan (không trùng): `update-style-ban-hang` (áp style MISA vào code thật) — mockup này là bước phác thảo trước.

## Nguồn dữ liệu mô phỏng

Chụp & trích từ màn thật `http://127.0.0.1:3000/assign/quotations/80` (báo giá **BG-2026-00080**, trạng thái *Đang tạo*).

## Các khối màn (mô phỏng đúng thứ tự màn thật)

1. **Topbar**: logo BÁN HÀNG · tiêu đề "Báo giá: BG-2026-00080 (Đang tạo)" · nhóm icon phải + user.
2. **Sidebar trái**: ô tìm chức năng, Yêu thích, Gần đây + 11 mục menu phân hệ (Bán hàng active).
3. **Thông tin chung**: card, lưới 2 cột (Mã BG, Dự án, Khách hàng, MST, liên hệ, địa chỉ, hiệu lực,
   bảo hành, loại tiền tệ + bảng giá, người lập…) + meta người lập/ngày tạo.
4. **Giảm giá**: dòng trạng thái "Không có".
5. **Chi tiết báo giá**: card + nút "Ẩn cột chi tiết"; bảng 18 cột (scroll ngang), có nhóm
   `A — Hàng hoá`, section `I. TTB SỬA CHỮA CHUNG`, item cha–con (6, 6.1, 6.2), dòng TỔNG.
6. **Tổng hợp giá trị báo giá**: bảng 5 dòng (Hàng hoá / Dịch vụ / Chi phí / Chi phí vận chuyển / Tổng).
7. **Điều khoản báo giá**: "—".
8. **Thanh hành động** (sticky): Quay lại · Lịch sử · Xuất Excel · In.

## Quyết định thiết kế

- Self-contained (inline CSS + SVG) để mở trực tiếp bằng browser, không cần server/CDN.
- Palette & shell kế thừa `menu-mockup.html` (teal `#12a594`) để đồng bộ bộ mockup Bán hàng.
- Bảng chi tiết wrap trong `overflow-x:auto` vì 18 cột rộng hơn màn.

## Hướng thiết kế đã chốt (sau các phase tinh chỉnh)

- **Màu nhận diện = NỀN màn chọn phân hệ** (không dùng màu nhóm tím): navy `#0a1c3d→#1e57a0`, chủ đạo `#2E71C3`,
  sáng `#4C90D9`, glow `#6fb2ff`, chữ trên navy `#eaf1fb/#b6c8e2`. Nguồn: `layouts/system.vue` + `components/subsystems.js`.
- **Chrome navy hiện đại**: topbar + sidebar gradient navy, glow mềm; active item pill phát sáng viền `#6fb2ff`;
  icon menu mỗi mục 1 màu; nền sidebar có **bó đường sóng ribbon** (SVG spirograph, mềm mại).
- **Accent nội dung teal**: tiêu đề card `#0a99a7`; header bảng teal nhạt `#eefafb→#e2f5f6` + chữ teal `#0a7c88` + viền teal;
  nhóm/tổng/hover đồng bộ gam teal. Button: primary (gradient xanh) / outline / ghost.
- **Thông tin chung thu gọn được** (chevron) → summary 1 hàng, đẩy bảng chi tiết lên.

## Cách làm việc

User đưa yêu cầu chỉnh → sửa trực tiếp file mockup → user mở lại file để duyệt. Mỗi yêu cầu ghi 1 task ở `plan.md`.
