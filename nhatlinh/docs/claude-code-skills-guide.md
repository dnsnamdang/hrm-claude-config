# Hướng dẫn sử dụng Skills & Subagents trong Claude Code

**Dành cho: Team Dev ERP TPE**
**Phiên bản: 1.0 — Tháng 04/2026**

---

## Mục lục

1. Tổng quan kiến trúc
2. Khái niệm cơ bản
3. Custom Skills (`.skills/`)
4. Superpowers Skills (plugin)
5. Subagents
6. So sánh & Kết hợp
7. Workflow thực tế
8. Danh sách Skills hiện có
9. Hướng dẫn tạo Skill mới

---

## 1. Tổng quan kiến trúc

```
┌─────────────────────────────────────────────────┐
│                  Claude Code                     │
│                                                  │
│  ┌──────────────┐    ┌────────────────────────┐  │
│  │  CLAUDE.md   │    │  Superpowers Plugin    │  │
│  │  (project)   │    │  (~/.claude/plugins/)  │  │
│  └──────┬───────┘    └───────────┬────────────┘  │
│         │                        │               │
│         ▼                        ▼               │
│  ┌──────────────┐    ┌────────────────────────┐  │
│  │  .skills/    │    │  Superpowers Skills    │  │
│  │  (custom)    │    │  (built-in workflows)  │  │
│  └──────┬───────┘    └───────────┬────────────┘  │
│         │                        │               │
│         └────────┬───────────────┘               │
│                  ▼                                │
│         ┌────────────────┐                       │
│         │   Subagents    │                       │
│         │  (parallel     │                       │
│         │   execution)   │                       │
│         └────────────────┘                       │
└─────────────────────────────────────────────────┘
```

**3 lớp chính:**

- **CLAUDE.md** — Quy tắc project, mapping skills, session management
- **Custom Skills** (`.skills/`) — Checklist & hướng dẫn riêng cho project ERP TPE
- **Superpowers Skills** (plugin) — Workflow chuẩn: TDD, debugging, planning, code review...
- **Subagents** — Thực thi song song, không chiếm context của session chính

---

## 2. Khái niệm cơ bản

### Skill là gì?

Skill là file `SKILL.md` chứa hướng dẫn chi tiết cho Claude Code biết **cách thực hiện** một loại task cụ thể. Khi Claude nhận yêu cầu, nó đọc skill tương ứng rồi follow hướng dẫn bên trong.

**Ví dụ:** Khi bạn nói "tạo SRS cho feature X", Claude:
1. Quét `.skills/` → tìm thấy `srs-documenter/SKILL.md`
2. Đọc SKILL.md → biết template, quy trình, quy tắc
3. Thực hiện theo đúng hướng dẫn

### Subagent là gì?

Subagent là một **phiên Claude riêng biệt** được dispatch từ session chính để thực hiện task độc lập. Subagent có context riêng, không chiếm context của bạn.

**Ví dụ:** Bạn đang code feature A, muốn review code → dispatch subagent code-reviewer → subagent review song song → trả kết quả → bạn tiếp tục code.

### So sánh nhanh

| | Skill | Subagent |
|---|---|---|
| Là gì | File hướng dẫn (.md) | Phiên Claude riêng |
| Chạy ở đâu | Trong session hiện tại | Song song, tách biệt |
| Tốn context | Có (đọc vào context chính) | Không (context riêng) |
| Kết quả | Claude follow hướng dẫn trực tiếp | Trả message kết quả về |
| Tạo bởi | Team dev (`.skills/`) | Claude Code tự dispatch |

---

## 3. Custom Skills (`.skills/`)

### Vị trí

```
hrm/
├── .skills/
│   ├── api-documenter/SKILL.md
│   ├── bug-fixer/SKILL.md
│   ├── code-reviewer/SKILL.md
│   ├── export-excel/SKILL.md
│   ├── feature-scaffolder/SKILL.md
│   ├── import-excel/SKILL.md
│   ├── list-page/SKILL.md
│   ├── print-invoice/SKILL.md
│   └── srs-documenter/SKILL.md
```

### Cách hoạt động

1. **CLAUDE.md** chứa quy tắc: "Trước khi thực hiện task, quét `.skills/` → nếu match → đọc SKILL.md"
2. Claude nhận yêu cầu → match tên skill → đọc SKILL.md → follow hướng dẫn
3. SKILL.md chứa: mục đích, khi nào dùng, quy trình, template, quy tắc, checklist

### Cách gọi

```
# Tự động (Claude tự nhận diện)
"Tạo SRS cho feature notify-task-report"
→ Claude tự match → đọc .skills/srs-documenter/SKILL.md

# Chỉ định rõ
"Dùng skill bug-fixer để trace lỗi API 500 ở màn giao việc"
→ Claude đọc .skills/bug-fixer/SKILL.md
```

### Ưu điểm

- Tùy chỉnh 100% cho project
- Chứa conventions, checklist, template riêng
- Mọi dev trong team đều dùng chung chuẩn
- Dễ mở rộng: thêm thư mục + SKILL.md là xong

### Hạn chế

- Đọc vào context chính → tốn token
- Chỉ là hướng dẫn, không phải workflow tự động
- Phải maintain khi project thay đổi

---

## 4. Superpowers Skills (Plugin)

### Vị trí

```
~/.claude/plugins/cache/claude-plugins-official/superpowers/
└── skills/
    ├── brainstorming/
    ├── writing-plans/
    ├── executing-plans/
    ├── test-driven-development/
    ├── systematic-debugging/
    ├── requesting-code-review/
    ├── receiving-code-review/
    ├── subagent-driven-development/
    ├── dispatching-parallel-agents/
    ├── verification-before-completion/
    ├── finishing-a-development-branch/
    └── ...
```

### Cách hoạt động

- Là plugin cài sẵn trong Claude Code, không nằm trong repo project
- Cung cấp **workflow chuẩn** cho các hoạt động phát triển phần mềm
- Tự động trigger dựa trên context (VD: bắt đầu code → trigger brainstorming)
- Có thể gọi bằng tên: `superpowers:requesting-code-review`

### Danh sách Superpowers Skills chính

| Skill | Mục đích | Khi nào trigger |
|-------|----------|-----------------|
| `brainstorming` | Khám phá yêu cầu, phân tích trước khi code | Nhận yêu cầu feature mới |
| `writing-plans` | Lên kế hoạch implementation | Có spec/requirements |
| `executing-plans` | Thực thi plan từng bước | Có plan sẵn |
| `test-driven-development` | Viết test trước, code sau | Implement feature/bugfix |
| `systematic-debugging` | Debug có hệ thống | Gặp bug, test fail |
| `requesting-code-review` | Gọi reviewer kiểm tra code | Xong feature, trước merge |
| `receiving-code-review` | Xử lý feedback review | Nhận review feedback |
| `subagent-driven-development` | Chia task cho subagents song song | Nhiều task độc lập |
| `dispatching-parallel-agents` | Dispatch nhiều agent cùng lúc | 2+ task không phụ thuộc |
| `verification-before-completion` | Verify trước khi claim done | Sắp commit/merge |
| `finishing-a-development-branch` | Hoàn tất branch dev | Tests pass, sẵn sàng merge |

### Ưu điểm

- Workflow đã được thiết kế tối ưu
- Tự động trigger, không cần nhớ
- Dispatch subagents song song
- Cập nhật qua plugin, không cần maintain

### Hạn chế

- Generic, không biết conventions riêng của project
- Không tùy chỉnh được nội dung
- Phụ thuộc vào plugin version

---

## 5. Subagents

### Các loại Subagent

| Type | Mục đích | Tools có sẵn |
|------|----------|-------------|
| `Explore` | Tìm kiếm, đọc code, khám phá codebase | Read, Grep, Glob (read-only) |
| `Plan` | Thiết kế implementation plan | Read, Grep, Glob (read-only) |
| `general-purpose` | Task phức tạp, multi-step | Tất cả tools |
| `code-reviewer` | Review code theo plan & standards | Tất cả tools |

### Khi nào dùng Subagent

**Nên dùng:**
- 2+ task độc lập có thể chạy song song
- Task cần đọc nhiều file (tốn context) → delegate cho subagent
- Code review → subagent review, bạn tiếp tục code
- Explore codebase lớn → dispatch 2-3 Explore agents cùng lúc

**Không nên dùng:**
- Task đơn giản chỉ cần Grep/Read 1-2 file
- Task phụ thuộc kết quả của task trước
- Khi cần user input giữa chừng

### Ví dụ dispatch

```
# Dispatch 1 agent
"Dispatch Explore agent tìm tất cả API endpoints trong module Assign"

# Dispatch nhiều agent song song
"Dispatch 3 agent song song:
 1. Explore: tìm code BE liên quan đến feature X
 2. Explore: tìm code FE liên quan đến feature X  
 3. Plan: thiết kế implementation plan cho feature X"

# Dispatch code reviewer
"Dispatch code-reviewer: review commits từ abc123 đến def456 
 theo .skills/code-reviewer/SKILL.md"
```

---

## 6. So sánh & Kết hợp

### Bảng so sánh tổng hợp

| Tiêu chí | Custom Skill | Superpowers Skill | Subagent |
|----------|-------------|-------------------|----------|
| Nằm ở đâu | `.skills/` trong repo | `~/.claude/plugins/` | Runtime (tạm thời) |
| Tạo bởi | Team dev | Plugin superpowers | Claude tự dispatch |
| Tùy chỉnh | 100% | Không | Qua prompt |
| Scope | Project-specific | Generic | Per-task |
| Context | Đọc vào session chính | Đọc vào session chính | Context riêng biệt |
| Song song | Không | Có (dispatch subagent) | Có |
| Maintain | Team dev | Tự động (plugin update) | Không cần |

### Cách kết hợp hiệu quả

```
Superpowers Skill (QUY TRÌNH)
    │
    │  dispatch
    ▼
Subagent (THỰC THI song song)
    │
    │  đọc & follow
    ▼
Custom Skill (CHECKLIST project-specific)
```

**Ví dụ thực tế:**

```
1. Bạn: "Review code feature notify-task-report"

2. superpowers:requesting-code-review    ← QUY TRÌNH
   → Hướng dẫn lấy SHA, chuẩn bị context

3. Dispatch subagent code-reviewer       ← THỰC THI
   → Chạy song song, không chiếm context bạn

4. Subagent đọc .skills/code-reviewer    ← CHECKLIST
   → Biết check PHP 7.4, Vue 2, V2Base, N+1...

5. Subagent trả kết quả                 ← KẾT QUẢ
   → Critical: 0, Important: 2, Minor: 3
```

---

## 7. Workflow thực tế cho Team

### Flow phát triển feature mới

```
┌──────────────────────────────────────────────────┐
│  NHẬN YÊU CẦU                                    │
│  "Thêm tính năng X vào module Assign"            │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│  BRAINSTORMING                                    │
│  superpowers:brainstorming                        │
│  → Khám phá yêu cầu, hỏi user, phân tích        │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│  PLANNING                                         │
│  superpowers:writing-plans                        │
│  + .skills/feature-scaffolder (biết file cần tạo)│
│  → Tạo .plans/[feature]/plan.md + design.md      │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│  IMPLEMENT                                        │
│  superpowers:executing-plans                      │
│  + .skills/list-page, import-excel... (nếu match)│
│  → Code từng task, đánh [x] trong plan.md        │
│                                                   │
│  Gặp bug? → .skills/bug-fixer                    │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│  CODE REVIEW                                      │
│  superpowers:requesting-code-review (quy trình)   │
│  → dispatch subagent code-reviewer                │
│  → subagent đọc .skills/code-reviewer (checklist) │
│  → fix issues nếu có                              │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│  TÀI LIỆU (nếu cần)                             │
│  .skills/srs-documenter → SRS                     │
│  .skills/api-documenter → Tài liệu API mobile    │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────┐
│  MERGE                                            │
│  superpowers:verification-before-completion       │
│  superpowers:finishing-a-development-branch       │
│  → Push + Merge                                   │
└──────────────────────────────────────────────────┘
```

### Các lệnh thường dùng

| Muốn làm gì | Nói gì |
|---|---|
| Bắt đầu feature mới | "Tạo feature [tên] trong module [X]" |
| Fix bug | "Fix lỗi [mô tả], màn [tên]" |
| Tạo SRS | "Tạo SRS cho feature [tên]" |
| Tạo tài liệu API | "Tạo tài liệu API [feature] cho mobile" |
| Review code | "Review code feature [tên]" |
| Tạo màn danh sách | "Tạo màn danh sách [tên] trong module [X]" |
| Import Excel | "Thêm import Excel cho [entity]" |
| Scaffold feature | "Scaffold feature [tên] trong module [X]" |

---

## 8. Danh sách Skills hiện có trong project

### Custom Skills (`.skills/`)

| Skill | File | Mục đích |
|-------|------|----------|
| API Documenter | `.skills/api-documenter/SKILL.md` | Tạo tài liệu API cho mobile/team khác |
| Bug Fixer | `.skills/bug-fixer/SKILL.md` | Quy trình debug: trace log → fix đúng layer |
| Code Reviewer | `.skills/code-reviewer/SKILL.md` | Checklist review theo conventions ERP TPE |
| Export Excel | `.skills/export-excel/SKILL.md` | Pattern export Excel |
| Feature Scaffolder | `.skills/feature-scaffolder/SKILL.md` | Tạo bộ khung file cho feature mới |
| Import Excel | `.skills/import-excel/SKILL.md` | Pattern import Excel |
| List Page | `.skills/list-page/SKILL.md` | Quy tắc tạo màn danh sách + phân quyền |
| Print Invoice | `.skills/print-invoice/SKILL.md` | Pattern in phiếu/hóa đơn |
| SRS Documenter | `.skills/srs-documenter/SKILL.md` | Generate tài liệu SRS từ code/requirements |

---

## 9. Hướng dẫn tạo Skill mới

### Bước 1: Tạo thư mục

```bash
mkdir .skills/[ten-skill]
```

### Bước 2: Viết SKILL.md

```markdown
# [Tên Skill] — ERP TPE

## Mục đích
[Skill này giải quyết vấn đề gì?]

## Khi nào dùng
- [Điều kiện 1]
- [Điều kiện 2]

## Quy trình
### Bước 1: [...]
### Bước 2: [...]

## Template (nếu có)
[Template output]

## Quy tắc
- [Rule 1]
- [Rule 2]
```

### Bước 3: Tự động nhận diện

Skill sẽ được Claude tự nhận diện nhờ quy tắc trong CLAUDE.md:

> Trước khi thực hiện task, quét `.skills/` → nếu task khớp tên skill → đọc SKILL.md

### Bước 4: Tạo PR

Theo quy tắc team:
> `.skills/` là tài sản chung — sửa qua PR, không tự ý sửa.
> Muốn thêm skill mới → tạo PR với SKILL.md đầy đủ.

### Tips viết Skill hiệu quả

1. **Cụ thể cho project** — đừng viết generic, hãy ghi rõ file paths, patterns, conventions của ERP TPE
2. **Có template** — output mẫu giúp Claude generate đúng format
3. **Có checklist** — dễ verify kết quả
4. **Có quy tắc "Không được"** — tránh sai lầm phổ biến
5. **Tham chiếu docs khác** — link tới `docs/conventions.md`, `docs/shared.md` khi cần

---

*Tài liệu này được tạo bởi Claude Code cho team ERP TPE — Tháng 04/2026*
