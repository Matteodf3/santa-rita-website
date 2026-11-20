(function(){
const KEY='santarita.cart.v1';
function load(){try{const x=JSON.parse(localStorage.getItem(KEY)||'[]');return Array.isArray(x)?x:[]}catch(e){return []}}
function save(items){try{localStorage.setItem(KEY,JSON.stringify(items));document.dispatchEvent(new Event('cart-change'));return true}catch(e){return false}}
function add(item){const items=load();item.id=Date.now().toString(36)+Math.random().toString(36).slice(2,8);item.qty=1;items.push(item);return save(items)}
function remove(id){return save(load().filter(x=>x.id!==id))}
function quantity(id,n){return save(load().map(x=>x.id===id?{...x,qty:Math.max(1,Math.min(99,Number(n)||1))}:x))}
function count(){return load().reduce((n,x)=>n+(Number(x.qty)||1),0)}
function updateBadges(){document.querySelectorAll('[data-cart-count]').forEach(e=>e.textContent=count())}
document.addEventListener('cart-change',updateBadges);window.addEventListener('storage',updateBadges);if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',updateBadges);else updateBadges();window.SantaCart={load,save,add,remove,quantity,count};
})();