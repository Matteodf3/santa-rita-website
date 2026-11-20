(function(){
function update(){const lang=['da','it','en'].includes(document.documentElement.lang)?document.documentElement.lang:'da';document.querySelectorAll('[data-booking-link]').forEach(a=>{a.href='https://book.trattoriasantarita.dk/book?lang='+lang})}
new MutationObserver(update).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});update();
})();
