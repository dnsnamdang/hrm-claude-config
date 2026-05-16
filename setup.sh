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
