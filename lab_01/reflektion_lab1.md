1. Vad tror Du vi har för skäl till att spara det skrapade datat i JSON-format?
  * Slippa skrapa sajten varje gång man vill ha tillgång till datan. JSON är ett enkelt och bra format att arbeta med,
  används av öppna API:er

2. Olika jämförelsesiter är flitiga användare av webbskrapor. Kan du komma på fler typer av tillämplingar där webbskrapor förekommer?
  * Google? Statistik, sno information från konkurrenter.

3. Hur har du i din skrapning underlättat för serverägaren?
  * Indentifierat skrapan, lagt in time.sleep() så man inte "pressar" sajten för mycket.

4. Vilka etiska aspekter bör man fundera kring vid webbskrapning?
  * Läsa "Terms of service", fråga om lov, följa robots.txt det vill säga inte skrapa sidor som ägaren inte vill att man ska skrapa.
  * Försöka att inte "pressa" sajten man skrapar för mycket.

5. Vad finns det för risker med applikationer som innefattar automatisk skrapning av webbsidor? Nämn minst ett par stycken!
  * Skrapa information som inte "får" komma ut.
  * Finns risker att HTML-strukturen kan ändras

6. Tänk dig att du skulle skrapa en sida gjord i ASP.NET WebForms. Vad för extra problem skulle man kunna få då?
  * Varje anrop kräver att man skickar med extra information för att behålla "state:n".

7. Välj ut två punkter kring din kod du tycker är värd att diskutera vid redovisningen. Det kan röra val du gjort, tekniska lösningar eller lösningar du inte är riktigt nöjd med.
  * Hur man kan skarpa vilken sida som helst och följa länkar (paging) utan att ange url?
  * Kolla i urlen för att skilja på om det verkligen är en kurs, program etc.

8. Hitta ett rättsfall som handlar om webbskrapning. Redogör kort för detta.
  * Intressant rättsfall http://out-law.com/page-10975.
  Två konkurrenter, det ena företag vill ha tillgång till en databas om bildelar till Mitsubishi. Företaget som vill ha tillgång till databasen skulle få betala för att få använda en databas som ett företag fört in via kataloger och dylikt. De valde istället att skrapa hemsidan på de uppgifterna och på så sätt få tillgång till databasen. Företaget som hade databasen fick sin hemsida krashad på grund av skrapandet. Det sades också att det var Mitsubishi som givit inloggningsuppgifter till konkurrenten så att de kunde skrapa hemsidan på dess databas.

9. Känner du att du lärt dig något av denna uppgift?
  * Ja, jag har lärt mig mycket och det har varit intressant och roligt.
  Trevligt och ganska så klurigt att gå igenom så pass många länkar samt att utföra en inloggning via ett skript.