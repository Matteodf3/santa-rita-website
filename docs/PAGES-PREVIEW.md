# Anteprima GitHub Pages separata

La sorgente resta nel branch di sviluppo. Il sito di produzione `https://trattoriasantarita.dk` resta su one.com. BOOK resta su `book.trattoriasantarita.dk`. L'anteprima prevista è `https://matteodf3.github.io/santa-rita-website/` e viene pubblicata manualmente dal branch `gh-pages` nella radice `/` di quel branch. Nessun workflow automatico, CNAME o cambio DNS.

## Preparare e controllare il pacchetto

Da questa repository:

```powershell
py -3 scripts/build-pages-preview.py
py -3 tests/pages_preview.py
```

Il risultato è nella cartella ignorata `.pages-preview/`. Il test ricostruisce il pacchetto e controlla file ammessi, risorse locali, URL, metadati e firme comuni di segreti. Copiare **il contenuto** di quella cartella nella radice del branch orfano `gh-pages` in un worktree dedicato; poi fare commit e push espliciti di quel branch. Per un aggiornamento, ricostruire e sostituire il contenuto del branch `gh-pages` con il nuovo pacchetto, quindi commit e push espliciti. Nel repository GitHub configurare Pages con sorgente `Deploy from a branch`, branch `gh-pages`, cartella `/ (root)`. Verificare l'URL dopo la pubblicazione.

Il pacchetto contiene solo otto HTML, dieci JS/CSS richiesti, le immagini effettivamente referenziate, `.nojekyll` e `robots.txt`. Esclude sorgenti originali delle foto, documenti, script di build, test, dati JSON, sitemap di produzione e file locali. I link assoluti interni sono adattati a `/santa-rita-website/`; canonical e metadati OG usano l'URL di anteprima. Tutti gli HTML hanno `noindex,nofollow` e lo schema Restaurant è rimosso. `robots.txt` permette la scansione per rendere visibile il `noindex`; su un percorso di progetto il suo ambito può essere limitato. L'assenza dall'indice non è garantita. BOOK continua a puntare al dominio esterno.

Prima di pubblicare o aggiornare, controllare il diff del pacchetto e il suo contenuto: la repository e l'anteprima sono pubbliche. Dopo la pubblicazione, provare navigazione, lingua, immagini, 404 e BOOK nelle tre lingue sul sito remoto. Non interpretare il `noindex` come protezione di informazioni riservate.
