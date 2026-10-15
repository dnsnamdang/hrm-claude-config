async (page) => {
  const KEY='__KEY__', FROM=0, ONLY=null, SKIP_EDITS=false;
  const base='http://127.0.0.1:8766/'+KEY+'/';
  const W=(ms)=>page.waitForTimeout(ms);
  const norm=(s)=>(s||'').replace(/\s+/g,' ').trim();
  async function go(ref){ await page.click('#t-name-box'); await page.fill('#t-name-box', ref); await page.keyboard.press('Enter'); await W(450); }
  async function val(ref){ await go(ref); return await page.evaluate(()=>{const e=document.querySelector('#t-formula-bar-input'); return e? e.innerText.replace(/\n$/,''):null}); }
  async function paste(ref,text){ await go(ref); await page.evaluate((t)=>{const dt=new DataTransfer(); dt.setData('text/plain',t); document.activeElement.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}));},text); await W(1500); }
  async function menu(top,sub,item){ await page.click(top); await W(600); if(sub){ await page.locator('.goog-menuitem:visible',{hasText:sub}).first().hover(); await W(700);} await page.locator('.goog-menuitem:visible',{hasText:item}).first().click(); await W(1300); }
  async function merge(r){ await go(r); await menu('#docs-format-menu',/^Hợp nhất ô/,'Hợp nhất theo chiều dọc'); const ok=page.locator('[role=dialog] button:visible',{hasText:/^OK$/}); if(await ok.count()){ await ok.first().click(); await W(800);} }
  async function groups(label){ await go('A1'); for(let y=170;y<760;y+=10){ await page.mouse.click(13,y,{button:'right'}); await W(220); const it=page.locator('.goog-menuitem:visible',{hasText:label}); if(await it.count()){ await it.first().click(); await W(1200); return true;} await page.keyboard.press('Escape'); await W(80);} return false; }
  const idx=(await (await page.request.get(base+'index.json')).json());
  const tid=await page.evaluate((name)=>{const el=[...document.querySelectorAll('.docs-sheet-tab')].find(e=>e.innerText.trim().split('\n').pop().trim().startsWith(name)); return el?el.id:null;}, idx.tab);
  if(!tid) return {error:'Không thấy tab '+idx.tab};
  await page.click('[id="'+tid+'"]'); await W(1500);
  const expanded = await groups('Mở rộng tất cả các nhóm hàng');
  const res=[];
  if(!SKIP_EDITS) for(let i=0;i<idx.ecount;i++){
    const E=await (await page.request.get(base+'e'+String(i).padStart(2,'0')+'.json')).json();
    const c=await val((E.idcol||'C')+E.row);
    if(norm(c)!==norm(E.expect_c)){ return {stop:'edit '+i, error:(E.idcol||'C')+E.row+'='+JSON.stringify(c)+' cần '+E.expect_c, res}; }
    const cur=await val(E.cell);
    if(!norm(cur).startsWith(norm(E.expect_prefix).slice(0,18)) && !norm(cur).startsWith(norm(E.text.replace(/^"|"$/g,'').replace(/""/g,'"')).slice(0,18))){ return {stop:'edit '+i, error:E.cell+'='+JSON.stringify((cur||'').slice(0,60))+' cần '+E.expect_prefix, res}; }
    await paste(E.cell, E.text);
    if(E.clear){ await go(E.clear); await page.keyboard.press('Delete'); await W(700); }
    const after=await val(E.cell);
    res.push({edit:i, cell:E.cell, ok: norm(after).slice(0,15)===norm(E.text.replace(/^"|"$/g,'').replace(/""/g,'"')).slice(0,15)});
  }
  for(let i=FROM;i<idx.count;i++){
    if(ONLY!==null && i!==ONLY) continue;
    const OP=await (await page.request.get(base+String(i).padStart(2,'0')+'.json')).json();
    const IC=OP.idcol||'C'; const cur=await val(IC+OP.after_row);
    if(norm(cur)!==norm(OP.expect_c)){ res.push({i,error:IC+OP.after_row+'='+JSON.stringify(cur)+' cần '+OP.expect_c}); return {stop:i,res}; }
    const nxt=await val(IC+(OP.after_row+1));
    if(norm(nxt)!==norm(OP.expect_next)){ res.push({i,error:'hàng sau='+JSON.stringify(nxt).slice(0,60)+' cần '+OP.expect_next.slice(0,60)}); return {stop:i,res}; }
    const n=OP.n_rows;
    await go((OP.after_row-n+1)+':'+OP.after_row);
    await menu('#docs-insert-menu',/^Hàng/,'Chèn '+n+' hàng xuống dưới');
    if(OP.header_from){
      await go(OP.header_from+':'+OP.header_from); await page.keyboard.press('Meta+c'); await W(700);
      await go((OP.after_row+1)+':'+(OP.after_row+1)); await page.keyboard.press('Meta+v'); await W(1500);
      await paste(IC+(OP.after_row+1), OP.header_title);
    }
    await paste(OP.paste_at, OP.tsv);
    if(OP.ab_tsv) await paste('A'+OP.first_case_row, OP.ab_tsv);
    for(const m of OP.merges) await merge(m);
    const chk=await val(IC+OP.last_case_row);
    const first=await val(OP.paste_at);
    const ok=norm(chk)===norm(OP.last_id) && norm(first)===norm(OP.first_id);
    res.push({i,ok, first, last:chk});
    if(!ok) return {stop:i,res};
  }
  if(expanded) await groups('Thu gọn tất cả các nhóm hàng');
  return {done:true,res};
}
