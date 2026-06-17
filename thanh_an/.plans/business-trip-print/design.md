# Design tóm tắt — In QUYẾT ĐỊNH cử đi công tác (Business Trip)

**Người phụ trách:** @khoipv
**Ngày:** 2026-06-16

## Mục tiêu
Đổi trang in màn `timesheet/business_trip_assigns/:id/print` từ mẫu "GIẤY ĐI ĐƯỜNG" sang mẫu "QUYẾT ĐỊNH cử người lao động đi công tác" — copy layout từ `jobassignment/_id/print.vue`.

## Scope
- BE: thêm field `employee_account_id` vào `BusinessTripEmployeeResource` (để FE load tên công ty).
- FE: viết lại `<template>` + `<script>` của `business_trip_assigns/_id/print.vue`, giữ nguyên `<style>` (bổ sung class `.qd-header/.qd-footer`).

## Quyết định lớn
1. In **1 quyết định liệt kê tất cả nhân viên** (không in 1 trang/NV như cũ).
2. Tên công ty lấy qua `employee_account_id` → `human/employee/{id}` → `employeeConcurrentlyCompanies[0].name` (giống jobassignment).

## Map dữ liệu
| Mẫu jobassignment | Nguồn business_trip |
|---|---|
| `employees[]` | `data.business_trip_employees` |
| `tripPlaces` | `data.business_trip_assign.place` |
| `startTime`/`endTime` | `data.business_trip_assign.from_time`/`to_time` |
| `companyName` | load qua `employee_account_id` |

## Link chi tiết
- Spec: `docs/superpowers/specs/2026-06-16-business-trip-print-design.md`
- Plan chi tiết: `docs/superpowers/plans/2026-06-16-business-trip-print.md`
