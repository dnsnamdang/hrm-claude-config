# Sắp xếp options Giai đoạn dự án theo tên

- [x] BE: `ProjectPhaseService::getAll()` đổi `orderBy('id','asc')` → `orderBy('name','asc')` (nguồn duy nhất của mọi select giai đoạn qua `optionsSelect/fetchProjectPhases`)
