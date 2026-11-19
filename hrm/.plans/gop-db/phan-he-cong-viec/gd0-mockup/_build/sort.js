(function(){
window.__mkRenumber=function(){document.querySelectorAll('table').forEach(function(t){var h=t.querySelector('thead tr');if(!h||!/^STT$/i.test((h.children[0].textContent||'').trim()))return;var f=document.body.classList.contains('mk-filtered'),i=0;[].slice.call(t.querySelectorAll('tbody > tr')).forEach(function(r){if(!f||!r.classList.contains('mk-fx'))r.children[0].textContent=String(++i);});if(f)[].slice.call(t.querySelectorAll('tbody > tr.mk-fx')).forEach(function(r){r.children[0].textContent=String(++i);});});};

function val(td){var t=(td.innerText||td.textContent||'').trim();var m=t.match(/(\d{2})\/(\d{2})\/(\d{4})(?:\s+(\d{2}):(\d{2}))?/);if(m)return {n:+new Date(+m[3],+m[2]-1,+m[1],+(m[4]||0),+(m[5]||0))};
var n=t.replace(/\s/g,'').match(/^-?[\d.,]+/);if(n&&/^[\d.,\s%/()-]|^\d/.test(t)){var v=parseFloat(n[0].replace(/\./g,'').replace(',','.'));if(!isNaN(v))return {n:v};}
if(t==='—'||t==='')return {n:null,s:''};return {s:t.toLowerCase()};}
document.querySelectorAll('thead .sortable-header').forEach(function(h){h.addEventListener('click',function(){
var th=h.closest('th'),tr=th.parentElement,idx=[].indexOf.call(tr.children,th),table=th.closest('table'),tb=table.querySelector('tbody');
var dir=h.getAttribute('data-dir')==='asc'?'desc':'asc';
table.querySelectorAll('thead .sortable-header').forEach(function(o){o.removeAttribute('data-dir');o.classList.remove('is-sorted');var i=o.querySelector('i.mk-sort');if(i)i.className='ri-arrow-up-down-line mk-sort';});
h.setAttribute('data-dir',dir);h.classList.add('is-sorted');h.querySelector('i.mk-sort').className=(dir==='asc'?'ri-arrow-up-line':'ri-arrow-down-line')+' mk-sort';
var rows=[].slice.call(tb.children);rows.sort(function(a,b){var x=val(a.children[idx]||a),y=val(b.children[idx]||b);
if(x.n===null&&y.n!==null)return 1;if(y.n===null&&x.n!==null)return -1;var r=(x.n!=null&&y.n!=null)?x.n-y.n:(x.s||'').localeCompare(y.s||'','vi');return dir==='asc'?r:-r;});
rows.forEach(function(r){tb.appendChild(r);});
window.__mkRenumber&&window.__mkRenumber();
});});})();
