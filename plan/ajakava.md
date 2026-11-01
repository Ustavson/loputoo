# Bakalaureusetöö ajakava

**Autor:** Karl-Ustav Kõlar
**Teema (töönimi):** Tartu linnaruumi 3D-maailma loomine Gaussi splattimise (*3D Gaussian Splatting*) meetodil
**Juhendajad:** _[täita]_
**Koostatud:** 01.11.2026. Ajakava vaadatakse üle igal juhendajakohtumisel.

---

## 1. Kindlad tähtajad

| Kuupäev | Mis | Märkus |
|---|---|---|
| 07.10.2026 (K) | Esimene kohtumine juhendajatega | toimunud |
| **02.11.2026 (E)** | **Teema ja juhendaja(te) registreerimine** | instituudi tähtaeg |
| 04.11.2026 (K) | Juhendajakohtumine | |
| 16.11.2026 (E) | Lugemisülesanne (EBSCO Discovery, refereerimine) Moodle'isse | LTAT.01.004 |
| 08.12.2026 (T) | Refereeriv tekst (lõputöö osa), mustand Moodle'isse | LTAT.01.004 |
| 08.01.2027 (R) | Refereeriv tekst, lõppversioon | LTAT.01.004 |
| 12.05.2027 (K) | Lõputöö esitamine (thesis.cs.ut.ee) | kevadine kaitsmisvoor |
| 04.–11.06.2027 | Lõputöö kaitsmine (täpne päev selgub) | 10-minutiline ettekanne, kohapeal |

**Juhendajakohtumised** toimuvad üle nädala kolmapäeviti:
04.11 · 18.11 · 02.12 · 16.12 · 30.12 (pühade tõttu tõenäoliselt ära) · 13.01 · 27.01 · 10.02 · 24.02 · 10.03 · 24.03 · 07.04 · 21.04 · 05.05 · 19.05 · 02.06

---

## 2. Lahtised küsimused ja kuidas ajakava nendega arvestab

| Küsimus | Seis | Mõju ajakavale |
|---|---|---|
| Kas filmime Tartu ise või kasutame olemasolevaid andmeid? | Juhendajad ootavad vastuseid | Ajakavas on kaks stsenaariumit (A ja B, vt etapp 5). |
| Kui filmime ise, siis millal? | Teadmata | Vt allpool filmimise ajaaknaid. |
| Kus mudeleid treenin? | Selgitada 04.11 | gsplat vajab NVIDIA (CUDA) GPU-d. Kui oma arvutis seda pole, on vaja ligipääsu nt TÜ HPC keskuse klastrile. |
| Kaitsmise täpne päev | Selgub kevadel | Kaitsmiseks valmistun 04.06 seisuga. |

**Põhimõte:** kõik, mis andmetest ei sõltu, teen ära enne andmete otsust: kirjanduse ülevaate, teooria ning töövoo ehitamise ja testimise avalike andmestike ja enda testvõtetega. Nii ei jää töö ootamise taha seisma.

**Andmete otsuse sihttähtaeg on 13.01.2027 kohtumine.** Kui otsust ka 24.02 kohtumiseks pole, teen juhendajatele ettepaneku filmida ise piiratud ala (nt üks väljak või tänavalõik). See hoiab töö teostatavana.

**Filmimise ajaaknad Tartus (kui filmime ise):**
- **november–veebruar:** päevavalgust on vähe (detsembris u 6 h) ning lumi ja märjad pinnad muudavad stseeni. Sobib ainult proovivõteteks.
- **märtsi lõpp – aprill:** lumi on sulanud ja puudel pole veel lehti, seega jääb hooneid vähem varju. **See on parim aken.** Filmida tuleks **hiljemalt 15.04**, et rekonstrueerimiseks ja tulemuste kirjutamiseks jääks enne 12.05 aega.

---

## 3. Ajakava etappide kaupa

### Etapp 0. Idee ja ettevalmistus (september–oktoober 2026). Tehtud.
- Lõputöö idee ja juhendajad on olemas, esimene kohtumine toimus 07.10.
- Tutvusin teemaga ja lugesin sissejuhatavat kirjandust.
- Lõin mobiilirakendusega Scaniverse esimesed katselised maailmad.

### Etapp 1. Projekti käivitamine (01.11–04.11)
- [x] Projekti baas: git-hoidla, kaustastruktuur, LaTeX-i põhi, uurimislogi (01.11)
- [x] Ajakava (01.11)
- [ ] Teema ja juhendajate registreerimine (**02.11**)
- [ ] Scaniverse: rohkem ruume ja pikemad videod
- [ ] gsplat: paigaldamine ja esimene treening
- **Väljund:** 04.11 kohtumisel näitan Scaniverse'i ja gsplat'i tulemusi ning ajakava.

### Etapp 2. Kirjandusotsing ja lugemisülesanne (05.11–16.11)
- [ ] EBSCO Discovery otsingud (vähemalt 2), otsingute võrdlus ja analüüs
- [ ] Refereering (150–200 sõna, ≥2 allikat) koos viidete ja kuvatõmmistega
- [ ] **Lugemisülesande esitamine 15.11** (üks päev enne tähtaega)
- [ ] Kirjanduse koondtabel (`notes/`): allikas, põhiidee, seos minu tööga
- [ ] Katsed gsplat'iga jätkuvad
- **Väljund:** 18.11 kohtumisel lepin juhendajatega kokku, millise lõputöö osa refereeriva tekstina kirjutan, ja näitan selle kava.

### Etapp 3. Refereeriv tekst: lõputöö osa (17.11–08.12)
- [ ] Laen alla instituudi LaTeX-malli ja viin lõputöö põhja sellele üle
- [ ] Valitud osa: **teoreetiline ülevaade** (Gaussi splattimine, NeRF, *structure-from-motion*). See osa ei sõltu andmete otsusest.
- [ ] Kohustuslikud osad: teema ja juhendaja; töö eesmärk ja probleemipüstitus koos taustaga; kaaskiri (milline osa ja mille kohta tagasisidet soovin); osa ise (u 6000 tm koos tühikutega, ≥3 allikat, refereeringud integreeritud oma teksti); kirjanduse loetelu
- [ ] Kirjutan eesti keeles. Kui lõputöö tuleb ingliskeelne, täidab see ühtlasi nõutud ≥2 lk eestikeelse teksti ning seda saab hiljem kasutada eestikeelse kokkuvõtte jaoks.
- [ ] **02.12 kohtumisel** annan mustandi juhendajatele
- [ ] **Esitamine 07.12** Moodle'isse, Google'i dokumendina kommenteerimisõigusega (üks päev enne tähtaega)

### Etapp 4. Tagasiside ja töövoo ehitamine (09.12.2026–08.01.2027)
- [ ] Parandan teksti kursuse ja juhendajate tagasiside põhjal, **lõppversiooni esitamine 07.01**
- [ ] Töövoog: video → kaadrid → SfM (COLMAP) → gsplat → vaatur. Testin avaliku andmestiku ja oma testvõttega.
- [ ] Hindamise mõõdikud (PSNR, SSIM, LPIPS) ja katsete dokumenteerimise kord (`experiments/`)
- 16.12 kohtumine; 24.–27.12 puhkus (puhver)

### Etapp 5. Andmed ja metoodika (09.01–28.02.2027)
- [ ] **13.01: andmete otsus** (sihttähtaeg)
- **Stsenaarium A, olemasolevad andmed:** andmete hankimine, kvaliteedi hindamine ja eeltöötlus jaanuaris–veebruaris
- **Stsenaarium B, filmime ise:** filmimisplaan (alad, marsruut, seadmed, seaded) ja proovivõtted jaanuaris–veebruaris; põhifilmimine märtsis–aprillis (hiljemalt 15.04)
- [ ] Taustapeatükk: refereerivat teksti laiendades, **juhendajatele 10.02**
- [ ] Metoodika peatüki mustand, **juhendajatele 24.02**

### Etapp 6. Rekonstrueerimine ja tulemused (01.03–21.04.2027)
- [ ] Tartu alade rekonstrueerimine, katsed ja nende võrdlus
- [ ] Alade kokkupanek ühtseks maailmaks ja vaatur
- [ ] Tulemuste peatüki mustand, **juhendajatele 07.04**
- [ ] **21.04: terviklik mustand juhendajatele** (3 nädalat enne esitamist)

### Etapp 7. Viimistlemine ja esitamine (22.04–12.05.2027)
- [ ] Kokkuvõte (järeldused, piirangud, soovitused edasisteks uuringuteks)
- [ ] Sissejuhatus (kirjutan viimasena)
- [ ] Teisekeelne kokkuvõte, keeleline toimetamine ja viitamise kontroll
- [ ] Lisad (kood, link vaaturile), infoleht koos CERCS-koodiga, lihtlitsents
- [ ] 05.05 kohtumine: juhendajate viimane läbivaatus
- [ ] **Esitamine 11.05** (üks päev enne tähtaega) aadressil thesis.cs.ut.ee, fail `perekonnanimi_õppekava_aasta.pdf`

### Etapp 8. Kaitsmine (13.05–11.06.2027)
- [ ] 10-minutiline ettekanne ja demo (lend läbi Tartu maailma)
- [ ] Vastused retsensendi küsimustele
- [ ] Ettekande proov juhendajatega (19.05 või 02.06)
- [ ] **Kaitsmine 04.–11.06.2027**

---

## 4. Lähieesmärgid SMART-meetodil (01.11–08.12.2026)

S – spetsiifiline, M – mõõdetav, A – saavutatav, R – realistlik, T – ajaliselt piiritletud.

| # | S: mida täpselt | M: mille järgi mõõdan | A: kuidas saavutan | R: miks see aitab | T: tähtaeg ja ajakulu |
|---|---|---|---|---|---|
| 1 | Registreerin lõputöö teema ja juhendajad | Vorm on esitatud | Täidan instituudi registreerimisvormi | Kohustuslik eeldus kaitsmisele pääsemiseks | 02.11, 15 min |
| 2 | Teen Scaniverse'iga uusi katseid | 3 uut ruumi + 1 vähemalt 2-minutiline video. Igaühe kohta märge logis: kestus, nähtavad vead | Filmin telefoniga ja võrdlen lühikese ja pika video tulemust | Selgub, kuidas video pikkus ja katvus kvaliteeti mõjutavad. Sellest saab hilisema filmimisjuhendi alus | 03.11, 3 h |
| 3 | Paigaldan gsplat'i ja treenin esimese stseeni | 1 treenitud stseen, 1 renderdatud pilt ja selle PSNR | Kasutan gsplat'i näidisskripti avaliku testandmestikuga; kui GPU-d pole, selgitan välja ligipääsu | Töövoo esimene toimiv samm, mida 04.11 juhendajatele näidata | 03.11, 4 h |
| 4 | Teen lugemisülesande otsingud EBSCO Discoverys | 2 päringut otsinguajaloos, ≥5 teemakohast kirjet, ½ lk otsingute võrdlust | Kasutan Advanced Searchi: sünonüümid OR-iga ühel real, read AND-iga, piirangud (aeg, märksõnad) | Leitud allikaid kasutan ka detsembri refereerivas tekstis | 10.11, 2 h |
| 5 | Kirjutan lugemisülesande refereeringu | 1 lõik, 150–200 sõna, ≥2 allikat, tekstisisesed viited, kirjanduse loetelu, kuvatõmmised | Loen allikad läbi, panen põhimõtted märkmetesse ja kirjutan märkmete, mitte originaalteksti põhjal | Harjutan refereerimist enne pikemat teksti | 14.11: 2 h lugemist + 1 h kirjutamist; esitamine 15.11 |
| 6 | Koostan refereeriva teksti kava | 3–5 alapealkirja, igaühe juures 1–2 allikat, kokku ≥5 allikat | Valin koondtabelist allikad, mis katavad teoreetilise ülevaate | Selge kava võimaldab juhendajatel suuna enne kirjutamist kinnitada | 18.11 kohtumiseks, 3 h |
| 7 | Kirjutan refereeriva teksti põhiosa | 6000 tm: 3 kirjutamiskorda × u 2000 tm | Iga kord: 1 h allikate ülevaatamist + 1,5 h kirjutamist; kirjutamiskorrad 22.11, 26.11, 29.11 | Täidab kursuse ülesande ja on lõputöö taustapeatüki mustand | 29.11, kokku u 7,5 h |
| 8 | Kirjutan eesmärgi, probleemipüstituse ja kaaskirja | Eesmärk + probleem u 1000 tm; kaaskiri 3–5 lauset | Kirjutan olemasoleva põhiosa ja juhendajatega arutatu põhjal | Kohustuslikud osad; kaaskiri suunab tagasiside sinna, kus seda kõige rohkem vajan | 01.12, 2 h; juhendajatele 02.12; Moodle'isse 07.12 |

**Edasi:** iga juhendajakohtumise järel sõnastan järgmise kahe nädala lähieesmärgid samas vormis ja kannan need uurimislogisse (`LOG.md`).
