(function(){
const KEY='santarita.language.v1',supported=['da','it','en'];
function valid(value){return supported.includes(value)?value:'da'}
function browserLanguage(){const languages=navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||'da'];for(const value of languages){const base=String(value).toLowerCase().split(/[-_]/)[0];if(supported.includes(base))return base}return 'da'}
window.SantaLanguage={get(){try{const saved=localStorage.getItem(KEY);if(supported.includes(saved))return saved}catch(e){}return browserLanguage()},set:valid,choose(language){const value=valid(language);try{localStorage.setItem(KEY,value)}catch(e){}return value}};
function labels(){const language=document.documentElement.lang;
const words={da:{restaurantSubtitle:'Italiensk restaurant · Horsens',country:'Danmark',illustrativePhotos:'Illustrationsfotos:',wine:'Vin',basket:'Gavekurv',photos:'Fotos:'},it:{restaurantSubtitle:'Ristorante italiano · Horsens',country:'Danimarca',illustrativePhotos:'Foto illustrative:',wine:'Vino',basket:'Cesto regalo',photos:'Foto:'},en:{restaurantSubtitle:'Italian restaurant · Horsens',country:'Denmark',illustrativePhotos:'Illustrative photos:',wine:'Wine',basket:'Gift basket',photos:'Photos:'}};
document.querySelectorAll('[data-site-text]').forEach(e=>{const value=(words[language]||words.da)[e.dataset.siteText];if(value)e.textContent=value});
document.querySelectorAll('[data-cart-label]').forEach(e=>e.textContent=language==='en'?'Basket':language==='it'?'Carrello':'Kurv');document.querySelectorAll('[data-language-select]').forEach(e=>{e.value=language;e.setAttribute('aria-label',language==='en'?'Website language':language==='it'?'Lingua del sito':'Hjemmesidens sprog')})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',labels);else labels();new MutationObserver(labels).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
})();
