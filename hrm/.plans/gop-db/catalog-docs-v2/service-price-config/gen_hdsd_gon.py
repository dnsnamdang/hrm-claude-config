# -*- coding: utf-8 -*-
"""HDSD Cập nhật nhanh giá dịch vụ — bản GỌN (skill hdsd-documenter, 29/09/2026). Chạy: python3 gen_hdsd_gon.py

Màn không có danh sách / bộ lọc / CRUD: chỉ 2 phần Truy cập + Cập nhật giá (viết qua 'thay' + 'thu_tu').
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_catalog_docs_lib'))
from hdsd_gon import build  # noqa: E402

TEN = 'Cập nhật nhanh giá dịch vụ'


def truycap(c):
    ic, step = c['ic'], c['step']
    c['phan']('TRUY CẬP MÀN HÌNH')
    step(['Bước 1: Từ phân hệ CSKH sau bán ', ic('menu_phanhe'), ', chọn Cập nhật nhanh giá dịch vụ ',
          ('img', ic('menu_muc')[1], 0.36)])   # mục menu 2 dòng chữ: 0,22" làm chữ bé hơn thân bài
    step('Bước 2: Hệ thống mở màn hình, hai ô Hệ số giá bán dịch vụ và Định mức đàm phán giá (%) hiện sẵn giá trị đang dùng.')
    c['img']('01_list', 'Màn hình Cập nhật nhanh giá dịch vụ')


def capnhat(c):
    ic, step, sub = c['ic'], c['step'], c['sub']
    c['phan']('CẬP NHẬT GIÁ DỊCH VỤ')
    step(c['vao'])
    step('Bước 2: Nhập Hệ số giá bán dịch vụ (bắt buộc).')
    step('Bước 3: Nhập Định mức đàm phán giá (%) nếu cần.')
    step(['Bước 4: Bấm ', ic('btn_luu'), ' ở chân trang'])
    sub(['Hoặc bấm ', ic('btn_quaylai'), ' để rời màn hình, không lưu.'])
    step('Bước 5: Hệ thống hiện hộp xác nhận “Xác nhận cập nhật giá dịch vụ”')
    c['img']('30_confirm', 'Hộp xác nhận cập nhật giá dịch vụ')
    step(['Bước 6: Bấm ', ic('btn_confirm_xacnhan'), ' để áp giá cho toàn bộ gói bảo dưỡng'])
    sub(['Hoặc bấm ', ic('btn_huy_confirm'), ' nếu bấm nhầm'])


G = {
    'dir': HERE,
    'ten': TEN,
    'thuat_ngu': [
        ['Hệ số giá bán dịch vụ', 'Hệ số nhân dùng khi tính giá bán (giá gốc cấp dịch vụ) của gói bảo dưỡng. Bắt buộc, từ 0.01 đến 999.99.'],
        ['Định mức đàm phán giá (%)', 'Tỷ lệ phần trăm tối đa được phép giảm khi thương lượng giá với khách hàng. Không bắt buộc, từ 0 đến 99.'],
        ['Gói bảo dưỡng', 'Gói dịch vụ bán cho khách hàng (màn Danh mục gói bảo dưỡng). Mọi gói đều bị áp lại hệ số và định mức khi lưu.'],
        ['Cấp dịch vụ', 'Mức độ của một lần bảo dưỡng trong gói. Giá gốc của cấp dịch vụ được tính lại khi hệ số thay đổi.'],
    ],
    'phien_ban': [
        ['1.0', '13/08/2026', 'Đội phát triển phần mềm', 'Tạo mới cho màn Cập nhật nhanh giá dịch vụ.'],
        ['1.1', '25/09/2026', 'Đội phát triển phần mềm', 'Cập nhật theo phiên bản hiện tại: mục menu riêng trong phân hệ CSKH sau bán, nút Lưu / Quay lại ở chân trang, nút Xác nhận trong hộp xác nhận.'],
        ['1.2', '29/09/2026', 'Đội phát triển phần mềm', 'Rút gọn theo mẫu HDSD mới: mỗi chức năng một phần, chỉ các bước thao tác.'],
    ],
    'quyen': [
        ['Cập nhật nhanh giá dịch vụ', 'Truy cập màn hình, xem và cập nhật hai thông số giá cho toàn bộ gói bảo dưỡng.'],
    ],
    'thu_tu': ['truycap', 'capnhat'],
    'thay': {'truycap': truycap, 'capnhat': capnhat},
}

if __name__ == '__main__':
    print('OK', build(G, os.path.join(HERE, 'out', 'HDSD_Cap nhat nhanh gia dich vu.docx')))
