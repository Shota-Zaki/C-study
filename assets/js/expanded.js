/* Navigation and reading aids; all educational text remains in static HTML. */
(() => {
  'use strict';
  const article=document.querySelector('.article');if(!article)return;
  const nav=document.querySelector('.left-nav'),openButton=document.querySelector('[data-drawer="open"]');
  let previousFocus=null;
  function openDrawer(){if(!nav)return;previousFocus=document.activeElement;nav.classList.add('open');openButton?.setAttribute('aria-expanded','true');nav.querySelector('button,a')?.focus();}
  function closeDrawer(){nav?.classList.remove('open');openButton?.setAttribute('aria-expanded','false');previousFocus?.focus?.();}
  openButton?.addEventListener('click',openDrawer);
  document.querySelector('[data-drawer="close"]')?.addEventListener('click',closeDrawer);
  nav?.addEventListener('click',event=>{if(innerWidth<=820&&event.target.closest('a'))closeDrawer();});
  document.addEventListener('keydown',event=>{
    if(!nav?.classList.contains('open')||innerWidth>820)return;
    if(event.key==='Escape'){event.preventDefault();closeDrawer();return;}
    if(event.key==='Tab'){const elements=[...nav.querySelectorAll('a,button,input,select,[tabindex="0"]')].filter(x=>x.getClientRects().length);const first=elements[0],last=elements.at(-1);if(event.shiftKey&&document.activeElement===first){event.preventDefault();last?.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first?.focus();}}
  });
  document.addEventListener('click',event=>{
    if(innerWidth<=820&&nav?.classList.contains('open')&&!nav.contains(event.target)&&!openButton?.contains(event.target))closeDrawer();
    const button=event.target.closest('[data-wrap-code]');if(button){const wrapped=button.closest('.codebox').classList.toggle('wrap-code');button.setAttribute('aria-pressed',String(wrapped));button.textContent=wrapped?'折り返し解除':'折り返し';}
  });
  function revealHash(){let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}if(!id)return;const target=document.getElementById(id);if(!target)return;let node=target;while(node&&node!==article.parentElement){if(node.tagName==='DETAILS')node.open=true;node=node.parentElement;}requestAnimationFrame(()=>target.scrollIntoView({block:'start',behavior:'instant'}));}
  addEventListener('hashchange',revealHash);if(location.hash)revealHash();
  const headings=[...article.querySelectorAll('h2[id]')],title=document.querySelector('.reading-title'),count=document.querySelector('[data-reading-count]'),bar=document.querySelector('[data-reading-progress]');
  const tocLinks=[...document.querySelectorAll('.right-toc a[href^="#"],.compact-toc a[href^="#"]')];let queued=false,lastId='';
  function readingPosition(){queued=false;if(!headings.length)return;let index=-1;for(let i=0;i<headings.length;i++){if(headings[i].getBoundingClientRect().top<=160)index=i;else break;}const current=index<0?null:headings[index],currentId=current?.id||'__intro__';if(currentId!==lastId){lastId=currentId;if(title)title.textContent=current?.textContent||article.querySelector('h1')?.textContent||'導入';if(count)count.textContent=index<0?`導入 / ${headings.length}`:`${index+1} / ${headings.length}`;tocLinks.forEach(a=>{const active=!!current&&a.hash==='#'+current.id;a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});}if(bar){const box=article.getBoundingClientRect(),travel=Math.max(1,box.height-innerHeight+124),progress=Math.max(0,Math.min(1,(124-box.top)/travel));bar.style.width=`${progress*100}%`;}}
  function queue(){if(!queued){queued=true;requestAnimationFrame(readingPosition);}}
  addEventListener('scroll',queue,{passive:true});addEventListener('resize',queue);document.addEventListener('toggle',queue,true);readingPosition();
  document.querySelector('[data-show-toc]')?.addEventListener('click',()=>{const compact=document.querySelector('.compact-toc');if(compact){compact.open=true;compact.scrollIntoView({block:'start',behavior:'instant'});compact.querySelector('summary')?.focus();}});
  const filter=document.querySelector('#term-filter'),termCount=document.querySelector('#term-count');
  filter?.addEventListener('input',()=>{const query=filter.value.trim().toLowerCase();let visible=0;document.querySelectorAll('.term-entry').forEach(term=>{const show=term.textContent.toLowerCase().includes(query);term.hidden=!show;if(show)visible++;});document.querySelectorAll('.term-group').forEach(group=>group.hidden=!group.querySelector('.term-entry:not([hidden])'));if(termCount)termCount.textContent=`${visible} / 180語`;queue();});
})();
