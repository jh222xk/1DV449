# Reflektion

* Vad finns det för krav du måste anpassa dig efter i de olika API:erna?
Caching, inte göra för många requests mot API:erna.

* Hur och hur länga cachar du ditt data för att slippa anropa API:erna i onödan?
Cachar datan i en timme innan vi gör en ny request mot API:erna. Datan är sparad i databasen och efter att en timme har gått så skrivs datan i databasen över när vår nya request görs mot API:erna.

* Vad finns det för risker med din applikation?
Jag litar på datan från SR och Google vilket i säg kanske inte är så bra. Om jag inte får ut någon data från dessa API:er så kommer min applikation dö (eller använda väldigt gammal data).

* Hur har du tänkt kring säkerheten i din applikation?
Meteor publicerar databasen på klienten så att vi kan använda databasen där. I ett fräscht projekt av meteor så kommer den med lite paket som gör applikationen osäker men väldigt enkel att arbeta med. Jag har tagit bort dessa paket och gjort det "the hard way". Paketen i fråga är "autopublish" och "unsecure".

* Hur har du tänkt kring optimeringen i din applikation?
Minifierat och konkatinerat alla javascript & css.
Cachar statiska filer & datan.