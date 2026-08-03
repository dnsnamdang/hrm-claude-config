# Design — Tooltip ⓘ giải thích thuật ngữ nghiệp vụ

## Mục tiêu

Người dùng hover (desktop) hoặc chạm (cảm ứng) vào icon ⓘ cạnh nhãn trường để đọc định nghĩa nghiệp vụ của thuật ngữ đó. Tooltip ẩn khi rời chuột / chạm ra ngoài.

## Phạm vi — 5 thuật ngữ

| Thuật ngữ | Nội dung tooltip |
| --- | --- |
| Nhóm ngành | Là ngành kỹ thuật/công nghệ do TPE cung cấp, được phân chia theo tính chất công nghệ. |
| Nhóm giải pháp | Phân loại theo loại hình kỹ thuật cốt lõi, phản ánh một năng lực công nghệ cụ thể của công ty; là tập hợp các giải pháp tương đồng về công nghệ. |
| Ứng dụng | Là dây chuyền hoặc giải pháp thiết bị, giải quyết một hoặc nhiều công đoạn trong quy trình sản xuất, kinh doanh của khách hàng. (+2 gạch đầu dòng) |
| Loại hình hoạt động khách hàng | Là tập hợp cùng loại hình hoạt động sản xuất kinh doanh tương đồng về mặt công nghệ. |
| Lĩnh vực kinh doanh khách hàng | Khách hàng sản xuất kinh doanh sản phẩm dịch vụ cụ thể. |

Áp dụng ở **mọi màn có trường này** (user chốt), gồm cả bộ lọc màn danh sách và màn báo cáo.

## Quyết định lớn

**Tra từ điển theo nhãn thay vì gắn tay từng chỗ** (user chốt). `V2BaseLabel` đọc nhãn của chính nó → chuẩn hoá (bỏ `*`, `:`, gộp khoảng trắng, lowercase) → tra `utils/constants/field-hints.js` → khớp thì tự render `V2BaseFieldHint`.

- Lý do: nhãn xuất hiện ~40 chỗ, `V2BaseLabel` dùng 1153 chỗ toàn hệ thống. Sửa 1 file phủ hết, màn mới sau này tự có.
- Khớp **chính xác** cả chuỗi, không khớp chuỗi con → "Mã nhóm ngành", "Số ứng dụng" không dính tooltip.
- Alias khai báo trong `labels[]` của từng thuật ngữ (vd `nhóm ngành` + `tên nhóm ngành`).

Nhãn `<label>` thuần chưa chuyển sang `V2BaseLabel` thì gắn tay `<V2BaseFieldHint label="..." />`.

`CascadePairSelect` (cặp Loại hình : Lĩnh vực, Nhóm ngành : Nhóm giải pháp) tự render label từ prop `parentLabel/childLabel` → cho `parentTooltip/childTooltip` fallback sang từ điển, phủ hết 4 nơi gọi.

## Hành vi tooltip

- Trigger `hover` + `focus`, `tabindex="0"` trên icon → desktop hover, cảm ứng chạm (focus) hiện, chạm ra ngoài (blur) ẩn.
- `@click.prevent.stop` để click icon không kích hoạt input gắn với `<label>`.
- Nội dung nhiều dòng dùng `\n`, render bằng `white-space: pre-line` trong class global `.v2-field-hint-tooltip`.

## Dọn dẹp kèm theo

Bốn màn từng tự chế tooltip riêng (nội dung cũ, khác spec) đã gỡ để tránh 2 icon cạnh nhau: `assign-components/customer/CustomerForm`, `prospective-projects/CustomerBlock`, `prospective-projects/ProjectInfoSection`, `solutions/InfoTab`.

Ghi chú riêng của màn (vd "Nếu không tìm thấy Nhóm ngành... liên hệ Master Data") được nối vào cuối tooltip chung qua prop `hint-extra` thay vì popover riêng.

## Mở rộng

Thêm thuật ngữ mới: thêm 1 entry vào `FIELD_HINTS` (mã thuật ngữ + `labels[]` + `content`). Không phải sửa màn nào.
