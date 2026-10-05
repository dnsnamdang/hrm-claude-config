from common import *
def tab(page,label): return page.locator('.tp-card').get_by_text(label, exact=True).first
with browser_page() as page:
    go(page,'/assign/request-solution/pending',25000)
    row=page.locator('tbody tr').first
    acts=row.locator('td').last.locator('a, button, span[title]')
    print('acts',acts.count())
    for k in range(acts.count()):
        print(k, acts.nth(k).get_attribute('title'))
    go(page,'/assign/request-solution/34',45000)
    page.screenshot(path=S+'h04_detail_req.png', full_page=True)
    for lab,fn in [('Thông tin yêu cầu','tab_ttyc'),('Dự án tiền khả thi','tab_tkt'),('Meetings','tab_meetings'),('Phiếu thu thập thông tin','tab_phieu')]:
        cut(page, page.get_by_text(lab, exact=True).first.locator('xpath=..'), fn+'.png')
    for lab,fn in [('Tiếp nhận','btn_tiepnhan_footer'),('Từ chối','btn_tuchoi_footer'),('Quay lại','btn_quaylai')]:
        cut(page, page.locator('.footer').get_by_role('button', name=lab).first, fn+'.png')
    page.get_by_text('Dự án tiền khả thi', exact=True).first.click(); page.wait_for_timeout(5000); page.mouse.move(5,5)
    page.screenshot(path=S+'h05_tab_tkt.png', full_page=True)
    page.get_by_text('Meetings', exact=True).first.click(); page.wait_for_timeout(8000); page.mouse.move(5,5)
    page.screenshot(path=S+'h06_tab_meet.png')
    page.get_by_text('Phiếu thu thập thông tin', exact=True).first.click(); page.wait_for_timeout(10000); page.mouse.move(5,5)
    page.screenshot(path=S+'h07_tab_phieu.png')
    for lab,fn in [('Lịch sử thay đổi','btn_lichsuthaydoi'),('Lưu phiếu','btn_luuphieu'),('Xem mẫu in','btn_xemmauin')]:
        try: cut(page, page.get_by_role('button', name=lab).first, fn+'.png')
        except Exception as e: print('miss',lab,e)
    page.get_by_role('button', name='Lịch sử thay đổi').first.click(); page.wait_for_timeout(8000); page.mouse.move(5,5)
    page.screenshot(path=S+'h08_history.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1500)
    # supplement
    page.get_by_role('button', name='Thêm câu hỏi').first.scroll_into_view_if_needed()
    cut(page, page.get_by_role('button', name='Thêm câu hỏi').first, 'btn_themcauhoi.png')
    page.get_by_role('button', name='Thêm câu hỏi').first.click(); page.wait_for_timeout(1000)
    ta=page.get_by_placeholder('Nhập nội dung câu hỏi...').first
    ta.fill('Vui lòng bổ sung bản vẽ mặt bằng khu vực lắp đặt và công suất điện cấp cho xưởng')
    page.wait_for_timeout(800); page.mouse.move(5,5)
    page.screenshot(path=S+'h11_add_q.png')
    btn_add=page.get_by_role('button', name='Thêm', exact=True).first
    cut(page, btn_add, 'btn_them.png')
    cut(page, page.get_by_role('button', name='Hủy', exact=True).first, 'btn_huy_q.png')
    btn_add.click(); page.wait_for_timeout(1500); page.mouse.move(5,5)
    page.screenshot(path=S+'h12_q_added.png')
    cut(page, page.get_by_role('button', name='Yêu cầu bổ sung').first, 'btn_yeucaubosung.png')
    cut(page, page.locator('.footer').get_by_role('button', name='Hủy yêu cầu làm giải pháp').first, 'btn_huyyc_footer.png')
    # receive modal
    page.reload(wait_until='domcontentloaded'); page.wait_for_timeout(35000); page.mouse.move(5,5)
    page.locator('.footer').get_by_role('button', name='Tiếp nhận').first.click(); page.wait_for_timeout(4000); page.mouse.move(5,5)
    page.screenshot(path=S+'h09_receive.png')
    m=page.locator('.modal.show, .modal-content').last
    cut(page, page.get_by_role('button', name='Xác nhận tiếp nhận').first, 'btn_xacnhantiepnhan.png')
    cut(page, page.locator('.modal-content').last.get_by_role('button', name='Đóng').first, 'btn_dong_modal.png')
    page.locator('.modal-content').last.locator('.select2-selection').first.click(); page.wait_for_timeout(2500)
    page.screenshot(path=S+'h10_pm.png')
