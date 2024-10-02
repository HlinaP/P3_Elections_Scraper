# P3_Elections_Scraper // Volby do Poslanecké sněmovny z roku 2017
Python skript slouží k získání výsledků voleb přímo z webu volby.cz, které jsou ukládány do formátu CSV.  
Data obsahují výsledky za všechny obce vybraného okresu, přesněji kód a název obce, počet registrovaných
voličů, vydané obálky, platné hlasy a počet získaných hlasů pro jednotlivé politické strany.

## Požadavky
K tomu, aby skript správně fungoval je potřeba nainstalovat následující knihovny:
   - `requests`
   - `beautifulsoup4`
   - `re`
   - `csv`

Knihovny je možné snadno nainstalovat pomocí příkazu:
```  
pip install -r requirements.txt
```

## Použití
Skript potřebuje jeden název skriptu a dva argumenty na spuštění:  
**Skript_name**: webscraping.py  
**URL**: zvoleného okresu z webu volby.cz , např. "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6105"  
**Output_filename**: název výstupního CSV souboru, např. "vysledky_ZR" 

## Syntaxe
```
python <skript_name.py> <url> <output_filename>
```
## Příklad využití
```
python webscraping.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6105" "vysledky_ZR.csv"
```
#### Poznámka
Při spouštění v příkazovém řádku Windows je nutné využívat dvojité **" "** , nikoliv jednoduché **' '**
## Funkce
Skript je rozdělen do několika funkcí pro různé části procesu – získání obcí, získání volebních výsledků a export do CSV.
Výsledný soubor CSV by měl obsahovat následující informace:  
  - kód obce  
  - název obce  
  - počet voličů  
  - počet vydaných obálek  
  - počet platných hlasů  
  - strany a jejich získaný počet hlasů
## Chování programu
Během stahování dat uživatel vidí, které obce jsou momentálně stahovány.  
V rámci programu jsou ošetřeny chyby při 
zadání špatné URL adresy, zaměnění argumentů, případně špatné zvolení formátu výstupního souboru. Skript také zahlásí chybu v 
případě, že zadaná adresa není přístupná. 
## Očekáváný výstup
```
Connection was successful.
Data for the selected district has been successfully downloaded.
Data has been successfully exported to the file vysledky.csv.
```
Vygenerovaný soubor ve formátu CSV.
```
code,municipality,registered,envelopes,valid,strana1,strana2,strana3,...
532568,Bernartice,191,148,148,4,0,0,...
530743,Bílkovice,170,121,118,7,0,0,...
```
