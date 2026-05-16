# Claude Config Repo — Spec chi tiết

> Repo: `git@github.com:dnsnamdang/hrm-claude-config.git`
> Ngày: 2026-05-16
> Người phụ trách: @manhcuong

---

## 1. Mục tiêu

Tổ chức 1 repo Git duy nhất để:
- **Backup & version control** config Claude Code cho tất cả project
- **Chia sẻ cho team** — dev clone về, chạy 1 script là có config sẵn
- Hỗ trợ **thêm project mới** dễ dàng (7+ project, sẽ tăng dần)

## 2. Cấu trúc repo

```
hrm-claude-config/
├── README.md                    # Hướng dẫn cho team
├── setup.sh                     # Script tạo symlink
├── .gitignore                   # Ignore chung cho repo
│
├── nhatlinh/                    # Config cho project nhatlinh
│   ├── .claude/
│   │   ├── skills/              # Skills riêng project
│   │   ├── commands/            # Commands riêng project
│   │   └── settings.json        # Settings (không track settings.local.json)
│   ├── .plans/                  # Plans & STATUS.md
│   ├── docs/                    # Docs riêng project
│   ├── CLAUDE.md                # CLAUDE.md riêng project
│   └── .gitignore.project       # .gitignore dành cho project đích
│
├── hrm/                         # Config cho project HRM
│   └── (cấu trúc tương tự)
│
├── thanh_an/                    # Config cho project thanh_an
│   └── (cấu trúc tương tự)
│
└── [ten-project-moi]/           # Thêm project mới = thêm folder
    └── (cấu trúc tương tự)
```

### Quy tắc đặt tên folder
- Trùng với tên folder project thực tế trên máy
- Viết thường, dùng dấu gạch ngang (`-`) nếu cần

## 3. Script `setup.sh`

### 3.1 Lệnh `link` — tạo symlink

```bash
./setup.sh link <project-name> <đường-dẫn-project>
```

**Ví dụ:**
```bash
./setup.sh link nhatlinh /Users/manhcuong/Desktop/dns/nhatlinh
```

**Hành vi:**
1. Kiểm tra folder `<project-name>/` có tồn tại trong repo không → nếu không, báo lỗi
2. Kiểm tra `<đường-dẫn-project>` có tồn tại không → nếu không, báo lỗi
3. Với mỗi item cần symlink (`.claude/`, `.plans/`, `docs/`, `CLAUDE.md`):
   - Nếu target **chưa có** → tạo symlink
   - Nếu target **đã có và là symlink** → xóa symlink cũ, tạo mới
   - Nếu target **đã có và là file/folder thật** → hỏi user: overwrite (backup cũ rồi tạo symlink) hay skip
4. Xử lý `.gitignore.project`:
   - **Copy** (không symlink) thành `.gitignore` ở project đích
   - Nếu project đích đã có `.gitignore` → hỏi overwrite hay skip
5. In kết quả: danh sách item đã link thành công

**Danh sách item được symlink:**

| Source (trong repo config) | Target (trong project) | Kiểu |
|---|---|---|
| `<project>/.claude/` | `<target>/.claude/` | symlink |
| `<project>/.plans/` | `<target>/.plans/` | symlink |
| `<project>/docs/` | `<target>/docs/` | symlink |
| `<project>/CLAUDE.md` | `<target>/CLAUDE.md` | symlink |
| `<project>/.gitignore.project` | `<target>/.gitignore` | **copy** |

### 3.2 Lệnh `new` — tạo project mới (optional, phase 2)

```bash
./setup.sh new <ten-project>
```

**Hành vi:**
1. Tạo folder `<ten-project>/` trong repo
2. Tạo cấu trúc cơ bản: `.claude/skills/`, `.plans/STATUS.md`, `docs/`, `CLAUDE.md` (placeholder), `.gitignore.project`
3. In hướng dẫn: "Đã tạo config cho project <ten-project>. Chạy `./setup.sh link <ten-project> <path>` để kết nối."

### 3.3 Lệnh `status` — xem tổng quan

```bash
./setup.sh status
```

**Hành vi:** Liệt kê tất cả project trong repo (tên folder + số file config).

## 4. File `.gitignore` của repo

```gitignore
# OS
.DS_Store
~$*

# Claude Code local config (mỗi dev khác nhau)
**/settings.local.json

# Plans — file binary không cần track
**/.plans/**/*.pdf
**/.plans/**/*.html

# Docs — file tham chiếu không cần track
**/docs/test-cases/*.xlsx
**/docs/test-cases/~$*
**/docs/references/
```

## 5. File `.gitignore.project`

Đây là file `.gitignore` sẽ được **copy** vào project đích. Nội dung mẫu:

```gitignore
# Repo con (API + Client)
*-api/
*-client/

# OS
.DS_Store
~$*

# Claude Code local config
.claude/settings.local.json

# Plans
.plans/**/*.pdf
.plans/**/*.html

# Docs
docs/references/
docs/test-cases/*.xlsx
docs/test-cases/~$*
docs/superpowers/
.vscode
```

> Mỗi project có thể customize file này sau khi copy.

## 6. README.md

### Nội dung bắt buộc:

```markdown
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
   git clone git@github.com:dnsnamdang/hrm-claude-config.git

2. Chạy script link:
   cd hrm-claude-config
   ./setup.sh link <project-name> <đường-dẫn-project>

3. Verify — kiểm tra symlink đã tạo đúng:
   ls -la <đường-dẫn-project>/.claude
   ls -la <đường-dẫn-project>/CLAUDE.md

## Thêm project mới

1. Tạo folder mới trong repo: mkdir <ten-project>
2. Copy cấu trúc từ project có sẵn hoặc tự tạo
3. Chạy ./setup.sh link để kết nối

## Quy tắc

- Mỗi dev sửa config project mình phụ trách → commit vào folder tương ứng
- Commit message format: [project-name] mô tả thay đổi
- Không sửa config project khác khi chưa được đồng ý
```

## 7. Quy trình migrate config hiện có

Thứ tự thực hiện cho từng project:

1. Clone repo `hrm-claude-config` (nếu chưa có)
2. Tạo folder project trong repo: `mkdir nhatlinh`
3. **Copy** (không move) toàn bộ `.claude/`, `.plans/`, `docs/`, `CLAUDE.md`, `.gitignore` từ project thực tế vào folder trong repo
4. Rename `.gitignore` thành `.gitignore.project`
5. Commit & push
6. Quay lại project thực tế → xóa folder/file gốc
7. Chạy `./setup.sh link` để tạo symlink
8. Verify mọi thứ hoạt động bình thường

> **Lưu ý:** Bước 6-7 nên làm cẩn thận — backup trước khi xóa.

## 8. Edge cases

- **Project chưa có trong repo:** `setup.sh link` báo lỗi rõ ràng, gợi ý tạo folder trước
- **Đường dẫn project sai:** Báo lỗi, không tạo gì
- **Symlink bị broken** (target bị xóa/move): Dev cần chạy lại `setup.sh link`
- **Nhiều dev cùng sửa 1 project config:** Dùng Git flow bình thường (pull trước, resolve conflict nếu có)
- **settings.local.json:** Không track — mỗi dev có config local riêng
