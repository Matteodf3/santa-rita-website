# Milestone sito pubblico Santa Rita

Aggiornamento: 20/11/2026. Piano corretto secondo le indicazioni dell’utente.
Stato e prove devono distinguere: verificato, confermato dall’utente, da verificare.

## WEB-001 — copia, backup, cronologia e destinazione

- Copia di sviluppo indipendente dalla cartella sul Desktop; backup ZIP iniziale conservato sul PC.
- Repository GitHub privata: https://github.com/Matteodf3/santa-rita-website.
- Nessun deploy automatico; cartella Desktop conservata.
- Destinazione scelta per il sito pubblico: one.com, già utilizzato dall’utente. BOOK resta separato sulla propria VPS.
- Confermare dominio canonico (.dk, con o senza www), accesso al piano one.com e strumenti disponibili per pubblicazione, HTTPS e redirect prima di progettare il rilascio. L’eventuale servizio per ordini/pagamenti sarà deciso separatamente.

**Fatto quando:** backup locale presente e verificato; copia indipendente, repository privata e primo commit disponibili; destinazione one.com registrata e capacità/configurazione dell’hosting verificate. Copia, backup e repository sono già verificati; hosting e dominio canonico restano da verificare.

## WEB-002 — prenotazione e immagini

Stato: implementata nella copia di sviluppo, da verificare su BOOK autenticato. Prove e limiti: [VERIFICA-WEB-002.md](VERIFICA-WEB-002.md).

- Dominio BOOK corretto indicato dall’utente: `https://book.trattoriasantarita.dk`.
- Destinazione prevista: `https://book.trattoriasantarita.dk/book?lang=da`, oppure `?lang=it` e `?lang=en`, secondo la lingua selezionata sul sito. Il supporto del parametro risulta dal codice secondo la segnalazione dell’utente; percorso e comportamento sono da provare nel browser. Non considerare la precedente destinazione .it verificata o confermata.
- Collegare tutti i pulsanti di prenotazione, compresi navigazione, hero, contatti e pagine shop; rimuovere le vecchie finestre di prenotazione dimostrative.
- Rimuovere le strisce di anteprima residue. Non presentare ordini e pagamenti non attivi come funzionanti.
- Estrarre immagini incorporate in HTML e CSS in file separati. Conservare gli originali, produrre varianti ottimizzate e responsive, usare dimensioni esplicite e caricamento differito per immagini fuori schermo.
- La foto principale si carica subito. Misurare il traffico iniziale con cache vuota, senza scorrimento, a viewport 390×844 e 1440×900: HTML, CSS, JavaScript, font e immagini richiesti al caricamento. Obiettivo di accettazione: massimo 500 KiB trasferiti per la home a ciascuna dimensione. Riportare separatamente il peso completo dopo lo scorrimento. Se qualità o vincoli impediscono il limite, proporre una soglia motivata prima di dichiarare conclusa la scheda.

**Fatto quando:** ogni pulsante apre il dominio .dk e mantiene la lingua; provati separatamente da/it/en e registrato l’esito; nessuna striscia residua; immagini responsive con caricamento corretto e misure prima/dopo entro la soglia concordata. Nessuna prenotazione reale necessaria per verificare l’apertura del flusso.

## WEB-003 — tre lingue

- Danese predefinito, italiano e inglese su tutte le pagine.
- Preferenza conservata fra pagine, compresi carrello e shop; tradurre testi, descrizioni, pulsanti, errori ed etichette accessibili.
- La stessa preferenza genera `lang=da`, `lang=it` o `lang=en` nei collegamenti BOOK; non basta tradurre il testo del pulsante.

**Fatto quando:** tutte le pagine controllate nelle tre lingue, nessuna chiave o frase non tradotta involontaria, preferenza conservata dopo navigazione/ricaricamento e BOOK aperto nella lingua giusta per ciascuna scelta.

## WEB-004 — reperibilità, condivisione e aggiornamento dati

- Fonte autorevole degli orari: configurazione BOOK in `/impostazioni`. Il responsabile del ristorante conferma gli orari; l’utente incaricato della gestione del sito li riporta e verifica.
- Quando cambiano: aggiornare prima BOOK, poi orari visibili e dati strutturati del sito; il gestore del profilo Google aggiorna anche gli orari Google Business Profile. Nessuna sincronizzazione automatica va presunta. Annotare responsabile, data e confronto effettuato; accesso a BOOK/VPS solo nel perimetro autorizzato.
- Dati strutturati Restaurant con indirizzo, telefono, orari confermati, menu e prenotazione. Non promettono un migliore posizionamento su Maps.
- Titoli e descrizioni per pagina, Open Graph con immagine, favicon, sitemap, robots, 404; URL canonici coerenti con la destinazione definita in WEB-001.
- Inventario degli indirizzi del vecchio WordPress e mappa dei redirect sull’hosting one.com; i redirect indispensabili per il primo rilascio restano un requisito di WEB-006 anche se questa milestone completa è rinviata.

**Fatto quando:** responsabili degli aggiornamenti identificati; orari confrontati con BOOK e confermati dal ristorante; metadati, link canonici e dati strutturati validati; anteprima di condivisione verificata; sitemap/robots/404 e mappa redirect controllati sul tipo di hosting effettivo.

## WEB-005 — shop e verifica responsive estesa

- Inserire prodotti, prezzi e disponibilità forniti dall’utente; definire costi di confezione, consegna e regole dei buoni.
- Ordini e pagamenti reali richiedono un servizio server, verifiche e configurazioni dedicate; HTTPS da solo non li attiva.
- Controlli browser a 360, 390, 768, 820, 1024 e 1440 pixel, nelle lingue disponibili, con almeno verifica delle soglie navbar 849/850/851 pixel e orientamento tablet.
- Distinguere prove emulate da iPad/telefono fisici; registrare browser, versione, dimensione e risultato. Verificare overflow, immagini, tastiera, form, lingua e persistenza carrello.

**Fatto quando:** prodotti e costi confermati; ordine/ritiro/spedizione e pagamento verificati nell’ambiente di prova scelto; matrice responsive eseguita senza difetti bloccanti e limiti delle prove fisiche dichiarati. Pubblicazione dello shop solo dopo autorizzazione.

## WEB-006 — primo rilascio e ripristino

- L’utente riferisce un backup quotidiano del sito attuale: disponibilità e ripristino non ancora verificati. Non sostituisce il backup prima del rilascio.
- Prima di sostituire il WordPress: esportazione completa di file, caricamenti, temi/plugin e database, scaricata sul PC fuori dal repository; verificare integrità e procedura di ripristino. Il solo export XML WordPress non basta. Conservare eventuali segreti solo nell’archivio protetto.
- Confermare configurazione one.com, DNS, HTTPS, dominio canonico e procedura di pubblicazione già analizzati in WEB-001.
- Preparare e provare i redirect essenziali degli indirizzi precedenti; evitare catene e collegamenti interrotti.
- Verificare diritti fotografici, contatti e orari, menu e prezzi, navigazione, link BOOK e controllo minimo su computer e telefono. Non rinviare questi controlli essenziali alla WEB-005.
- Primo rilascio minimo: WEB-001 + WEB-002 + WEB-006. Le due lingue già presenti devono funzionare; se inglese è ancora assente non mostrarne un selettore non operativo. WEB-003, WEB-004 e WEB-005 possono arrivare dopo, singolarmente.
- Shop/carrello non operativi: escluderli dalla navigazione pubblica del rilascio minimo o mantenerne esplicito lo stato; non pubblicare un acquisto che sembra reale.
- Piano scritto di ritorno al vecchio sito, verifiche subito dopo la pubblicazione e autorizzazione esplicita dell’utente prima del rilascio.

**Fatto quando:** export WordPress completo e recuperabile sul PC; procedura di rollback scritta e verificata; controlli minimi e redirect riusciti; approvazione esplicita registrata; dopo rilascio HTTPS, pagine, menu, contatti e BOOK controllati sull’URL pubblico. Fino ad allora nessun cambiamento a produzione, DNS o hosting.

## Privacy e cookie — decisione di progetto

Nessun tracciamento analitico o pubblicitario previsto; non aggiungere Google Analytics, pixel o altri strumenti di tracciamento senza una decisione esplicita. Attualmente sono previste solo preferenze locali di lingua e carrello. Nessun banner promozionale di consenso viene introdotto in questa fase. Verificare comunque richieste a terzi e informativa privacy prima del rilascio: immagini remote, integrazioni Google, pagamenti o nuove funzionalità possono cambiare i requisiti. La configurazione effettiva e l’informativa sono un controllo di WEB-006.

## Dopo il rilascio

- Il gestore del profilo Google aggiorna il collegamento al sito pubblico e quello alle prenotazioni.
- Il titolare o il gestore autorizzato verifica la proprietà in Google Search Console; inviare sitemap e controllare indicizzazione/redirect quando disponibili.
- Responsabile del ristorante: approva menu, prezzi, disponibilità e orari. Gestore del sito indicato dall’utente: applica gli aggiornamenti e registra la verifica. I nominativi vanno confermati prima del rilascio.
- Monitorare link interrotti, errori, prenotazione e dati di contatto dopo la pubblicazione.

Recensioni Google: componente predisposto, API e fatturazione disattivate. Non assumere una conservazione giornaliera delle recensioni consentita senza verifica delle condizioni applicabili.
