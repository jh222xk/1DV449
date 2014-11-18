# Del 2 - Optimering

## Åtgärder
1. Komprimerat och minifierat CSS och Javscript. (Vi hämtar också JS-filerna asynkront).
2. Tog bort JS som inte används, det vill säga bootstrap.js
3. Lägga till cache: true i ajax requestsen.

## Teori kring åtgärderna
1. Det görs fler HTTP-requests desto fler filer man har, därför har jag minifierat och kombinerat JS och CSS så att vi bara behöver göra två HTTP-requests för alla js och css-filerna.
2. Onödigt att ha med "död kod" som gör att browsern måste hämta mer data.
3. Att cacha datan innebär att vi inte hela tiden behöver "pulla" datan hela tiden om den inte är ny.

## Oberservation
1. Några MS snabbare att ladda sidan, istället för många stora filer, en stor fil istället. Ett anrop efter JS och ett efter CSS istället för 3-4 stycken.
2. Ger väl inte jätte mycket egentligen men lite snabbare går det.
3. Ger oss ungefär 100MS snabbare laddning, vilket är mycket bra!

## Reflektion
1. Inte så konstigt i och med att vi bara behöver göra en HTTP-request för JS och en för CSS istället för flera stycken som vi hade innan.
2. Mindre data att hämta = snabbare response.
3. Helt klart att snabbare när vi kan hämta från cachen istället för att göra nya requests för att få tag på gammal data.