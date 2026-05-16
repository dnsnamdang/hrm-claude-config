# HRM Claude Config

Repo lưu trữ config Claude Code cho các project của team.

## Danh sách project

| Project | Mô tả |
|---------|-------|
| nhatlinh | HRM cho Nhất Linh |
| hrm | HRM gốc |
| thanh_an | HRM cho Thành An |

## Setup

1. Clone repo:

   ```bash
   git clone git@github.com:dnsnamdang/hrm-claude-config.git
   ```

2. Chạy script link:

   ```bash
   cd hrm-claude-config
   ./setup.sh link <project-name> <đường-dẫn-project>
   ```

   Ví dụ:

   ```bash
   ./setup.sh link nhatlinh /Users/manhcuong/Desktop/dns/nhatlinh
   ```

3. Verify — kiểm tra symlink đã tạo đúng:

   ```bash
   ls -la <đường-dẫn-project>/.claude
   ls -la <đường-dẫn-project>/CLAUDE.md
   ```

## Thêm project mới

```bash
./setup.sh new <ten-project>
./setup.sh link <ten-project> <đường-dẫn-project>
```

Hoặc thủ công:

1. Tạo folder mới trong repo: `mkdir <ten-project>`
2. Copy cấu trúc từ project có sẵn hoặc tự tạo
3. Chạy `./setup.sh link` để kết nối

## Xem tổng quan

```bash
./setup.sh status
```

## Quy tắc

- Mỗi dev sửa config project mình phụ trách → commit vào folder tương ứng
- Commit message format: `[project-name] mô tả thay đổi`
- Không sửa config project khác khi chưa được đồng ý
