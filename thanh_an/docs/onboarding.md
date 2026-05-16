# Onboarding — Dùng Claude Code với dự án ThanhAn

## Setup lần đầu

```bash
# 1. Clone repo config (chứa CLAUDE.md, skills, plans, docs)
git clone https://github.com/dnsnamdang/thanhan-claude-config.git dns

# 2. Clone repo BE + FE vào trong folder dns
cd dns
git clone <url-repo-hrm-thanhan-api> hrm-thanhan-api
git clone <url-repo-hrm-thanhan-client> hrm-thanhan-client

# 3. Mở Claude Code từ folder dns
claude
```

Cấu trúc sau khi setup:
```
dns/                          ← repo config
├── CLAUDE.md
├── .skills/
├── .plans/
├── docs/
├── hrm-thanhan-api/                  ← repo BE (riêng)
└── hrm-thanhan-client/               ← repo FE (riêng)
```

## Đầu mỗi phiên làm việc

Yêu cầu Claude pull cả 3 repo:
```
pull code cả 3 repo
```

---

## Bước 1: Mở Claude Code từ đúng folder

- Luôn mở từ `dns/` (root) — KHÔNG mở từ `hrm-thanhan-api/` hay `hrm-thanhan-client/` riêng
- Khi mở từ root, Claude Code sẽ tự đọc CLAUDE.md và hiểu toàn bộ context dự án

## Bước 2: Không tạo CLAUDE.md riêng

- Dự án đã có CLAUDE.md chuẩn — dùng chung, không tạo thêm
- Không tự tạo `.skills/`, `docs/` riêng ngoài cấu trúc đã có
- Muốn sửa/thêm → tạo PR để team review

## Bước 3: Đọc tài liệu theo vai trò

| Vai trò | Đọc file |
|---------|----------|
| BE dev | `docs/shared.md` (Base classes, API pattern) + `docs/conventions.md` (phần Backend) |
| FE dev | `docs/shared.md` (Base components + Bootstrap-Vue, Vuex store) + `docs/conventions.md` (phần Frontend) |
| Fullstack | Đọc cả hai |

## Bước 4: Dùng skill có sẵn

Trước khi code pattern lặp lại → kiểm tra `.skills/` xem đã có SKILL.md chưa:

| Skill | Mô tả | File |
|-------|--------|------|
| list-page | Quy tắc permission + style cho màn danh sách | `.skills/list-page/SKILL.md` |

## Bước 5: Plan & wrap up

- Mỗi feature tạo `.plans/[feature]/plan.md` + `design.md`
- Ghi tên người phụ trách trong `.plans/STATUS.md` (format: `@username`)
- Wrap up cuối ngày hoặc cuối task: cập nhật plan.md → STATUS.md → design.md
- Đọc `.plans/STATUS.md` đầu session để biết ai đang làm gì

## Bước 6: Quy tắc commit config

| File/Folder | Ai quản lý | Cách sửa |
|-------------|-----------|----------|
| `CLAUDE.md` | Lead | Chỉ lead sửa |
| `.skills/` | Team | Tạo PR, cần review |
| `docs/` | Team | Tạo PR, cần review |
| `.plans/` | Người phụ trách feature | Tự cập nhật feature mình |