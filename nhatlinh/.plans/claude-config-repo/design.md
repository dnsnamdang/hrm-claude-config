# Claude Config Repo — Design tóm tắt

> Spec chi tiết: `docs/superpowers/specs/2026-05-16-claude-config-repo-design.md`

## Mục tiêu
Gom config Claude Code (`.claude/`, `.plans/`, `docs/`, `CLAUDE.md`) của tất cả project vào 1 repo Git (`hrm-claude-config`) để backup, version control, và chia sẻ cho team.

## Cách tổ chức
- Mỗi project = 1 folder ở root của repo
- Config hoàn toàn riêng giữa các project (không có phần chung)
- Script `setup.sh` tạo symlink từ repo config vào project thực tế

## Scope
- `setup.sh` hỗ trợ: `link`, `new`, `status`
- `.gitignore` + `.gitignore.project` cho từng project
- `README.md` hướng dẫn team
- Quy trình migrate config hiện có

## Quyết định chính
- Symlink (không copy) để thay đổi ở repo config tự động apply vào project
- `.gitignore` được **copy** (không symlink) vì mỗi project có thể cần customize thêm
- Không dùng multi-branch — tất cả project trên `main`
