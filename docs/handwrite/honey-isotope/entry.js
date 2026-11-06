/* Extend only slide 21; the deck's slide order and existing activities remain. */
(()=>{'use strict';
const script=document.currentScript,link=new URL('index.html',script.src).href;
const slide=[...document.querySelectorAll('.slide')][20];
if(!slide||!slide.querySelector('h2')?.textContent.includes('蜂蜜'))return;
// Clarify the visible sentence without discarding the original source snapshot.
const walker=document.createTreeWalker(slide,NodeFilter.SHOW_TEXT);let node;
while((node=walker.nextNode()))if(node.textContent.includes('兩者的差距,就是摻假的量。'))node.textContent=node.textContent.replace('兩者的差距,就是摻假的量。','差距還要和C4糖端點比較，才能估算摻入比例。');
const p=document.createElement('p');p.className='honey-animation-entry';p.innerHTML='<a href="'+link+'">▶ 蜂蜜同位素動畫實驗：一步一步學</a><span>先預測方向，再拖曳比例，最後才看公式。</span>';slide.appendChild(p);
const style=document.createElement('style');style.textContent='.honey-animation-entry{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:14px 0 0;font-size:17px;line-height:1.5}.honey-animation-entry a{display:inline-block;color:#fff;background:#266553;border-radius:7px;padding:9px 15px;text-decoration:none}.honey-animation-entry span{color:#52676c}.honey-animation-entry a:focus-visible{outline:3px solid #bd851e;outline-offset:3px}body.scroll .honey-animation-entry{font-size:16px}';document.head.appendChild(style);
})();
