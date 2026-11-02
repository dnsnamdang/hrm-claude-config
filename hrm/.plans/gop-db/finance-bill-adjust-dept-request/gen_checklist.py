# -*- coding: utf-8 -*-
"""Đối chiếu testcase + SRS màn Phiếu yêu cầu điều chỉnh công nợ với checklist "Mẫu tài liệu.xlsx" (02/11/2026).

Chạy: python gen_checklist.py -> Đối chiếu checklist.xlsx (chạy sau gen_testcase.py, gen_srs.py).
Mã TC tra theo KHÓA case trong gen_testcase.py (bảng ID) nên thêm / bớt case không làm lệch map.
Ghi chú trong ngoặc sau tham chiếu ra cột Ghi chú (lệch giữa hành vi thật và checklist).
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from checklist_doi_chieu import write  # noqa: E402
from gen_testcase import ID  # noqa: E402

NA_KHOA = 'N/A: màn không có chức năng Khóa / Mở khóa (phiếu đi theo vòng đời trạng thái, không có trạng thái khóa)'
NA_IMPORT = 'N/A: màn không có chức năng Import Excel'


def k(*keys, note=None):
    ref = ', '.join(ID[('ROLE', x[5:])] if x.startswith('ROLE-') else ID[x] for x in keys)
    return ref + (' (%s)' % note if note else '')


L_ITEM = 'lệch: thông báo hiện là "Item Not Found!" (tiếng Anh), chưa theo chuẩn thông báo tiếng Việt — đúng theo code'
L_PAGE = 'lệch: form Tạo / Sửa là TRANG riêng, không phải popup — TC kiểm màn sau khi lưu điều hướng đi đâu'
L_XL = 'lệch: màn chưa có cửa sổ chọn trường xuất, file luôn 12 cột cố định — đúng theo code'

TC_MAP = {
    1: k('list_open', 'list_open_sale'), 2: k('list_title'), 3: k('list_buttons', 'list_row_btn'), 4: k('list_cols'),
    5: k('list_cols_hidden', note='màn không có cột ẩn mặc định'), 6: k('list_data'), 7: k('list_status'),
    8: k('list_empty'), 9: k('list_nomatch'),
    10: k('list_open'), 11: k('pg_size'), 12: k('pg_next'), 13: k('pg_first_last'), 14: k('pg_btn_state'), 15: k('pg_stt'),
    16: k('pg_total'), 17: k('pg_reset_filter'), 18: k('pg_size'),
    19: k('list_open'), 20: k('sort_asc'), 21: k('sort_desc'), 22: k('sort_date'), 23: k('sort_none'),
    24: k('sort_keep_page'), 25: k('sort_reset_page'),
    26: k('qs_exact'), 27: k('qs_partial'), 28: k('qs_case'),
    29: k('qs_accent', note='kiểm ở ô Khách hàng / Nhà cung cấp; ô tìm nhanh chỉ tìm mã phiếu không dấu'),
    30: k('qs_notfound'),
    31: k('qs_special', note='lệch: "%" và "_" được hiểu là ký tự đại diện, gõ "%" ra toàn bộ phiếu — đúng theo code'),
    32: k('qs_trim'), 33: k('qs_len', note='ô tìm nhanh không giới hạn ký tự'), 34: k('qs_clear'), 35: k('qs_enter', 'qs_exact'),
    36: k('flt_default'),
    37: k('flt_type', 'flt_status', 'flt_party', 'flt_contract', 'flt_money', 'flt_date', 'flt_people', 'flt_report', 'org_pick'),
    38: k('combo_2', 'combo_3'), 39: k('combo_1'), 40: k('flt_nores'), 41: k('flt_total'), 42: k('flt_paging'), 43: k('flt_sort'),
    44: k('flt_reset'),
    45: k('mem_back', 'mem_other', 'mem_expire'),
    46: k('mem_f5', note='lệch: F5 không giữ bộ lọc đang chọn, chỉ nhớ khi đi vào chi tiết / sửa trong 10 phút — đúng theo code'),
    47: k('mem_tab'),
    48: k('mem_account', note='lệch tiềm ẩn: bộ lọc lưu theo trình duyệt, không theo tài khoản'),
    49: k('add_nav'), 50: k('add_title'), 51: k('add_fields'), 52: k('add_required'), 53: k('add_default'),
    54: k('add_fields', note='không có nút Đóng: form là trang riêng, dùng nút Quay lại'),
    55: k('add_send_ok'), 56: k('add_required_only'), 57: k('add_required_only', 'add_draft_missing'), 58: k('add_after'),
    59: k('add_draft_ok', 'add_send_ok'), 60: k('add_history'),
    61: k('add_send_empty', 'add_send_missing_to'), 62: k('add_format', 'add_rate'), 63: k('add_special'),
    64: k('add_minlen', note='Diễn giải không có độ dài tối thiểu'),
    65: k('add_maxlen', note='lệch: Diễn giải chưa có giới hạn độ dài tối đa — đúng theo code'),
    66: k('add_overlen', note='lệch: không chặn / không báo vượt độ dài tối đa — đúng theo code'),
    67: k('add_dup', note='phiếu không có trường duy nhất: 2 phiếu cùng nội dung đều lưu, mã khác nhau'),
    68: k('add_trim'), 69: k('add_spaces'), 70: k('add_send_empty', 'add_send_missing_to'), 71: k('add_err_clear'),
    72: k('sc_ok'), 73: k('sc_missing'), 74: k('sc_format'), 75: k('sc_dup'), 76: k('sc_ok', note=L_PAGE),
    77: k('sc_ok'), 78: k('sc_close'),
    79: k('add_draft_ok'), 80: k('add_draft_missing'), 81: k('add_format'), 82: k('add_dup'), 83: k('draft_close', note=L_PAGE),
    84: k('draft_close'), 85: k('draft_close'),
    86: k('add_send_ok'), 87: k('add_send_empty', 'add_send_missing_to'), 88: k('add_rate'), 89: k('add_concurrent', 'add_dup'),
    90: k('draft_close', note=L_PAGE), 91: k('draft_close'), 92: k('draft_close'),
    93: k('close_empty'), 94: k('close_dirty'),
    95: k('close_tab', note='form là trang riêng: không có nút X của popup, kiểm bằng dấu X của tab trình duyệt'),
    96: k('close_exit'), 97: k('close_stay'), 98: k('close_cleared'), 99: k('close_restored'),
    100: k('close_idle', note='hết phiên khi đang nhập: dữ liệu chưa lưu bị mất'),
    101: k('add_double'), 102: k('add_concurrent'),
    103: k('ed_open', note='màn Sửa là trang riêng, không phải popup'), 104: k('ed_fill'), 105: k('ed_fields'), 106: k('ed_buttons'),
    107: k('ed_one'), 108: k('ed_many'), 109: k('ed_same'), 110: k('ed_after'), 111: k('ed_updated'), 112: k('ed_history'),
    113: k('ed_required'), 114: k('ed_format'), 115: k('ed_overlimit'), 116: k('ed_dup_other'), 117: k('ed_required'),
    118: k('ed_err_clear'),
    119: k('ed_nochange_close'), 120: k('ed_restore'), 121: k('ed_dirty_close'), 122: k('ed_exit'), 123: k('ed_stay'),
    124: k('ed_exit'), 125: k('ed_no_log', 'ed_same'),
    126: 'N/A: màn không có chức năng Khóa; phiếu sai trạng thái không có nút Sửa (kiểm ở %s)' % ID['ed_in_use'],
    127: k('ed_deleted', note=L_ITEM), 128: k('ed_concurrent'), 129: k('ed_in_use'),
    130: k('del_btn'), 131: k('del_popup'), 132: k('del_popup'), 133: k('del_ok'), 134: k('del_cancel'), 135: k('del_in_use'),
    136: k('del_children'), 137: NA_KHOA, 138: k('del_gone', note=L_ITEM), 139: k('del_ok'), 140: k('del_ok'),
    141: k('del_related'),
    162: k('his_open'),
    163: k('his_cols', note='popup hiển thị dạng dòng thời gian từng mốc, không phải bảng cột'),
    164: k('his_order'), 165: k('his_actor'), 166: k('his_actor'), 167: k('his_type'), 168: k('his_content'),
    169: k('his_f_action'), 170: k('his_f_actor'), 171: k('his_f_date'), 172: k('his_f_combo'), 173: k('his_f_none'),
    174: k('his_f_reset'), 175: k('his_f_toggle'),
    176: k('his_create'), 177: k('his_edit_one'), 178: k('his_edit_many'), 179: NA_KHOA, 180: NA_KHOA,
    181: NA_IMPORT + ' nên không có lịch sử tạo bằng import',
    182: k('his_nochange'), 183: k('his_multi'), 184: k('his_close'), 185: k('his_keep'),
    186: k('dt_open', note='màn chi tiết là trang riêng, không phải popup'), 187: k('dt_title'), 188: k('dt_fields'),
    189: k('dt_match_create'), 190: k('dt_match_list'), 191: k('dt_readonly'), 192: k('dt_no_save'), 193: k('dt_buttons', 'dt_reject_note'),
    194: NA_KHOA, 195: k('dt_history'), 196: k('dt_close'),
    197: k('dt_keep', note='lệch: giữ bộ lọc và sắp xếp nhưng về trang 1 (không nhớ số trang) — đúng theo code'),
    198: k('col_open'), 199: k('col_list'), 200: k('col_default'), 201: k('col_show'), 202: k('col_hide'), 203: k('col_locked'),
    204: k('col_drag'), 205: k('col_fixed'), 206: k('col_save'), 207: k('col_close'), 208: k('col_f5'), 209: k('col_account'),
    210: k('col_data'), 211: k('col_filter'),
    212: k('xl_no_popup', note=L_XL), 213: k('xl_no_popup', 'xl_order', note=L_XL), 214: k('xl_no_popup', note=L_XL),
    215: k('xl_fixed_cols', note=L_XL), 216: k('xl_fixed_cols', note=L_XL), 217: k('xl_fixed_cols', note=L_XL),
    218: k('xl_no_popup', note=L_XL),
    219: k('xl_search'), 220: k('xl_filter'), 221: k('xl_pages'), 222: k('xl_empty'),
    223: k('xl_name'), 224: k('xl_format'), 225: k('xl_head'), 226: k('xl_order'), 227: k('xl_count'), 228: k('xl_data'),
    229: k('xl_types'), 230: k('xl_vn'),
    268: k('ef_no_child'), 269: k('ef_child'), 270: k('del_in_use'), 271: NA_KHOA, 272: k('ef_edit_link'), 273: NA_KHOA,
    274: k('ef_appear'), 275: NA_IMPORT, 276: NA_KHOA, 277: NA_KHOA, 278: k('ef_rename'),
    279: 'N/A: mã phiếu do hệ thống sinh khi lưu, không sửa được nên không có tình huống đổi mã',
    280: k('ef_delete_sync'), 281: k('ef_status_auto'), 282: k('ef_filter'),
    283: k('ef_parent'), 284: k('ef_ref_keep'), 285: k('ef_orphan', 'del_children'), 286: k('ef_no_dup', 'add_double'),
    287: k('ROLE-00', 'ROLE-01', 'ROLE-02', 'ROLE-03', 'ROLE-04', 'ROLE-06'), 288: k('ROLE-10', 'ROLE-08', 'dt_open'),
    289: k('pq_create'), 290: k('ROLE-09', 'pq_url'), 291: k('ROLE-09', 'del_in_use'),
    292: 'N/A: màn không có chức năng Khóa / Mở khóa nên không có quyền tương ứng',
    293: k('pq_export', note='màn không có Import'), 294: k('pq_history'), 295: k('ROLE-08', 'ROLE-09', 'list_row_btn'),
    296: k('ROLE-07', 'ROLE-10', 'pq_url', note='màn Sửa vẫn mở được bằng đường dẫn, hệ thống chặn ở bước Lưu'),
    297: k('pq_api', 'del_in_use'), 298: k('pq_revoke'), 299: k('ROLE-01', 'ROLE-02', 'ROLE-03', 'ROLE-04', 'ROLE-05'),
    300: k('ap_btn', note='"Duyệt" của màn này là Tạo phiếu kế toán'),
    301: k('ap_popup', note='lệch: không có cửa sổ xác nhận duyệt, bấm là mở màn Tạo phiếu kế toán; xác nhận ghi sổ ở nút Lưu và duyệt của màn phiếu kế toán'),
    302: k('ap_ok'), 303: k('ap_required'), 304: k('ap_rules'), 305: k('ap_ok'), 306: k('ap_data'),
    307: k('ap_related', 'ef_status_auto'), 308: k('ap_notify'), 309: k('ap_notify_link'), 310: k('ap_cancel'), 311: k('ap_again'),
    312: k('ap_history'),
    313: k('rj_btn', note='"Không duyệt" của màn này là Từ chối'), 314: k('rj_popup'), 315: k('rj_ok'), 316: k('rj_empty'),
    317: k('rj_len'), 318: k('rj_status'), 319: k('rj_reason'), 320: k('rj_related'), 321: k('rj_notify'), 322: k('rj_cancel'),
    323: k('rj_again'), 324: k('rj_history'),
}
for n in range(142, 162):
    TC_MAP[n] = NA_KHOA
for n in range(231, 268):
    TC_MAP[n] = NA_IMPORT

S_NA_KHOA = 'N/A: màn không có chức năng Khóa / Mở khóa'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2', 12: 'Phần 2',
    13: 'Phần 2 (ma trận ghi rõ màn không có Khóa / Mở khóa)', 14: 'Phần 2 (không có Import; Xuất Excel, Lịch sử dùng phạm vi xem)',
    15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3; 2.5.1 (sơ đồ tổng quan + Use Case từng chức năng thao tác)', 18: '2.1.1; 2.5.2', 19: '2.1.1; 2.5.2',
    20: '2.5.2', 21: '2.5.2', 22: '2.5.2', 23: '2.1.1; 2.5.2 (đoạn "Quy tắc chung" có ở cả 16 chức năng)',
    24: '2.1.2; 2.5.3', 25: '2.10.3; 2.12.3; 2.14.3', 26: '2.1.3; 2.5.4', 27: '2.5.4', 28: '2.5.4', 29: '2.1.4; 2.5.5',
    30: '2.5.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1; 2.1.3', 34: '2.1.3', 35: '2.1.3; 2.1.4', 36: '2.1.3', 37: '2.1.3', 38: '2.1.1',
    39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1', 43: '2.2.1; 2.2.3 (không giới hạn ký tự)', 44: '2.2.3', 45: '2.2.3', 46: '2.2.1',
    47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1', 50: '2.2.1; 2.1.3', 51: '2.2.4',
    52: '2.5.2; Phần 2 (trang riêng, không phải popup)', 53: '2.5.4', 54: '2.5.4', 55: '2.5.2', 56: '2.5.4; 2.5.5', 57: '2.5.5',
    58: '2.5.2; 2.5.4', 59: '2.5.2 (lệch: form là trang riêng, không có nút X / click ngoài — đóng tab thì trình duyệt hỏi)',
    60: '2.5.2; 2.5.4', 61: '2.5.5', 62: '2.5.5',
    63: '2.8.2; Phần 2', 64: '2.8.2', 65: '2.8.2', 66: '2.8.5', 67: '2.8.2', 68: '2.8.2', 69: '2.8.5', 70: '2.8.5',
    71: 'N/A: màn không có khóa; phiếu ngoài trạng thái Đang tạo / Từ chối không sửa được (ghi ở 2.8.2)',
    72: '2.8.5; 2.16.3', 73: '2.8.5',
    74: '2.10.2; Phần 2', 75: '2.10.2', 76: '2.10.2; Phần 4', 77: S_NA_KHOA, 78: '2.10.4', 79: '2.10.4', 80: '2.10.2; 2.10.5',
    81: '2.10.5', 82: '2.10.5',
    83: 'Phần 1 (các trạng thái phiếu; màn không có Khóa / Mở khóa)',
    94: '2.16.1; 2.16.2', 95: '2.16.3', 96: '2.16.3', 97: '2.16.1; 2.16.3', 98: '2.16.3', 99: '2.16.1', 100: '2.16.1; 2.16.4',
    101: '2.16.4',
    120: '2.15.2 (lệch: chưa có cửa sổ chọn trường xuất — đúng theo code)', 121: '2.15.4',
    122: '2.15.2 (lệch: không chọn trường, luôn đủ 12 cột)', 123: '2.15.2 (lệch: không có Chọn tất cả / Bỏ chọn hết)',
    124: '2.15.2; 2.15.4', 125: '2.15.2', 126: '2.15.2', 127: '2.15.2; 2.15.4', 128: '2.15.2; 2.15.4',
    129: '2.15.5 (lệch: không có event chọn trường)',
    130: '2.11.2', 131: '2.11.3', 132: '2.11.4', 133: '2.11.4', 134: S_NA_KHOA, 135: '2.11.4', 136: '2.11.4; 2.16.3',
    137: '2.11.2 (lệch: giữ bộ lọc, sắp xếp; không giữ số trang)', 138: '2.11.5',
    139: '2.4.1; 2.4.2', 140: '2.4.3', 141: '2.4.1; 2.4.3', 142: '2.4.3; 2.4.4', 143: '2.4.4', 144: '2.4.1', 145: '2.4.1',
    146: '2.4.4',
    147: 'Phần 4 (BR-08, BR-14)', 148: 'Phần 4 (BR-14)', 149: 'N/A: màn không có khóa nên không có trùng với bản ghi đã khóa (ghi ở BR-14)',
    150: 'Phần 4 (BR-01)', 151: 'Phần 4 (BR-15)', 152: S_NA_KHOA, 153: 'Phần 4 (BR-16); Phần 5', 154: 'Phần 4 (BR-17)',
    155: 'Phần 4 (BR-02 → BR-13)',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5', 161: S_NA_KHOA + ' (Phần 5 ghi rõ)', 162: 'Phần 5',
    163: 'Phần 5',
}
for n in range(84, 94):
    SRS_MAP[n] = S_NA_KHOA
for n in range(102, 120):
    SRS_MAP[n] = 'N/A: màn không có chức năng Import Excel'

if __name__ == '__main__':
    write(HERE, TC_MAP, SRS_MAP)
