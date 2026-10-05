import sys, re; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
from _vm import vm_eval
S = 'shots/'
STEP = sys.argv[1] if len(sys.argv) > 1 else 'all'
def settle(page, extra=2500):
    page.wait_for_timeout(2500)
    page.wait_for_function("() => !document.querySelector('.loading-page')", timeout=240000)
    page.wait_for_timeout(extra)
def go(page, path, sel='text=Thông tin yêu cầu'):
    page.goto(BASE + path, wait_until='domcontentloaded')
    page.wait_for_selector(sel, timeout=240000); settle(page)
def btn(page, name):
    return page.locator('button', has_text=re.compile(r'^\s*%s\s*$' % re.escape(name)))
def main():
  with browser_page() as page:
      if STEP in ('all', 'a'):
          go(page, '/assign/request-solution/add')
          page.screenshot(path=S + '06-tao-trong.png')
          btn(page, 'Lưu nháp').last.click(); page.wait_for_timeout(1500); settle(page, 1500)
          page.screenshot(path=S + '06b-tao-loi.png')
          go(page, '/assign/request-solution/36')
          page.screenshot(path=S + '10-ct-nhap.png')
          go(page, '/assign/request-solution/36/edit')
          page.screenshot(path=S + '11-sua-nhap.png')
          go(page, '/assign/request-solution/25/edit')
          page.screenshot(path=S + '12-sua-bosung.png')
          go(page, '/assign/request-solution/25')
          page.screenshot(path=S + '12b-ct-bosung.png')
      if STEP in ('all', 'b'):
          go(page, '/assign/request-solution/34')
          page.screenshot(path=S + '10b-ct-cho.png')
          for nm, f in [('Tiếp nhận', 'icon_tiepnhan_ft'), ('Từ chối', 'icon_tuchoi_ft')]:
              b = btn(page, nm); print(nm, b.count())
              if b.count(): clip(page, b.last, S + f + '.png')
          for i, t in enumerate(['Dự án tiền khả thi', 'Meetings', 'Phiếu thu thập thông tin']):
              page.get_by_text(t, exact=True).first.click(); page.wait_for_timeout(1500); settle(page, 3000)
              page.screenshot(path=S + '10%s-tab-%d.png' % ('cde'[i], i + 1))
          page.get_by_text('Thông tin yêu cầu', exact=True).first.click(); page.wait_for_timeout(1500)
          btn(page, 'Tiếp nhận').last.click(); page.wait_for_timeout(3000)
          page.screenshot(path=S + '15-tiepnhan.png')
          page.keyboard.press('Escape'); page.wait_for_timeout(1500)
          go(page, '/assign/request-solution/34')
          btn(page, 'Từ chối').last.click(); page.wait_for_timeout(2000)
          page.screenshot(path=S + '15b-tuchoi.png')
          page.locator('.modal.show').locator('button', has_text='Không').click(); page.wait_for_timeout(800)
      if STEP in ('all', 'c'):
          page.goto(BASE + '/assign/prospective-projects', wait_until='domcontentloaded')
          page.wait_for_selector('table.data-table tbody tr td', timeout=240000); settle(page)
          row = page.locator('tr', has_text='Mazda Thái Bình').first
          b = row.locator('a[href*="request-solution/add"]').first
          b.scroll_into_view_if_needed(); page.wait_for_timeout(800)
          clip(page, b, S + 'icon_taoycgp_row.png')
          page.screenshot(path=S + '08-tkt-ds.png')
          go(page, '/assign/request-solution/add?prospective_project_id=156')
          page.wait_for_timeout(4000)
          print(vm_eval(page, 'RequestSolutionForm', """
              vm.request.title = 'Yêu cầu làm giải pháp cầu nâng và thiết bị bảo dưỡng nhanh xưởng Mazda Thái Bình';
              vm.request.receive_dept = 51;
              vm.request.customer_need_quote_date = '2026-12-05';
              vm.request.note = 'Khách hàng cần phương án 4 khoang bảo dưỡng nhanh, ưu tiên cầu nâng cắt kéo âm nền; gửi kèm bản vẽ mặt bằng xưởng.';
              return vm.request.project_key + ' ' + vm.request.project_phase_id""", None))
          page.wait_for_timeout(2500)
          page.screenshot(path=S + '09-tao-tu-tkt.png')
          btn(page, 'Lưu và gửi').last.click(); page.wait_for_timeout(1500)
          page.screenshot(path=S + '09b-xac-nhan-gui.png')
          page.locator('.modal.show').locator('button', has_text='Xác nhận').click(); page.wait_for_timeout(8000)
          print(page.url)

if __name__ == '__main__':
    main()
