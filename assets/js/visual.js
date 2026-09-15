/* Progressive enhancement; no remote code services, credentials or execution emulation. */
(() => {
  'use strict';
  const panel=document.querySelector('.glossary-panel'),rail=document.querySelector('.glossary-rail');
  const media=matchMedia('(max-width:1180px)');
  function setTermMode(){if(panel)panel.open=!media.matches;}
  setTermMode();media.addEventListener('change',setTermMode);
  const reading=document.querySelector('.reading-position');
  if(reading&&panel){
    const button=document.createElement('button');button.type='button';button.className='terms-toggle';button.textContent='用語';button.setAttribute('aria-controls','page-terms');button.setAttribute('aria-expanded',String(panel.open));
    button.addEventListener('click',()=>{panel.open=!panel.open;button.setAttribute('aria-expanded',String(panel.open));if(panel.open)rail?.scrollIntoView({block:'start',behavior:'instant'});});
    reading.insertBefore(button,reading.querySelector('.reading-track'));panel.addEventListener('toggle',()=>button.setAttribute('aria-expanded',String(panel.open)));
    if(location.hash.startsWith('#local-term-'))panel.open=true;
  }
  document.addEventListener('click',event=>{
    const button=event.target.closest('[data-download-draft]');if(!button)return;
    const input=document.getElementById(button.dataset.downloadDraft);if(!(input instanceof HTMLTextAreaElement))return;
    const url=URL.createObjectURL(new Blob([input.value],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download=`Lesson${document.body.dataset.lesson||''}-${input.id}.cs`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  document.addEventListener('keydown',event=>{
    const dialog=document.querySelector('#search-dialog');
    if(event.key==='Escape'&&dialog?.open){event.preventDefault();dialog.close();}
  });
  // Tab keeps its standard keyboard-focus behavior.
})();
