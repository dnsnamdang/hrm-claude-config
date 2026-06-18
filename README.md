# HRM Claude Config

Repo lưu trữ config [Claude Code](https://claude.ai/claude-code) cho các project của team DNS.

Config bao gồm: `CLAUDE.md`, `.claude/` (skills, commands, settings), `.plans/` (kế hoạch feature), `docs/` (tài liệu convention, shared, onboarding).

---

## Danh sách project

| Project | Mô tả | Folder trong repo |
|---------|-------|-------------------|
| ERP TPE | ERP Tân Phát (Laravel + AngularJS, repo `TanPhatDev`) | `erp/` |
| HRM gốc | Project HRM chính (TPE) | `hrm/` |
| Nhất Linh | HRM cho công ty Nhất Linh | `nhatlinh/` |
| Thành An | HRM cho công ty Thành An | `thanh_an/` |

> **ERP + HRM thường được mở chung trong 1 workspace `ERP-HRM/`** — xem [Setup workspace ERP-HRM](#setup-workspace-erp-hrm-gộp-erp--hrm-trong-1-cửa-sổ-claude) bên dưới.

---

## Hướng dẫn setup (cho dev mới)

### Bước 1: Clone repo config về máy

```bash
cd ~/Desktop/dns
git clone git@github.com:dnsnamdang/hrm-claude-config.git
```

Sau khi clone xong, bạn sẽ có folder `hrm-claude-config/` chứa config của tất cả project.

### Bước 2: Kết nối config vào project của bạn

Giả sử bạn đang làm project **nhatlinh** và project nằm ở `~/Desktop/dns/nhatlinh`:

```bash
cd ~/Desktop/dns/hrm-claude-config
./setup.sh link nhatlinh ~/Desktop/dns/nhatlinh
```

Script sẽ tạo symlink từ repo config vào project:

```
nhatlinh/.claude   → hrm-claude-config/nhatlinh/.claude
nhatlinh/.plans    → hrm-claude-config/nhatlinh/.plans
nhatlinh/docs      → hrm-claude-config/nhatlinh/docs
nhatlinh/CLAUDE.md → hrm-claude-config/nhatlinh/CLAUDE.md
```

### Bước 3: Kiểm tra symlink đã tạo đúng

```bash
ls -la ~/Desktop/dns/nhatlinh/.claude
# Output mong đợi: .claude -> /Users/.../hrm-claude-config/nhatlinh/.claude

ls -la ~/Desktop/dns/nhatlinh/CLAUDE.md
# Output mong đợi: CLAUDE.md -> /Users/.../hrm-claude-config/nhatlinh/CLAUDE.md

# Thử đọc file
head -5 ~/Desktop/dns/nhatlinh/CLAUDE.md
```

### Bước 4: Mở Claude Code và kiểm tra

```bash
cd ~/Desktop/dns/nhatlinh
claude
```

Claude Code sẽ tự động đọc `CLAUDE.md` và `.claude/skills/` qua symlink — không cần config gì thêm.

---

## Setup workspace ERP-HRM (gộp ERP + HRM trong 1 cửa sổ Claude)

Đây là cách setup **giống máy đang dùng**: ERP và HRM nằm trong **một workspace `ERP-HRM/`** để mở chung 1 phiên Claude Code, mỗi project con vẫn dùng config riêng (`erp/`, `hrm/`) trong repo này qua symlink.

### Cấu trúc đích

```
~/DEV/code/
├── hrm-claude-config/         ← repo này (clone song song, KHÔNG nằm trong ERP-HRM)
│   ├── erp/   hrm/  ...        ← config từng project
│   └── setup.sh  README.md
│
└── ERP-HRM/                   ← workspace mở Claude ở đây
    ├── CLAUDE.md              ← FILE THẬT (không symlink) — trỏ sang 2 project con
    ├── ERP/                   ← repo ERP (chứa TanPhatDev/)
    │   ├── .claude   → hrm-claude-config/erp/.claude
    │   ├── .plans    → hrm-claude-config/erp/.plans
    │   ├── docs      → hrm-claude-config/erp/docs
    │   ├── CLAUDE.md → hrm-claude-config/erp/CLAUDE.md
    │   ├── .gitignore→ hrm-claude-config/erp/.gitignore
    │   └── TanPhatDev/         ← source code Laravel thật
    └── HRM/                   ← repo HRM (chứa hrm-api/, hrm-client/)
        ├── .claude   → hrm-claude-config/hrm/.claude
        ├── .plans    → hrm-claude-config/hrm/.plans
        ├── docs      → hrm-claude-config/hrm/docs
        ├── CLAUDE.md → hrm-claude-config/hrm/CLAUDE.md
        ├── .gitignore→ hrm-claude-config/hrm/.gitignore
        ├── hrm-api/            ← source code BE thật
        └── hrm-client/         ← source code FE thật
```

> Symlink luôn là **5 item**: `.claude`, `.plans`, `docs`, `CLAUDE.md`, `.gitignore` (khai báo trong `setup.sh` → `SYMLINK_ITEMS`).

### Các bước

```bash
# 0. Vào thư mục gốc chứa code (tùy máy, ví dụ ~/DEV/code)
cd ~/DEV/code

# 1. Clone repo config (song song, KHÔNG đặt trong ERP-HRM)
git clone git@github.com:dnsnamdang/hrm-claude-config.git

# 2. Tạo workspace + clone 2 project con vào trong
mkdir -p ERP-HRM
git clone <git-repo-ERP> ERP-HRM/ERP     # repo ERP (bên trong có TanPhatDev/)
git clone <git-repo-HRM> ERP-HRM/HRM     # repo HRM (bên trong có hrm-api/, hrm-client/)

# 3. Tạo CLAUDE.md gốc của workspace (FILE THẬT, không symlink)
cat > ERP-HRM/CLAUDE.md << 'EOF'
# ERP-HRM Workspace

Workspace chứa 2 dự án. Luôn đọc và tuân thủ CLAUDE.md của cả 2 project:

@ERP/CLAUDE.md
@HRM/CLAUDE.md

## Quy tắc quan trọng — Scope thư mục

- Khi làm việc cho dự án **HRM** → mọi thao tác (tạo file, đọc file, git) thực hiện trong `HRM/`
- Khi làm việc cho dự án **ERP** → mọi thao tác (tạo file, đọc file, git) thực hiện trong `ERP/`
- KHÔNG tạo file code, `.plans/`, `docs/` ở thư mục root `ERP-HRM/`
- Đường dẫn tương đối trong mỗi CLAUDE.md con đều tính từ thư mục chứa nó, không phải từ root
EOF

# 4. Link config vào từng project con
cd ~/DEV/code/hrm-claude-config
./setup.sh link erp ~/DEV/code/ERP-HRM/ERP
./setup.sh link hrm ~/DEV/code/ERP-HRM/HRM

# 5. Verify symlink
ls -la ~/DEV/code/ERP-HRM/ERP   | grep '\->'
ls -la ~/DEV/code/ERP-HRM/HRM   | grep '\->'

# 6. Mở Claude tại workspace (đọc cả 3 CLAUDE.md: root + ERP + HRM)
cd ~/DEV/code/ERP-HRM
claude
```

### Lưu ý quan trọng

- **`ERP-HRM/CLAUDE.md` là file thật**, KHÔNG link từ repo config. Nó chỉ `@ERP/CLAUDE.md` + `@HRM/CLAUDE.md` để Claude nạp cả 2 khi mở ở root.
- **`ERP-HRM/CLAUDE.md` không được commit vào source ERP/HRM** (nó nằm ở thư mục cha workspace, ngoài 2 repo).
- Mỗi project con tự là 1 git repo riêng → thao tác git luôn `cd` vào đúng `ERP/` hoặc `HRM/`.
- Config (`.claude/.plans/docs/CLAUDE.md`) sửa ở project nào → tự phản ánh vào `hrm-claude-config/erp` hoặc `/hrm`; commit trong repo config (xem [Cập nhật config](#cập-nhật-config-workflow-hàng-ngày)).

---

## Các lệnh của setup.sh

### `./setup.sh link <project> <path>` — Kết nối config vào project

```bash
# Ví dụ 1: Link config cho project HRM
./setup.sh link hrm ~/Desktop/dns/HRM

# Ví dụ 2: Link config cho project thanh_an
./setup.sh link thanh_an ~/Desktop/dns/thanh_an

# Ví dụ 3: Link config cho project nhatlinh
./setup.sh link nhatlinh ~/Desktop/dns/nhatlinh
```

**Xử lý khi project đã có config sẵn:**
- Nếu target chưa có → tạo symlink luôn
- Nếu target đã là symlink → thay symlink mới
- Nếu target đã có file/folder thật → hỏi bạn muốn backup rồi thay, hay giữ nguyên

### `./setup.sh new <project>` — Tạo config cho project mới

```bash
# Ví dụ: Tạo config cho project mới tên "abc-corp"
./setup.sh new abc-corp
```

Script sẽ tạo cấu trúc mẫu:
```
abc-corp/
├── .claude/
│   ├── skills/
│   ├── commands/
│   └── settings.json
├── .plans/
│   └── STATUS.md
├── docs/
├── CLAUDE.md              ← placeholder, cần cập nhật
└── .gitignore.project     ← sẽ được copy thành .gitignore khi link
```

Sau đó bạn cần:
1. Cập nhật `CLAUDE.md` với hướng dẫn riêng cho project
2. Thêm skills nếu cần
3. Link vào project: `./setup.sh link abc-corp ~/Desktop/dns/abc-corp`
4. Commit: `git add abc-corp/ && git commit -m "[abc-corp] init config"`

### `./setup.sh status` — Xem tổng quan tất cả project

```bash
./setup.sh status
```

Output mẫu:
```
=== HRM Claude Config ===

  hrm                  238 files  CLAUDE.md:✓  .plans:✓  docs:✓
  nhatlinh              60 files  CLAUDE.md:✓  .plans:✓  docs:✓
  thanh_an              48 files  CLAUDE.md:✓  .plans:✓  docs:✓

Tổng: 3 project
```

---

## Cập nhật config (workflow hàng ngày)

### Khi bạn sửa config trong quá trình làm việc

Vì dùng symlink, mọi thay đổi bạn làm trong project (ví dụ thêm skill, cập nhật plan) sẽ **tự động phản ánh** vào repo config. Bạn chỉ cần commit:

```bash
cd ~/Desktop/dns/hrm-claude-config

# Xem có gì thay đổi
git status

# Commit thay đổi
git add nhatlinh/
git commit -m "[nhatlinh] thêm skill import-excel"
git push
```

### Khi muốn pull config mới nhất từ team

```bash
cd ~/Desktop/dns/hrm-claude-config
git pull
```

Vì dùng symlink, project của bạn sẽ tự động có config mới nhất — không cần chạy lại `setup.sh link`.

---

## Thêm project mới (đầy đủ từ A-Z)

Giả sử team nhận project mới tên **"vinh-phat"**:

```bash
# 1. Vào repo config
cd ~/Desktop/dns/hrm-claude-config

# 2. Tạo cấu trúc config mới
./setup.sh new vinh-phat

# 3. Cập nhật CLAUDE.md cho project (mở bằng editor)
#    Sửa file: hrm-claude-config/vinh-phat/CLAUDE.md

# 4. Commit
git add vinh-phat/
git commit -m "[vinh-phat] init config"
git push

# 5. Link vào project thực tế (giả sử project nằm ở ~/Desktop/dns/vinh-phat)
./setup.sh link vinh-phat ~/Desktop/dns/vinh-phat

# 6. Verify
ls -la ~/Desktop/dns/vinh-phat/.claude
ls -la ~/Desktop/dns/vinh-phat/CLAUDE.md
```

---

## Cấu trúc repo

```
hrm-claude-config/
├── README.md           ← file này
├── setup.sh            ← script quản lý
├── .gitignore          ← ignore chung cho repo
│
├── erp/                ← config cho project ERP TPE (TanPhatDev)
│   ├── .claude/
│   │   ├── skills/     ← custom skills
│   │   ├── commands/
│   │   └── settings.json
│   ├── .plans/         ← kế hoạch feature (STATUS.md + từng feature/)
│   ├── docs/
│   ├── CLAUDE.md
│   └── .gitignore
│
├── hrm/                ← config cho project HRM gốc
│   ├── .claude/
│   │   ├── skills/     ← custom skills (button-convention, list-page, ...)
│   │   ├── commands/   ← custom slash commands
│   │   └── settings.json
│   ├── .plans/         ← kế hoạch feature (STATUS.md + từng feature/)
│   ├── docs/           ← conventions.md, shared.md, onboarding.md, ...
│   ├── CLAUDE.md       ← hướng dẫn chính cho AI
│   └── .gitignore
│
├── nhatlinh/           ← config cho project Nhất Linh
│   └── (cấu trúc tương tự)
│
└── thanh_an/           ← config cho project Thành An
    └── (cấu trúc tương tự)
```

---

## Quy tắc team

1. **Mỗi dev sửa config project mình phụ trách** → commit vào folder tương ứng
2. **Commit message format:** `[project-name] mô tả thay đổi`
   - Ví dụ: `[nhatlinh] thêm skill import-excel`
   - Ví dụ: `[hrm] cập nhật conventions.md`
   - Ví dụ: `[repo] sửa setup.sh`
3. **Không sửa config project khác** khi chưa được đồng ý
4. **Pull trước khi push** để tránh conflict:
   ```bash
   git pull --rebase
   git push
   ```
5. **Không commit** file `settings.local.json` (đã ignore sẵn) — đây là config cá nhân

---

## Troubleshooting

### Symlink bị broken (Claude Code báo không tìm thấy CLAUDE.md)

```bash
# Kiểm tra symlink
ls -la ~/Desktop/dns/nhatlinh/CLAUDE.md

# Nếu broken → chạy lại link
cd ~/Desktop/dns/hrm-claude-config
./setup.sh link nhatlinh ~/Desktop/dns/nhatlinh
```

### Muốn ngắt kết nối (không dùng symlink nữa)

```bash
# Xóa symlink và copy file thật về
cd ~/Desktop/dns/nhatlinh
rm .claude .plans docs CLAUDE.md    # xóa symlink
cp -R ~/Desktop/dns/hrm-claude-config/nhatlinh/.claude .
cp -R ~/Desktop/dns/hrm-claude-config/nhatlinh/.plans .
cp -R ~/Desktop/dns/hrm-claude-config/nhatlinh/docs .
cp ~/Desktop/dns/hrm-claude-config/nhatlinh/CLAUDE.md .
```

### Conflict khi pull

```bash
cd ~/Desktop/dns/hrm-claude-config
git pull --rebase
# Nếu conflict → resolve như bình thường
git add .
git rebase --continue
```
