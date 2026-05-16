# Claude Config Repo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tổ chức 1 repo Git (`hrm-claude-config`) chứa config Claude Code cho tất cả project, với script symlink tự động.

**Architecture:** Mỗi project = 1 folder ở root. Script `setup.sh` (bash) hỗ trợ 3 lệnh: `link`, `new`, `status`. Dev clone repo → chạy script → symlink vào project thực tế.

**Tech Stack:** Bash script, Git

---

## Task 1: Clone repo và tạo cấu trúc cơ bản

**Files:**
- Create: `hrm-claude-config/.gitignore`
- Create: `hrm-claude-config/README.md`

- [ ] **Step 1: Clone repo**

```bash
cd /Users/manhcuong/Desktop/dns
git clone git@github.com:dnsnamdang/hrm-claude-config.git
cd hrm-claude-config
```

- [ ] **Step 2: Tạo file `.gitignore`**

Tạo file `/Users/manhcuong/Desktop/dns/hrm-claude-config/.gitignore`:

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

- [ ] **Step 3: Tạo file `README.md`**

Tạo file `/Users/manhcuong/Desktop/dns/hrm-claude-config/README.md`:

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
```

- [ ] **Step 4: Commit**

```bash
cd /Users/manhcuong/Desktop/dns/hrm-claude-config
git add .gitignore README.md
git commit -m "[repo] init repo structure — .gitignore + README"
```

---

## Task 2: Viết script `setup.sh`

**Files:**
- Create: `hrm-claude-config/setup.sh`

- [ ] **Step 1: Tạo file `setup.sh`**

Tạo file `/Users/manhcuong/Desktop/dns/hrm-claude-config/setup.sh`:

```bash
#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SYMLINK_ITEMS=(".claude" ".plans" "docs" "CLAUDE.md")

usage() {
    echo "Usage:"
    echo "  $0 link <project-name> <target-path>   Tạo symlink config vào project"
    echo "  $0 new <project-name>                   Tạo config mới cho project"
    echo "  $0 status                               Xem tổng quan tất cả project"
    echo ""
    echo "Ví dụ:"
    echo "  $0 link nhatlinh /Users/manhcuong/Desktop/dns/nhatlinh"
    echo "  $0 new my-new-project"
}

ask_overwrite() {
    local target="$1"
    echo -e "${YELLOW}[!] '$target' đã tồn tại và không phải symlink.${NC}"
    read -p "    Overwrite (backup cũ rồi tạo symlink)? [y/N] " answer
    case "$answer" in
        [yY]) return 0 ;;
        *) return 1 ;;
    esac
}

do_link() {
    local project="$1"
    local target_path="$2"
    local project_dir="$SCRIPT_DIR/$project"

    if [ ! -d "$project_dir" ]; then
        echo -e "${RED}[ERROR] Folder '$project' không tồn tại trong repo.${NC}"
        echo "Các project hiện có:"
        ls -d "$SCRIPT_DIR"/*/  2>/dev/null | xargs -I{} basename {} | grep -v '^\.' | sed 's/^/  - /'
        echo ""
        echo "Tạo mới bằng: $0 new $project"
        exit 1
    fi

    if [ ! -d "$target_path" ]; then
        echo -e "${RED}[ERROR] Đường dẫn '$target_path' không tồn tại.${NC}"
        exit 1
    fi

    echo "Linking config '$project' → '$target_path'"
    echo "---"

    for item in "${SYMLINK_ITEMS[@]}"; do
        local source="$project_dir/$item"
        local target="$target_path/$item"

        if [ ! -e "$source" ]; then
            echo -e "${YELLOW}[SKIP] '$project/$item' không tồn tại trong repo config.${NC}"
            continue
        fi

        if [ -L "$target" ]; then
            rm "$target"
            ln -s "$source" "$target"
            echo -e "${GREEN}[OK] $item → symlink (đã thay symlink cũ)${NC}"
        elif [ -e "$target" ]; then
            if ask_overwrite "$item"; then
                local backup="${target}.backup.$(date +%Y%m%d%H%M%S)"
                mv "$target" "$backup"
                ln -s "$source" "$target"
                echo -e "${GREEN}[OK] $item → symlink (backup: $(basename "$backup"))${NC}"
            else
                echo -e "${YELLOW}[SKIP] $item — giữ nguyên${NC}"
            fi
        else
            ln -s "$source" "$target"
            echo -e "${GREEN}[OK] $item → symlink${NC}"
        fi
    done

    # .gitignore.project → copy thành .gitignore
    local gitignore_src="$project_dir/.gitignore.project"
    local gitignore_target="$target_path/.gitignore"

    if [ -f "$gitignore_src" ]; then
        if [ -f "$gitignore_target" ] && [ ! -L "$gitignore_target" ]; then
            if ask_overwrite ".gitignore"; then
                local backup="${gitignore_target}.backup.$(date +%Y%m%d%H%M%S)"
                cp "$gitignore_target" "$backup"
                cp "$gitignore_src" "$gitignore_target"
                echo -e "${GREEN}[OK] .gitignore → copy (backup: $(basename "$backup"))${NC}"
            else
                echo -e "${YELLOW}[SKIP] .gitignore — giữ nguyên${NC}"
            fi
        else
            cp "$gitignore_src" "$gitignore_target"
            echo -e "${GREEN}[OK] .gitignore → copy${NC}"
        fi
    fi

    echo "---"
    echo -e "${GREEN}Done!${NC}"
}

do_new() {
    local project="$1"
    local project_dir="$SCRIPT_DIR/$project"

    if [ -d "$project_dir" ]; then
        echo -e "${RED}[ERROR] Folder '$project' đã tồn tại.${NC}"
        exit 1
    fi

    mkdir -p "$project_dir/.claude/skills"
    mkdir -p "$project_dir/.claude/commands"
    mkdir -p "$project_dir/.plans"
    mkdir -p "$project_dir/docs"

    cat > "$project_dir/.claude/settings.json" << 'SETTINGS_EOF'
{}
SETTINGS_EOF

    cat > "$project_dir/.plans/STATUS.md" << 'STATUS_EOF'
# STATUS.md

## Đang làm

(none)

## Đã làm

(none)
STATUS_EOF

    cat > "$project_dir/CLAUDE.md" << 'CLAUDE_EOF'
# Project — Hướng dẫn cho AI

(Cập nhật hướng dẫn cho project tại đây)
CLAUDE_EOF

    cat > "$project_dir/.gitignore.project" << 'GI_EOF'
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
GI_EOF

    echo -e "${GREEN}Đã tạo config cho project '$project'.${NC}"
    echo "Cấu trúc:"
    find "$project_dir" -not -path '*/\.*' -o -name '.claude' -o -name '.plans' -o -name '.gitignore.project' | head -20 | sed "s|$SCRIPT_DIR/||"
    echo ""
    echo "Bước tiếp theo:"
    echo "  $0 link $project <đường-dẫn-project>"
}

do_status() {
    echo "=== HRM Claude Config ==="
    echo ""

    local count=0
    for dir in "$SCRIPT_DIR"/*/; do
        local name=$(basename "$dir")
        [[ "$name" == "." || "$name" == ".." ]] && continue

        local files=$(find "$dir" -type f | wc -l | tr -d ' ')
        local has_claude="✗"
        local has_plans="✗"
        local has_docs="✗"

        [ -f "$dir/CLAUDE.md" ] && has_claude="✓"
        [ -d "$dir/.plans" ] && has_plans="✓"
        [ -d "$dir/docs" ] && has_docs="✓"

        printf "  %-20s %3s files  CLAUDE.md:%s  .plans:%s  docs:%s\n" \
            "$name" "$files" "$has_claude" "$has_plans" "$has_docs"
        count=$((count + 1))
    done

    echo ""
    echo "Tổng: $count project"
}

# --- Main ---

if [ $# -eq 0 ]; then
    usage
    exit 1
fi

command="$1"
shift

case "$command" in
    link)
        if [ $# -lt 2 ]; then
            echo -e "${RED}[ERROR] Thiếu tham số.${NC}"
            echo "Usage: $0 link <project-name> <target-path>"
            exit 1
        fi
        do_link "$1" "$2"
        ;;
    new)
        if [ $# -lt 1 ]; then
            echo -e "${RED}[ERROR] Thiếu tên project.${NC}"
            echo "Usage: $0 new <project-name>"
            exit 1
        fi
        do_new "$1"
        ;;
    status)
        do_status
        ;;
    *)
        echo -e "${RED}[ERROR] Lệnh '$command' không hợp lệ.${NC}"
        usage
        exit 1
        ;;
esac
```

- [ ] **Step 2: Chmod executable**

```bash
chmod +x /Users/manhcuong/Desktop/dns/hrm-claude-config/setup.sh
```

- [ ] **Step 3: Test script hiển thị usage**

```bash
cd /Users/manhcuong/Desktop/dns/hrm-claude-config
./setup.sh
```

Expected: In ra usage guide, exit code 1.

- [ ] **Step 4: Commit**

```bash
cd /Users/manhcuong/Desktop/dns/hrm-claude-config
git add setup.sh
git commit -m "[repo] add setup.sh — link, new, status commands"
```

---

## Task 3: Migrate config project nhatlinh

**Files:**
- Copy from: `/Users/manhcuong/Desktop/dns/nhatlinh/.claude/`, `.plans/`, `docs/`, `CLAUDE.md`, `.gitignore`
- Create: `hrm-claude-config/nhatlinh/`

- [ ] **Step 1: Tạo folder và copy config**

```bash
cd /Users/manhcuong/Desktop/dns/hrm-claude-config
mkdir -p nhatlinh

# Copy toàn bộ config (giữ nguyên cấu trúc)
cp -R /Users/manhcuong/Desktop/dns/nhatlinh/.claude nhatlinh/.claude
cp -R /Users/manhcuong/Desktop/dns/nhatlinh/.plans nhatlinh/.plans
cp -R /Users/manhcuong/Desktop/dns/nhatlinh/docs nhatlinh/docs
cp /Users/manhcuong/Desktop/dns/nhatlinh/CLAUDE.md nhatlinh/CLAUDE.md
```

- [ ] **Step 2: Tạo `.gitignore.project` từ `.gitignore` hiện có**

```bash
cp /Users/manhcuong/Desktop/dns/nhatlinh/.gitignore /Users/manhcuong/Desktop/dns/hrm-claude-config/nhatlinh/.gitignore.project
```

- [ ] **Step 3: Xóa `settings.local.json` nếu bị copy theo**

```bash
rm -f /Users/manhcuong/Desktop/dns/hrm-claude-config/nhatlinh/.claude/settings.local.json
```

- [ ] **Step 4: Verify cấu trúc**

```bash
find /Users/manhcuong/Desktop/dns/hrm-claude-config/nhatlinh -maxdepth 2 -not -name '.DS_Store' | head -30
```

Expected: Thấy `.claude/`, `.plans/`, `docs/`, `CLAUDE.md`, `.gitignore.project`

- [ ] **Step 5: Commit**

```bash
cd /Users/manhcuong/Desktop/dns/hrm-claude-config
git add nhatlinh/
git commit -m "[nhatlinh] migrate config — .claude, .plans, docs, CLAUDE.md"
```

---

## Task 4: Migrate config project HRM

**Files:**
- Copy from: `/Users/manhcuong/Desktop/dns/HRM/.claude/`, `.plans/`, `docs/`, `CLAUDE.md`, `.gitignore`
- Create: `hrm-claude-config/hrm/`

- [ ] **Step 1: Tạo folder và copy config**

```bash
cd /Users/manhcuong/Desktop/dns/hrm-claude-config
mkdir -p hrm

cp -R /Users/manhcuong/Desktop/dns/HRM/.claude hrm/.claude
cp -R /Users/manhcuong/Desktop/dns/HRM/.plans hrm/.plans
cp -R /Users/manhcuong/Desktop/dns/HRM/docs hrm/docs
cp /Users/manhcuong/Desktop/dns/HRM/CLAUDE.md hrm/CLAUDE.md
```

- [ ] **Step 2: Tạo `.gitignore.project`**

```bash
cp /Users/manhcuong/Desktop/dns/HRM/.gitignore /Users/manhcuong/Desktop/dns/hrm-claude-config/hrm/.gitignore.project
```

- [ ] **Step 3: Xóa `settings.local.json` nếu bị copy theo**

```bash
rm -f /Users/manhcuong/Desktop/dns/hrm-claude-config/hrm/.claude/settings.local.json
```

- [ ] **Step 4: Verify cấu trúc**

```bash
find /Users/manhcuong/Desktop/dns/hrm-claude-config/hrm -maxdepth 2 -not -name '.DS_Store' | head -30
```

- [ ] **Step 5: Commit**

```bash
cd /Users/manhcuong/Desktop/dns/hrm-claude-config
git add hrm/
git commit -m "[hrm] migrate config — .claude, .plans, docs, CLAUDE.md"
```

---

## Task 5: Migrate config project thanh_an

> **Lưu ý:** thanh_an dùng `.skills/` (ngoài `.claude/`) — cần copy cả folder này. Ngoài ra thanh_an không có `.claude/skills/` mà dùng `.skills/` ở root.

**Files:**
- Copy from: `/Users/manhcuong/Desktop/dns/thanh_an/.plans/`, `.skills/`, `docs/`, `CLAUDE.md`, `.gitignore`
- Create: `hrm-claude-config/thanh_an/`

- [ ] **Step 1: Tạo folder và copy config**

```bash
cd /Users/manhcuong/Desktop/dns/hrm-claude-config
mkdir -p thanh_an

# thanh_an không có .claude/ dạng chuẩn, nhưng có thể có → kiểm tra
if [ -d /Users/manhcuong/Desktop/dns/thanh_an/.claude ]; then
    cp -R /Users/manhcuong/Desktop/dns/thanh_an/.claude thanh_an/.claude
fi

# Copy .skills/ (đặc biệt của thanh_an)
if [ -d /Users/manhcuong/Desktop/dns/thanh_an/.skills ]; then
    cp -R /Users/manhcuong/Desktop/dns/thanh_an/.skills thanh_an/.skills
fi

cp -R /Users/manhcuong/Desktop/dns/thanh_an/.plans thanh_an/.plans
cp -R /Users/manhcuong/Desktop/dns/thanh_an/docs thanh_an/docs
cp /Users/manhcuong/Desktop/dns/thanh_an/CLAUDE.md thanh_an/CLAUDE.md
```

- [ ] **Step 2: Tạo `.gitignore.project`**

```bash
cp /Users/manhcuong/Desktop/dns/thanh_an/.gitignore /Users/manhcuong/Desktop/dns/hrm-claude-config/thanh_an/.gitignore.project
```

- [ ] **Step 3: Xóa `settings.local.json` nếu bị copy theo**

```bash
rm -f /Users/manhcuong/Desktop/dns/hrm-claude-config/thanh_an/.claude/settings.local.json
```

- [ ] **Step 4: Verify cấu trúc**

```bash
find /Users/manhcuong/Desktop/dns/hrm-claude-config/thanh_an -maxdepth 2 -not -name '.DS_Store' | head -30
```

- [ ] **Step 5: Commit**

```bash
cd /Users/manhcuong/Desktop/dns/hrm-claude-config
git add thanh_an/
git commit -m "[thanh_an] migrate config — .plans, .skills, docs, CLAUDE.md"
```

---

## Task 6: Test symlink cho project nhatlinh

- [ ] **Step 1: Xóa config gốc ở project nhatlinh (backup trước)**

```bash
cd /Users/manhcuong/Desktop/dns/nhatlinh

# Backup
mkdir -p /tmp/nhatlinh-config-backup
cp -R .claude /tmp/nhatlinh-config-backup/.claude
cp -R .plans /tmp/nhatlinh-config-backup/.plans
cp -R docs /tmp/nhatlinh-config-backup/docs
cp CLAUDE.md /tmp/nhatlinh-config-backup/CLAUDE.md
cp .gitignore /tmp/nhatlinh-config-backup/.gitignore

# Xóa gốc
rm -rf .claude .plans docs CLAUDE.md
```

- [ ] **Step 2: Chạy `setup.sh link`**

```bash
cd /Users/manhcuong/Desktop/dns/hrm-claude-config
./setup.sh link nhatlinh /Users/manhcuong/Desktop/dns/nhatlinh
```

Expected: Tất cả item hiện `[OK]`.

- [ ] **Step 3: Verify symlink**

```bash
ls -la /Users/manhcuong/Desktop/dns/nhatlinh/.claude
ls -la /Users/manhcuong/Desktop/dns/nhatlinh/.plans
ls -la /Users/manhcuong/Desktop/dns/nhatlinh/docs
ls -la /Users/manhcuong/Desktop/dns/nhatlinh/CLAUDE.md
```

Expected: Tất cả đều là symlink trỏ về `hrm-claude-config/nhatlinh/...`

- [ ] **Step 4: Verify nội dung vẫn đọc được**

```bash
head -5 /Users/manhcuong/Desktop/dns/nhatlinh/CLAUDE.md
ls /Users/manhcuong/Desktop/dns/nhatlinh/.claude/skills/
```

Expected: Nội dung CLAUDE.md hiển thị bình thường, skills liệt kê đúng.

- [ ] **Step 5: Test `status`**

```bash
cd /Users/manhcuong/Desktop/dns/hrm-claude-config
./setup.sh status
```

Expected: Hiển thị 3 project (nhatlinh, hrm, thanh_an) với thông tin file.

---

## Task 7: Push lên remote

- [ ] **Step 1: Push**

```bash
cd /Users/manhcuong/Desktop/dns/hrm-claude-config
git push origin main
```

> Nếu branch mặc định là `master`, đổi thành `git push origin master`.

---

### Checkpoint — sau Task 7
Vừa hoàn thành: Repo config đã setup xong, 3 project đã migrate, symlink nhatlinh đã test.
Đang làm dở: (không)
Bước tiếp theo: Migrate symlink cho HRM và thanh_an nếu cần (tương tự Task 6).
Blocked: (không)
