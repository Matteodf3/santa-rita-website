(function(){
const KEY='santarita.language.v1';
window.SantaLanguage={get(){try{return localStorage.getItem(KEY)==='it'?'it':'da'}catch(e){return 'da'}},set(language){const value=language==='it'?'it':'da';try{localStorage.setItem(KEY,value)}catch(e){}return value}};
function labels(){document.querySelectorAll('[data-cart-label]').forEach(e=>{e.textContent=document.documentElement.lang==='it'?'Carrello':'Kurv'})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',labels);else labels();
new MutationObserver(labels).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
})();