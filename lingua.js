(function(){
const KEY='santarita.language.v1',supported=['da','it','en'];
function valid(value){return supported.includes(value)?value:'da'}
function browserLanguage(){const languages=navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||'da'];for(const value of languages){const base=String(value).toLowerCase().split(/[-_]/)[0];if(supported.includes(base))return base}return 'da'}
window.SantaLanguage={get(){try{const saved=localStorage.getItem(KEY);if(supported.includes(saved))return saved}catch(e){}return browserLanguage()},set:valid,choose(language){const value=valid(language);try{localStorage.setItem(KEY,value)}catch(e){}return value}};
const languageNames={da:'Dansk',it:'Italiano',en:'English'};
let pickerId=0;
function enhancePicker(select){
if(select._srPicker||!document.createElement)return;
const wrapper=select.closest('.sr-language-picker');if(!wrapper)return;
const trigger=document.createElement('button'),name=document.createElement('span'),code=document.createElement('span'),panel=document.createElement('div');
trigger.type='button';trigger.className='sr-language-trigger';name.className='sr-language-name';code.className='sr-language-code';code.setAttribute('aria-hidden','true');trigger.append(name,code);
panel.className='sr-language-panel';panel.id='sr-language-panel-'+(++pickerId);panel.hidden=true;panel.setAttribute('role','group');
trigger.setAttribute('aria-controls',panel.id);trigger.setAttribute('aria-expanded','false');
const options=supported.map(language=>{const option=document.createElement('button');option.type='button';option.className='sr-language-option';option.dataset.language=language;option.lang=language;
const title=document.createElement('span'),short=document.createElement('span'),check=document.createElement('span');title.textContent=languageNames[language];short.textContent=language.toUpperCase();short.className='sr-language-code';short.setAttribute('aria-hidden','true');check.className='sr-language-check';check.textContent='✓';check.setAttribute('aria-hidden','true');option.append(title,short,check);panel.append(option);
option.addEventListener('click',()=>{select.value=language;select.dispatchEvent(new Event('change',{bubbles:true}));sync();close(true)});return option});
function close(restore){panel.hidden=true;trigger.setAttribute('aria-expanded','false');if(restore)trigger.focus()}
function open(index){panel.hidden=false;trigger.setAttribute('aria-expanded','true');options[index===undefined?Math.max(0,supported.indexOf(select.value)):index].focus()}
function sync(){const language=valid(select.value),label=select.getAttribute('aria-label')||'Website language';name.textContent=languageNames[language];code.textContent=language.toUpperCase();trigger.setAttribute('aria-label',label+': '+languageNames[language]);panel.setAttribute('aria-label',label);options.forEach(option=>{const current=option.dataset.language===language;option.classList.toggle('is-current',current);if(current)option.setAttribute('aria-current','true');else option.removeAttribute('aria-current')})}
trigger.addEventListener('click',()=>panel.hidden?open():close(false));
wrapper.addEventListener('keydown',event=>{if(event.key==='Escape'&&!panel.hidden){event.preventDefault();close(true)}else if(['ArrowDown','ArrowUp','Home','End'].includes(event.key)){event.preventDefault();const index=options.indexOf(document.activeElement);if(event.key==='Home')open(0);else if(event.key==='End')open(options.length-1);else if(panel.hidden)open();else open((index+(event.key==='ArrowDown'?1:-1)+options.length)%options.length)}});
document.addEventListener('click',event=>{if(!wrapper.contains(event.target))close(false)});
// Safari on iPhone may report a null relatedTarget while a tapped option is
// receiving focus. Close only after focus actually reaches an outside element.
document.addEventListener('focusin',event=>{if(!wrapper.contains(event.target))close(false)});
select.addEventListener('change',sync);select.tabIndex=-1;select.setAttribute('aria-hidden','true');wrapper.append(trigger,panel);wrapper.classList.add('is-enhanced');select._srPicker={sync};sync();
}
function labels(){const language=document.documentElement.lang;
const words={da:{restaurantSubtitle:'Italiensk restaurant · Horsens',country:'Danmark',illustrativePhotos:'Illustrationsfotos:',wine:'Vin',basket:'Gavekurv',photos:'Fotos:'},it:{restaurantSubtitle:'Ristorante italiano · Horsens',country:'Danimarca',illustrativePhotos:'Foto illustrative:',wine:'Vino',basket:'Cesto regalo',photos:'Foto:'},en:{restaurantSubtitle:'Italian restaurant · Horsens',country:'Denmark',illustrativePhotos:'Illustrative photos:',wine:'Wine',basket:'Gift basket',photos:'Photos:'}};
document.querySelectorAll('[data-site-text]').forEach(e=>{const value=(words[language]||words.da)[e.dataset.siteText];if(value)e.textContent=value});
document.querySelectorAll('[data-cart-label]').forEach(e=>e.textContent=language==='en'?'Basket':language==='it'?'Carrello':'Kurv');document.querySelectorAll('[data-language-select]').forEach(e=>{e.value=language;e.setAttribute('aria-label',language==='en'?'Website language':language==='it'?'Lingua del sito':'Hjemmesidens sprog');enhancePicker(e);if(e._srPicker)e._srPicker.sync()})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',labels);else labels();new MutationObserver(labels).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
})();
