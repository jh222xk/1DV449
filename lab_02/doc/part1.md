# Del 1 - Säkerhetsproblem

## Problem
1. Man kan logga in utan ett giltigt användarnamn och lösenord.
2. Man kan komma åt sidor som ska kräva inloggning utan att vara inloggad.
3. Lösenorden är inte hashade.
4. Man kan sno sessions.
5. Man kan komma åt data utan att göra requests via ajax... (Kanske inget stort problem egentligen).

## Skada
1. Man kan posta meddelanden utan att vara inloggad.
2. "Speciella" sidor kan kommas åt utan en säker inloggning.
3. Om man får tag i databasen så står lösenorden i klartext, otur om man har samma lösenord fler hemsidor.
4. Om man får tag i sessions-kakan så kan man logga in och på så sätt få åtkomst till sidor som man inte ska komma åt.
5. Komma åt data som inte är avsett för "människor".

## Åtgärder
1. Kollar nu verkligen om vi hittar en valid user med ett lösenord som tillhör användarnamnet.
2. Kollar nu om en session finns med det inloggad användarnamnet.
3. Har nu ett hashat lösenord i databasen som vi sedan kollar om det överensstämmer när vi försöker logga in.
4. Har lagt in IP + User-Agent så det kollas när vi ska loggas in.
5. Har lagt in en funktion som kollar om requesten verkligen är en ajax request.