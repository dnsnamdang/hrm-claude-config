(function(){var pop=document.querySelector('.mk-filter-pop'),tb=document.querySelector('.mk-tb'),btn=document.querySelector('.mk-filter-btn');if(!pop||!tb)return;
var KEY='mk-filter-pop-box',MIN=480,DEF=680;
function mk(c,t){var d=document.createElement('div');d.className=c;d.title=t;pop.appendChild(d);return d;}
var hl=mk('mk-fp-rz-l','Kéo sang trái để nới rộng · kéo đúp: về mặc định'),hr=mk('mk-fp-rz-r','Kéo để đổi độ rộng · kéo đúp: về mặc định'),hc=mk('mk-fp-rz','Kéo để đổi độ rộng · kéo đúp: về mặc định');
var info=document.createElement('span');info.className='mk-fp-w';var ft=pop.querySelector('.mk-fp-ft');if(ft)ft.prepend(info);
function tbW(){return tb.clientWidth;}
function place(left,w){var W=tbW();w=Math.round(Math.min(Math.max(w,MIN),W));left=Math.round(Math.min(Math.max(left,0),W-w));pop.style.left=left+'px';pop.style.width=w+'px';var c=w<780?2:(w<1040?3:4);pop.setAttribute('data-cols',c);if(!info.isConnected){var f2=pop.querySelector('.mk-fp-ft');if(f2)f2.prepend(info);}info.textContent=w+'px · '+c+' cột';return [left,w];}
function def(){return place(btn?btn.offsetLeft:0,DEF);}
var saved=null;try{saved=JSON.parse(localStorage.getItem(KEY)||'null');}catch(x){}
if(saved&&saved.w)place(saved.l,saved.w);else def();
function save(){try{localStorage.setItem(KEY,JSON.stringify({l:parseInt(pop.style.left,10),w:parseInt(pop.style.width,10)}));}catch(x){}}
function start(side){return function(ev){ev.preventDefault();ev.stopPropagation();var x0=ev.clientX,l0=parseInt(pop.style.left,10)||0,w0=parseInt(pop.style.width,10)||DEF;pop.classList.add('mk-rzing');
function mv(m){var dx=m.clientX-x0;if(side==='l'){var nl=Math.max(0,Math.min(l0+dx,l0+w0-MIN));place(nl,w0+(l0-nl));}else{place(l0,w0+dx);}}
function up(){document.removeEventListener('mousemove',mv);document.removeEventListener('mouseup',up);pop.classList.remove('mk-rzing');window.__mkRz=Date.now();save();}
document.addEventListener('mousemove',mv);document.addEventListener('mouseup',up);};}
hl.addEventListener('mousedown',start('l'));hr.addEventListener('mousedown',start('r'));hc.addEventListener('mousedown',start('r'));
[hl,hr,hc].forEach(function(el){el.addEventListener('click',function(ev){ev.stopPropagation();});el.addEventListener('dblclick',function(ev){ev.stopPropagation();def();try{localStorage.removeItem(KEY);}catch(x){}});});
window.addEventListener('resize',function(){place(parseInt(pop.style.left,10)||0,parseInt(pop.style.width,10)||DEF);});
})();
