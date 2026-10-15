async (page) => {
  const NN='__NN__', FROM=__FROM__, ONLY=__ONLY__;
  const base='http://127.0.0.1:8765/'+NN+'/';
  const W=(ms)=>page.waitForTimeout(ms);
  async function go(ref){ await page.click('#t-name-box'); await page.fill('#t-name-box', ref); await page.keyboard.press('Enter'); await W(450); }
  async function val(ref){ await go(ref); return await page.evaluate(()=>{const e=document.querySelector('#t-formula-bar-input'); return e? e.innerText.replace(/\n$/,''):null}); }
  async function paste(ref,text){ await go(ref); await page.evaluate((t)=>{const dt=new DataTransfer(); dt.setData('text/plain',t); document.activeElement.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}));},text); await W(1500); }
  async function menu(top,sub,item){ await page.click(top); await W(600); if(sub){ await page.locator('.goog-menuitem:visible',{hasText:sub}).first().hover(); await W(700);} await page.locator('.goog-menuitem:visible',{hasText:item}).first().click(); await W(1300); }
  async function merge(r){ await go(r); await menu('#docs-format-menu',/^Hợp nhất ô/,'Hợp nhất theo chiều dọc'); const ok=page.locator('[role=dialog] button:visible',{hasText:/^OK$/}); if(await ok.count()){ await ok.first().click(); await W(800);} }
  async function groups(label){ await go('A1'); for(let y=170;y<760;y+=10){ await page.mouse.click(13,y,{button:'right'}); await W(220); const it=page.locator('.goog-menuitem:visible',{hasText:label}); if(await it.count()){ await it.first().click(); await W(1200); return true;} await page.keyboard.press('Escape'); await W(80);} return false; }
  const idx=(await (await page.request.get(base+'index.json')).json());
  const tid=await page.evaluate((name)=>{const el=[...document.querySelectorAll('.docs-sheet-tab')].find(e=>e.innerText.trim().split('\n').pop().trim().startsWith(name)); return el?el.id:null;}, idx.tab);
  if(!tid) return {error:'Không thấy tab '+idx.tab};
  await page.click('#'+tid.replace(/:/g,'\\:')); await W(1500);
  await groups('Mở rộng tất cả các nhóm hàng');
  const res=[];
  for(let i=FROM;i<idx.count;i++){
    if(ONLY!==null && i!==ONLY) continue;
    const OP=await (await page.request.get(base+String(i).padStart(2,'0')+'.json')).json();
    const cur=await val('C'+OP.after_row);
    if(cur!==OP.expect_c){ res.push({i,error:'C'+OP.after_row+'='+JSON.stringify(cur)+' cần '+OP.expect_c}); return {stop:i,res}; }
    const nxt=await val('C'+(OP.after_row+1));
    if(nxt!==OP.expect_next){ res.push({i,error:'hàng sau='+JSON.stringify(nxt).slice(0,60)+' cần '+OP.expect_next.slice(0,60)}); return {stop:i,res}; }
    const n=OP.n_rows;
    await go((OP.after_row-n+1)+':'+OP.after_row);
    await menu('#docs-insert-menu',/^Hàng/,'Chèn '+n+' hàng xuống dưới');
    if(OP.header_from){
      await go(OP.header_from+':'+OP.header_from); await page.keyboard.press('Meta+c'); await W(700);
      await go((OP.after_row+1)+':'+(OP.after_row+1)); await page.keyboard.press('Meta+v'); await W(1500);
      await paste('C'+(OP.after_row+1), OP.header_title);
    }
    await paste(OP.paste_at, OP.tsv);
    if(OP.ab_tsv) await paste('A'+OP.first_case_row, OP.ab_tsv);
    for(const m of OP.merges) await merge(m);
    const chk=await val('C'+OP.last_case_row);
    const first=await val(OP.paste_at);
    res.push({i,ok:chk===OP.last_id && first===OP.first_id, first, last:chk});
    if(!(chk===OP.last_id && first===OP.first_id)) return {stop:i,res};
  }
  if(!idx.keep_open) await groups('Thu gọn tất cả các nhóm hàng');
  return {done:true,res};
}
