# tsoha_wetalk

*Tietokannat ja web-ohjelmointi syksy 2023*

**WeTalk keskustelusovellus**

Sovelluksessa pystyy juttelemaan muiden käyttäjien kanssa yksityisesti sekä avoimissa ryhmissä. Käyttäjä voi olla peruskäyttäjä tai ryhmän ylläpitäjä.

Sovelluksen ominaisuuksia (**päivitetty lopullinen palautus**):

- voidaan luoda uusi käyttäjä, joka pystyy kirjautumaan sovellukseen sisään ja ulos
- sovelluksen etusivulla näkyy lista omista keskusteluista, ryhmäkeskusteluista sekä muista käyttäjistä
- käyttäjä voi luoda uuden ryhmän, jolloin hänestä tulee ryhmän ylläpitäjä
    - ylläpitäjänä voi muokata ryhmän nimeä
    - ylläpitäjä voi myös poistaa yksittäisiä viestejä tai koko ryhmän
- käyttäjä voi liittyä listan ryhmiin ja lähettää sinne viestiä
- käyttäjä voi lähettää viestiä muille käyttäjille yksityisesti
- käyttäjän sivuilta
    - pääsee aloittamaan chatin tai pääsee jo luotuun chattiin linkin kautta
    - näkee listan ryhmistä, joissa kyseinen käyttäjä on
- yläpalkista pääsee etusivulle, ryhmiin, käyttäjiin, chatteihin (kirjautuneena), kirjautumaan sisään/ulos ja rekisteröitymään

## Välipalautus 2

Sovelluksen toiminallisuudet:
- käyttäjä pystyy rekisteröitymään ja kirjautumaan sisään, mitkä vievät etusivulle
- etusivuilta löytyy lista ryhmistä
- etusivulta pääsee
    - omaan profiiliin, mistä pääsee kirjautumaan ulos
    - luomaan uuden ryhmän
    - liittymään ryhmään
    - ryhmäsivuille (vielä ei ole tarkistusta, onko käyttäjä ryhmän jäsen)
- ryhmäsivuilta pääsee lähettämään ryhmään viestin

## Välipalautus 3

Sovelluksen toiminnallisuudet (viime palautuksen lisäksi):
- etusivulta löytyy listat
    - ryhmistä
    - yksityiskeskusteluista (joihin täytyy lisätä jokin tunniste miten listataan)
    - käyttäjistä
- kirjautuneena näitä painamalla pääsee
    - ryhmissä ryhmäsivulle, jos on jäsen ja jos ei ole, pääsee liittymään
    - keskustelulinkistä ei vielä pääse mihinkään
    - käyttäjistä pääsee käyttäjän sivulle, jossa
        - linkki ksityiskeskustelusivulle, jossa voi laittaa viestiä
        - lista ryhmistä missä käyttäjä on (ei vielä näy)

## Käynnistys

- kloonataan repositorio (git clone git@github.com:eveliinaalikoski/tsoha_wetalk.git)
- luodaan kansio .env, jonne määritetään oma SECRET_KEY ja DATABASE_URL
- avataan virtuaaliympäristö
    - (python3 -m venv venv)
    - (source venv/bin/activate)
- asennetaan riippuvuudet (pip install -r requirements.txt)
- luodaan tietokanta komennolla (psql < schema.sql)
- käynnistetään sovellus komennolla (flask run)