/* Catalogue data is local until a verified product and price source is available.
   null prices mean the product cannot be ordered. Never infer a case price. */
window.SantaWineCatalogue = Object.freeze([
  {id:'cantolio-di-terra', name:'Cantolio 14° di Terra', type:'red', year:null, image:'immagini/vino-cantolio-di-terra.webp', priceDKK:null, casePriceDKK:null, verification:'label'},
  {id:'barone-montalto-nero-davola', name:'Barone Montalto Nero d’Avola', type:'red', year:null, priceDKK:null, casePriceDKK:null, verification:'variant'},
  {id:'la-cacciatora-barolo', name:'La Cacciatora Barolo', type:'red', year:null, priceDKK:null, casePriceDKK:null, verification:'variant'},
  {id:'trerose-salterio-2019', name:'Trerose Salterio', type:'red', year:'2019', image:'immagini/vino-trerose-salterio-2019.webp', priceDKK:null, casePriceDKK:null, verification:'label'},
  {id:'antica-masseria-colleone-primitivo-2019', name:'Antica Masseria Colleone Primitivo Salento', type:'red', year:'2019', priceDKK:null, casePriceDKK:null, verification:'label'},
  {id:'franchini-sedese-2019', name:'Franchini Sedese', type:'red', year:'2019', image:'immagini/vino-franchini-sedese-2019.webp', priceDKK:null, casePriceDKK:null, verification:'label'},
  {id:'via-76-77-primitivo-nero-di-troia-2025', name:'Via 76 / Via 77 Primitivo Nero di Troia', type:'red', year:'2025', priceDKK:null, casePriceDKK:null, verification:'name'},
  {id:'casato-di-melzi-salice-salentino-riserva-2014', name:'Casato di Melzi Salice Salentino Riserva', type:'red', year:'2014', priceDKK:null, casePriceDKK:null, verification:'label'},
  {id:'eghemon-passimento-don-vincenzo-2024', name:'Eghemon Passimento Don Vincenzo', type:'red', year:'2024', image:'immagini/vino-eghemon-passimento-don-vincenzo-2024.webp', priceDKK:null, casePriceDKK:null, verification:'label', badge:'bestseller'},
  {id:'sartori-marani-bianco-veronese-2022', name:'Sartori Marani Bianco Veronese', type:'white', year:'2022', image:'immagini/vino-sartori-marani-bianco-veronese-2022.webp', priceDKK:null, casePriceDKK:null, verification:'label'}
]);
/* Descriptive details: user-supplied vintages and names remain unverified against bottles. */
window.SantaWineDetails={
 'cantolio-di-terra':{producer:'Cantolio',region:'Puglia',source:'https://cantolio.it/prodotto/14-di-terra/'},
 'barone-montalto-nero-davola':{producer:'Barone Montalto',grapes:'Nero d’Avola',source:'user-unverified'},
 'la-cacciatora-barolo':{producer:'La Cacciatora',appellation:'Barolo',source:'user-unverified'},
 'trerose-salterio-2019':{producer:'Tenuta Trerose',grapes:'Sangiovese 95%, Colorino 5%',source:'https://tenutatrerose.it/it/vini/salterio'},
 'antica-masseria-colleone-primitivo-2019':{producer:'Antica Masseria Colleone',region:'Salento',grapes:'Primitivo',source:'user-unverified'},
 'franchini-sedese-2019':{producer:'Franchini',source:'https://www.franchinivini.com/vini/'},
 'via-76-77-primitivo-nero-di-troia-2025':{grapes:'Primitivo, Nero di Troia',source:'user-unverified'},
 'casato-di-melzi-salice-salentino-riserva-2014':{producer:'Casato di Melzi',appellation:'Salice Salentino Riserva',source:'user-unverified'},
 'eghemon-passimento-don-vincenzo-2024':{producer:'Eghemon',source:'user-unverified'},
 'sartori-marani-bianco-veronese-2022':{producer:'Sartori',region:'Verona',appellation:'Bianco Veronese',source:'user-unverified'}
};
