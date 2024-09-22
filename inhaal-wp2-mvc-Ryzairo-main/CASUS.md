# Werkplaats 2 2023 - Event Calendar

# Inleiding
Dit document beschrijft de casus die je kunt maken als inhaalopdracht voor WP2. Deze opdracht is kleiner dan de oorspronkelijke opdracht, maar bevat wel alle leerdoelen uit WP2. Hou er rekening mee dat je deze opdracht individueel moet maken.

> [!IMPORTANT]
> De deadline voor inleveren is gesteld op vrijdag 15 maart 2024. Je vindt de vereisten voor inleveren onderaan dit document. 

# De opdracht
We gaan een evenementenagenda maken die op een andere website ingesloten kan worden. Het idee is dat de agenda alle evenementen laat zien die nog gaan komen en dat een bezoeker kan doorklikken om meer details te vragen. Gebruikers met toegang tot de applicatie zelf kunnen agenda's en evenementen toevoegen, aanpassen en verwijderen. Daarnaast is er een admin die nieuwe gebruikers kan aanmaken en verwijderen.

Thema's en technieken in deze opdracht:
- Scrum stories schrijven
- HTML & CSS
- Flask (routing)
- Datum / tijd afhandeling in Python
- SQL
- MVC
- CRUD


# Vereisten 

De lijst met vereisten is opgesteld per rol. Je kunt deze lijst ook meteen beschouwen als geprioriteerd qua functionaliteiten - maak dus eerst alle eisen rondom *bezoekers*, daarna rondom *gebruikers* en begin als laatste aan de *admin* en de *extra doelen*.  

De applicatie moet de volgende elementen bevatten:

### Bezoekers
- Bezoekers landen op een pagina met evenementen. Bijvoorbeeld "/agenda/mijnfeestjes", of "/agenda/feestzaaldelft". Er kunnen dus meerdere agenda's zijn beschikbaar op "/agenda/<een_agenda_naam>". Als er een niet bestaande agenda wordt opgevraagd wordt een heldere foutmelding getoond. 
- Bij openen van de agenda toont de applicatie de titel van de agenda en de komende 20 aankomende evenementen. Je ziet hier per evenement alleen de naam van het evenement, de datum en de naam van de locatie. Zie bijvoorbeeld onderstaand screenshot:

![example_calendar.png](docs%2Fimages%2Fexample_calendar.png)!

- Er is onderaan de lijst met evenementen een optie om de volgende 20 evenementen te tonen (er komen er dan 40 in totaal te staan).
- Indien een bezoeker op een evenement klikt, komt hij op een pagina met meer informatie over het evenement. Hier staat buiten de eerdere zaken een kleine beschrijving van het evenement, de aanmelder van het evenement, de datum en hoe laat het evenement start en eindigt.
- Er is een eigen ontworpen huisstijl, die simpel is en een beperkt aantal "classes" bevat. Het kan zijn dat er een "overschrijvende" style sheet URL wordt aangegeven in de instellingen van de agenda. Als dat het geval is moet de eigen huisstijl worden gebruikt, anders de standaard huisstijl.
 
### Gebruikers

Gebruikers zijn mensen die kunnen inloggen op de applicatie. Ze kunnen dan agenda's aanmaken en evenementen toevoegen, aanpassen en verwijderen.

- In eerste instantie, als er een willekeurige pagina wordt geopend zonder dat de gebruiker is ingelogd wordt deze doorgestuurd naar een login pagina. Na succesvol inloggen met gebruikersnaam en wachtwoord wordt de index pagina getoond. 
- Als iemand de standaard index URL van de applicatie ("/") opent, wordt er een overzicht getoond met alle agenda's - met hun titel en de "/agenda/<agenda naam>" hyperlink. De gebruiker kan doorklikken op een agenda om evenementen in die agenda te tonen, of een nieuwe agenda aanmaken, of de agenda URL te openen op dezelfde manier als een bezoeker zou doen. 
- Als de gebruiker kiest om een nieuwe agenda aan te maken wordt een formulier getoond. Hier kan men een titel, een naam voor de URL en optioneel een style sheet URL worden meegeven. Na opslaan wordt de gebruiker terug gestuurd naar de pagina met alle agenda's. 
- De gebruiker kan ook de evenementen in een agenda bekijken. Hier worden alle aankomende evenementen getoond en anders dan voor bezoekers: per evenement de optie om deze aan te passen of te verwijderen. Er is een link terug naar de pagina met alle agenda's en een knop om een nieuw evenement aan te maken.
- Bij een nieuw evenement moet de gebruiker de naam, datum, starttijd en eindtijd, locatie, beschrijving en aanmelder opgeven. Gebruik voor de start- en eindtijd het HTML input type `time` en voor de datum het HTML input type `date`. 

### Admin
- Als een gebruiker de admin rol heeft (de "is_admin" kolom in de database) is er na inloggen een extra link naar een admin pagina.
- Op deze pagina kan de admin nieuwe gebruikers aanmaken (met usernaam, scherm naam en wachtwoord) en bestaande gebruikers verwijderen. Bij het aanmaken van een gebruiker kun je aangeven of deze gebruiker ook een admin is.

### Extra doelen
Er zijn een paar requirements die we graag willen zien en bijdragen aan een betere beoordeling:
- Agendas zouden gekoppeld moeten zijn aan gebruikers. Een gebruiker kan dan alleen de agenda's zien die hij heeft aangemaakt en zou geen andere agenda's of bijbehorende evenementen moeten kunnen aanpassen. Uitzondering daarop is een gebruiker met de admin vlag. Je zult hier het databasescript voor moeten aanpassen omdat we nu nog niet bijhouden welke gebruiker een agenda heeft aangemaakt.
- Er zijn geen filtervelden aangegeven voor de evenementen. Het zou mooi zijn als bezoekers en gebruikers via een filter evenementen kunnen selecteren op de datum, de locatie en de aanmelder.
- Bezoekers zullen vooral via mobiele apparaten gebruik maken van de agenda. De evenementen lijst zou "responsive" moeten zijn, zodat deze goed werkt op mobiel. Dit bereik je het snelst door het gebruik van Bootstrap en een grid systeem.

# Technische vereisten
### Stories
Eén van de leerdoelen van Werkplaats 2 is om kennis te maken met Scrum. Als individu heeft het scrum proces geen toegevoegde waarde, maar het opsplitsen in stories wel. We verwachten dat je de vereisten uitschrijft in kleinere stories en deze stories in Github issues plaatst. Mocht je een andere manier willen gebruiken om stories op te slaan, zorg dan bij inleveren voor een export in de repo in de vorm van een goed leesbare PDF.

### Database generator
Dit repository bevat een database generator. Dit is een Python script dat een SQLite database aanmaakt en vult met test data. Het script is te vinden in de `lib/database` folder. Start dit script vanuit jouw ontwikkeltool of met "python lib/database/database_generator.py". Het script maakt een database aan met de naam `event_calendar.db` in de `databases` folder. Het staat je vrij om dit script aan te passen waar nodig. 

De database verwijst naar het maken van een lijst op basis van een datum. Mocht je nog niet met de combinatie SQLite en Python gewerkt hebben, er staat een klein voorbeeld in de list_demo_events functie in het database generator script. 

### Techniek
We verwachten dat je de volgende technieken gebruikt:
- Een Flask webserver om Python code, de database en routes bij elkaar te brengen.
- HTML pagina's gegenereerd met behulp van Jinja templates. 
- Het rechtstreeks raadplegen van de database met behulp van SQL queries (..dus geen ORM).
- Zolang bovenstaande doelen geraakt worden staat het je vrij om andere technieken te gebruiken(zoals javascript en CSS libraries). Als je de moeite neemt om een nieuwe techniek te leren en toe te passen - en aan alle vereisten is voldaan - wegen we deze mee in de beoordeling. 

### Code kwaliteit
We verwachten dat je de volgende code kwaliteitseisen hanteert:
- De code moet in een Git repository staan. We verwachten dat je de code regelmatig commit en dat je duidelijke commit messages gebruikt. 
- De code moet in een virtual environment draaien. We verwachten dat je een `requirements.txt` bestand gebruikt om de benodigde Python packages te installeren.
- De code moet voldoen aan de PEP8 standaard. Gebruik een linter om dit te controleren.
- De code moet het MVC-patroon volgen. Database gebruik in eigen functies en HTML alleen in Flask templates. We willen *geen* SQL-code terug zien in dezelfde module als de Flask routes. 

# Beoordeling
We beoordelen je werk op twee manieren: we kijken naar de code en naar de opgeleverde applicatie. We verwachten dat alle schermen goed werken en dat je zover als mogelijk bent gekomen in de gegeven requirements.

Voor de techniek kijken we of aan de gevraagde *technische eisen* is voldaan. Buiten de zaken aldaar verwachten we dat je aan de algemene eisen van de werkplaats voldoet:  
- Is er genoeg inzet te zien?
- Is de code authentiek (dat wil zeggen, zelf geschreven)? 
- Volg je de regels voor het vermijden van spaghetti code?

Voor de beoordeling volgen we vuistregels. 
- Een product dat aan alle requirements voldoet en waarvan de code aan de bovenstaande eisen voldoet beoordelen we als "goed". 
- Indien er significante uitbreiding is op de eisen, dan beoordelen we dat als "uitstekend".
- Een project waarbij aan één van de code eisen of requirements niet is voldaan beoordelen we als "voldoende". 


# Inleveren

Lever de opdracht in voor de gestelde deadline. Je mag voor die tijd om feedback vragen als je niet zeker weet of jouw werk voldoende is.

We verwachten dan:

    Een repository met daarin:
        een v1.0 tag
        een event kalender applicatie die voldoet aan de eisen
        een README.md met daarin:
            een verwijzing naar de uitgeschreven stories 
            uitleg over hoe te starten in een virtual environment
            een bronnenlijst met geraadpleegde bronnen

Lever je werk in door een berichtje te sturen naar docent Mark op Teams.
