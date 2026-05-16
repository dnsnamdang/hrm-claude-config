# Optimize getAll API khi tạo Task/Issue từ màn Manager

**Mục tiêu:** Khi tạo task/issue từ màn manager (giải pháp/hạng mục/dự án), chỉ load bản ghi tương ứng thay vì toàn bộ danh sách.

**Phương án:** FE truyền `id` param → BE filter `where('id', $request->id)`. Lock select trong modal.

**Scope:** 2 BE service + 2 FE modal + vài file gọi modal từ manager.

**Spec chi tiết:** `docs/superpowers/specs/2026-05-11-optimize-getall-manager-context-design.md`
