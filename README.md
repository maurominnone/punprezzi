# Prezzo Luce su GitHub Pages

Questa versione separa la UI dal recupero dati:

- `index.html` legge solo `./data/latest.json`
- `scripts/update-pun.py` scarica i dati da Energy-Charts
- `.github/workflows/update-pun.yml` aggiorna il JSON ogni 30 minuti
- se una zona fallisce, mantiene l'ultimo dato valido
- se falliscono tutte le zone ma esiste un file precedente, conserva il file vecchio e marca `stale: true`

## Come pubblicare

1. Carica tutto il contenuto del progetto nel repository GitHub.
2. Vai in **Settings > Pages**.
3. In **Build and deployment**, scegli **Deploy from a branch**.
4. Seleziona branch `main` e cartella `/(root)`.
5. Vai in **Actions** e abilita i workflow se GitHub te lo chiede.
6. Apri il workflow **Aggiorna dati PUN** e lancia **Run workflow** una prima volta.
7. Quando il workflow ha creato `data/latest.json`, apri il sito pubblicato.

## Struttura

- `index.html`: pagina pubblica
- `data/latest.json`: dataset statico pubblicato da GitHub Pages
- `scripts/update-pun.py`: script di aggiornamento
- `.github/workflows/update-pun.yml`: automazione schedulata
