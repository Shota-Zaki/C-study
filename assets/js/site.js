/* C# Learning Lab — v2 learning-data compatible. Drafts are never executed. */
(() => {
  'use strict';
  const KEY = 'cstudy.learning.v2', MAX = 524288;
  const M = window.CSTUDY_META || {lessonIds: [], exerciseKeys: [], questionCounts: {}};
  const validLessons = new Set(M.lessonIds), validExercises = new Set(M.exerciseKeys);
  const fresh = () => ({version:2, updatedAt:new Date().toISOString(), theme:'system', completed:[], review:[], quiz:{}, drafts:{}, lastLesson:null});
  let pendingWarning = '', storageReadFailed = false;
  function warn(message) {
    pendingWarning = message;
    const box = document.querySelector('[data-storage-warning]');
    if (box) { box.textContent = message; box.hidden = !message; }
  }
  function validate(v, fromStorage=false) {
    const bad = error => ({ok:false,error});
    if(v==null) return fromStorage?{ok:true,value:fresh()}:bad('JSONオブジェクトが必要です');
    if(typeof v!=='object'||Array.isArray(v))return bad('最上位はオブジェクトです');
    if(v.version!==2)return bad('versionは2である必要があります');
    if(!['light','dark','system'].includes(v.theme))return bad('themeが不正です');
    for(const k of ['completed','review']) {
      if(!Array.isArray(v[k])||v[k].some(x=>typeof x!=='string'||!validLessons.has(x)))return bad(k+'のレッスンIDが不正です');
      if(new Set(v[k]).size!==v[k].length)return bad(k+'に重複があります');
    }
    if(v.lastLesson!==null&&(typeof v.lastLesson!=='string'||!validLessons.has(v.lastLesson)))return bad('lastLessonが不正です');
    if(typeof v.quiz!=='object'||v.quiz===null||Array.isArray(v.quiz))return bad('quizが不正です');
    for(const [id,q] of Object.entries(v.quiz)) {
      if(!validLessons.has(id)||typeof q!=='object'||q===null||!Array.isArray(q.answers))return bad('quizの構造が不正です');
      const count=M.questionCounts[id]??5;
      if(q.answers.length>count||q.answers.some(x=>x!==null&&(!Number.isInteger(x)||x<0||x>3)))return bad('quizの回答が不正です');
      if('score' in q&&(!Number.isInteger(q.score)||q.score<0||q.score>count))return bad('quizのスコアが不正です');
    }
    if(typeof v.drafts!=='object'||v.drafts===null||Array.isArray(v.drafts))return bad('draftsが不正です');
    let total=0;
    for(const [key,value] of Object.entries(v.drafts)) {
      if(!validExercises.has(key)||typeof value!=='string'||value.length>100000)return bad('下書きのキーまたは長さが不正です');
      total+=value.length;
    }
    if(total>400000)return bad('保存用の下書きデータが大きすぎます');
    return {ok:true,value:{version:2,updatedAt:typeof v.updatedAt==='string'?v.updatedAt:new Date().toISOString(),theme:v.theme,completed:[...v.completed],review:[...v.review],quiz:v.quiz,drafts:v.drafts,lastLesson:v.lastLesson}};
  }
  function load() {
    try {
      const raw=localStorage.getItem(KEY), parsed=validate(JSON.parse(raw||'null'),true);
      if(parsed.ok)return parsed.value;
      storageReadFailed=true;warn('保存済みデータを読み込めませんでした。元のデータは上書きせず保持します。設定画面から正しいバックアップを読み込んでください。');
    } catch { storageReadFailed=true;warn('ブラウザーの保存データを読み込めません。元のデータは上書きせず保持します。下書きはコピーして保管し、設定で正常なバックアップを読み込んでください。'); }
    return fresh();
  }
  let state=load();
  function updateProgress() {
    const total=M.lessonIds.length||32;
    document.querySelectorAll('[data-progress-text]').forEach(x=>x.textContent=`${state.completed.length} / ${total}`);
    document.querySelectorAll('[data-progress-bar]').forEach(x=>x.style.width=`${Math.round(state.completed.length/total*100)}%`);
    document.querySelectorAll('[data-complete]').forEach(b=>{const yes=state.completed.includes(b.dataset.complete);b.setAttribute('aria-pressed',String(yes));b.textContent=yes?'✓ 完了済み':'完了にする';});
    document.querySelectorAll('[data-review]').forEach(b=>{const yes=state.review.includes(b.dataset.review);b.setAttribute('aria-pressed',String(yes));b.textContent=yes?'★ 復習対象':'☆ 復習マーク';});
  }
  function save() {
    if(storageReadFailed){warn('元の保存データを保護するため、上書き保存を止めています。下書きをコピーして保管し、設定から正常なバックアップを読み込んでください。');updateProgress();return false;}
    state.updatedAt=new Date().toISOString();
    try {
      const checked=validate(state);
      if(!checked.ok)throw new Error(checked.error);
      const json=JSON.stringify(state);
      if(new TextEncoder().encode(json).length>MAX)throw new Error('保存用JSONが512 KiBを超えています');
      localStorage.setItem(KEY,json);warn('');updateProgress();return true;
    } catch(error) {
      warn('端末へ保存できませんでした。現在の入力はこの画面にあります。下書きをコピーするか、設定で書き出して保管してください。'+(error instanceof Error?' '+error.message:''));
      updateProgress();return false;
    }
  }
  const media=matchMedia('(prefers-color-scheme: dark)');
  function applyTheme(){document.documentElement.dataset.theme=state.theme==='system'?(media.matches?'dark':'light'):state.theme;document.querySelectorAll('[data-theme-label]').forEach(x=>x.textContent=state.theme);}
  applyTheme();updateProgress();media.addEventListener?.('change',()=>{if(state.theme==='system')applyTheme();});
  document.addEventListener('DOMContentLoaded',()=>warn(pendingWarning));
  async function copyCode(button) {
    const text=button.closest('.codebox')?.querySelector('code')?.textContent||''; const initial=button.textContent;
    try {
      if(navigator.clipboard?.writeText&&window.isSecureContext)await navigator.clipboard.writeText(text);
      else {
        const t=document.createElement('textarea');t.value=text;t.style.position='fixed';t.style.top='-9999px';document.body.append(t);t.select();
        const ok=document.execCommand('copy');t.remove();button.focus();if(!ok)throw new Error('copy unavailable');
      }
      button.textContent='コピー済み';
    } catch { button.textContent='手動で選択してコピー'; }
    setTimeout(()=>button.textContent=initial,1600);
  }
  document.addEventListener('click',event=>{
    const b=event.target.closest('button');if(!b)return;
    if(b.dataset.complete){const id=b.dataset.complete;state.completed=state.completed.includes(id)?state.completed.filter(x=>x!==id):[...state.completed,id];save();}
    if(b.dataset.review){const id=b.dataset.review;state.review=state.review.includes(id)?state.review.filter(x=>x!==id):[...state.review,id];save();}
    if(b.matches('[data-copy]'))void copyCode(b);
  });
  const pendingDrafts=new Map();
  function commitDraft(t){const key=t.dataset.draft;state.drafts[key]=t.value;const ok=save(),message=t.parentElement.querySelector('[data-draft-status]');if(message)message.textContent=ok?'下書きを端末へ保存済み':'未保存：保存領域を確認し、下書きをコピーしてください';}
  document.querySelectorAll('textarea[data-draft]').forEach(t=>{
    if(state.drafts[t.dataset.draft]!=null)t.value=state.drafts[t.dataset.draft];
    t.addEventListener('input',()=>{clearTimeout(pendingDrafts.get(t));const label=t.parentElement.querySelector('[data-draft-status]');if(label)label.textContent='下書きの変更あり';pendingDrafts.set(t,setTimeout(()=>{pendingDrafts.delete(t);commitDraft(t);},250));});
  });
  const flush=()=>{for(const [t,timer] of pendingDrafts){clearTimeout(timer);commitDraft(t);}pendingDrafts.clear();};
  addEventListener('pagehide',flush);document.addEventListener('visibilitychange',()=>{if(document.hidden)flush();});
  const lesson=document.body.dataset.lesson;
  if(lesson) {
    state.lastLesson=lesson;save();const answers=state.quiz[lesson]?.answers||[];
    document.querySelectorAll('.question').forEach((q,i)=>{if(Number.isInteger(answers[i])){const r=q.querySelector(`input[value="${answers[i]}"]`);if(r)r.checked=true;}});
    document.querySelector('[data-grade]')?.addEventListener('click',()=>{
      let score=0;const answers=[];
      document.querySelectorAll('.question').forEach(q=>{
        const chosen=q.querySelector('input:checked'),a=chosen?Number(chosen.value):null,correct=Number(q.dataset.answer);answers.push(a);q.classList.add('graded');
        q.querySelectorAll('.choice').forEach((c,j)=>{c.classList.toggle('correct',j===correct);c.classList.toggle('wrong',a===j&&j!==correct);});if(a===correct)score++;
      });
      state.quiz[lesson]={answers,score};const saved=save(),result=document.querySelector('[data-quiz-result]');
      if(result)result.textContent=`確認問題：${score} / ${answers.length} 正解。全選択肢の解説を表示しました。`+(saved?'':' 回答結果は端末へ未保存です。');
    });
  }
  const dialog=document.querySelector('#search-dialog'),input=dialog?.querySelector('input'),results=dialog?.querySelector('[data-search-results]');
  function refreshSearch(){if(!results||!input)return;const query=input.value.trim().toLowerCase(),base=document.body.dataset.base||'';const items=(window.CSTUDY_SEARCH_INDEX||[]).filter(x=>!query||(`${x.title} ${x.text}`).toLowerCase().includes(query)).slice(0,30);results.replaceChildren();for(const x of items){const a=document.createElement('a');a.className='search-result';a.href=base+x.url;const title=document.createElement('strong');title.textContent=x.title;const label=document.createElement('small');label.textContent=({lesson:'本編・演習・確認問題',detail:'詳細解説',guide:'補助教材・用語集',project:'制作課題・学習入口'})[x.kind]||'教材';a.append(title,label);results.append(a);}if(!items.length){const p=document.createElement('p');p.textContent='該当する教材がありません。別の用語で検索してください。';results.append(p);}}
  function openSearch(){dialog?.showModal();refreshSearch();input?.focus();}
  document.querySelectorAll('[data-open-search]').forEach(b=>b.addEventListener('click',openSearch));input?.addEventListener('input',refreshSearch);
  document.addEventListener('keydown',event=>{if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='k'){event.preventDefault();openSearch();}else if(event.key==='/'&&!/input|textarea|select/i.test(document.activeElement?.tagName||'')){event.preventDefault();openSearch();}});
  const selector=document.querySelector('[data-theme-select]');if(selector){selector.value=state.theme;selector.addEventListener('change',()=>{state.theme=selector.value;applyTheme();save();});}
  document.querySelector('[data-export]')?.addEventListener('click',()=>{flush();const blob=new Blob([JSON.stringify(state)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='cstudy-learning-data.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);});
  const importer=document.querySelector('[data-import]'),message=document.querySelector('[data-import-message]');
  importer?.addEventListener('change',async()=>{
    const file=importer.files?.[0];if(!file)return;if(file.size>MAX){message.textContent='読み込み失敗：512 KiBを超えています。現在のデータは維持しました。';return;}
    let parsed;try{parsed=JSON.parse(await file.text());}catch{message.textContent='読み込み失敗：JSONとして解析できません。現在のデータは維持しました。';return;}
    const checked=validate(parsed);if(!checked.ok){message.textContent='読み込み失敗：'+checked.error+'。現在のデータは維持しました。';return;}
    const previous=state,previousReadFailed=storageReadFailed;state=checked.value;storageReadFailed=false;if(!save()){state=previous;storageReadFailed=previousReadFailed;updateProgress();message.textContent='読み込み失敗：端末へ保存できません。現在のデータは維持しました。';return;}
    applyTheme();message.textContent='学習データを読み込みました。';setTimeout(()=>location.reload(),350);
  });
})();
