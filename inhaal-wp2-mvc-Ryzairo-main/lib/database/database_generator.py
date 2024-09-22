import sqlite3
from datetime import datetime, timedelta
from pathlib import Path


class WP2DatabaseGenerator:
    def __init__(self, database_file, overwrite=False, initial_data=False):
        self.database_file = Path(database_file)
        self.create_initial_data = initial_data
        self.database_overwrite = overwrite
        self.test_file_location()
        self.conn = sqlite3.connect(self.database_file)

    def generate_database(self):
        self.create_table_users()
        self.create_table_agendas()
        self.create_table_events()
        agenda_id = self.create_demo_data()
        self.list_demo_events(agenda_id)

    def create_table_users(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0,
            date_created DATE NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Table users created")

    def create_table_agendas(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS agendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_name TEXT NOT NULL,
            title TEXT NOT NULL,
            external_stylesheet TEXT,
            date_created DATE NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Table agendas created")

    def create_table_events(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            event_date DATE NOT NULL,
            start_time TEXT NOT NULL,            
            end_time TEXT NOT NULL,
            location TEXT NOT NULL,
            agenda_id INTEGER NOT NULL,
            date_created DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agenda_id) REFERENCES agendas (id)
        );
        """
        self.__execute_transaction_statement(create_statement)
        print("✅ Table events created")

    def create_demo_data(self):
        if self.create_initial_data:
            admin_id = self.create_demo_users_and_return_last()
            agenda_id = self.create_demo_agendas_and_return_last()
            self.create_demo_events(agenda_id)
        return agenda_id

    def create_demo_agendas_and_return_last(self):
        create_statement = """
        INSERT INTO agendas (title, url_name)
        VALUES (?, ?);
        """
        list_of_parameters = [
            ("FRANKS Partyagenda", "partyagenda"),
            ("Collegerooster", "collegerooster"),
            ("Dartavonden 2021", "dartavonden"),
            ("Gezellige Bingo Avond", "gezellige-bingo-avond"),
            ("Filmavond: Nederlandse Klassiekers", "filmavond-nederlandse-klassiekers"),
            ("Workshop Schilderen", "workshop-schilderen"),
            ("Optreden Lokale Band", "optreden-lokale-band"),
            ("Boekenclub Bespreking", "boekenclub-bespreking"),
            ("Culinaire Proeverij", "culinaire-proeverij"),
            ("Yoga in het Park", "yoga-in-het-park"),
            ("Vlooienmarkt", "vlooienmarkt"),
            ("Dansworkshop Salsa", "dansworkshop-salsa"),
            ("Lezing: Nederlandse Geschiedenis", "lezing-nederlandse-geschiedenis"),
            ("Kinderactiviteitenmiddag", "kinderactiviteitenmiddag"),
            ("Concert: Nederlandse Folk Muziek", "concert-nederlandse-folk-muziek"),
            ("Kunstmarkt", "kunstmarkt"),
            ("Comedy Avond: Nederlandse Humor", "comedy-avond-nederlandse-humor"),
            ("Fietstocht door Natuurpark", "fietstocht-door-natuurpark"),
            ("Meditatiesessie", "meditatiesessie"),
            ("Lokale Ambachtenmarkt", "lokale-ambachtenmarkt"),
            ("Afsluitend Barbecuefeest", "afsluitend-barbecuefeest"),
            ("Kunstlezing: Moderne Nederlandse Kunst", "kunstlezing-moderne-nederlandse-kunst"),
            ("Wijnproeverij", "wijnproeverij"),
            ("Schrijfworkshop: Nederlandse Literatuur", "schrijfworkshop-nederlandse-literatuur"),
            ("Fototentoonstelling", "fototentoonstelling"),
            ("Kookworkshop: Hollandse Keuken", "kookworkshop-hollandse-keuken"),
            ("Concert: Nederlandstalige Pop", "concert-nederlandstalige-pop"),
            ("Mode Show", "mode-show"),
            ("Fietsclub Avondrit", "fietsclub-avondrit"),
            ("Debatavond: Nederlandse Politiek", "debatavond-nederlandse-politiek"),
            ("Vogelspotexcursie", "vogelspotexcursie"),
            ("Quiz Night: Nederlandse Trivia", "quiz-night-nederlandse-trivia"),
            ("Creatieve Workshop: Delfts Blauw Schilderen", "creatieve-workshop-delfts-blauw-schilderen"),
            ("Bezoek aan Historisch Museum", "bezoek-aan-historisch-museum"),
            ("Schuif-aan-Tafel Dineravond", "schuif-aan-tafel-dineravond"),
            ("Natuurfotografie Workshop", "natuurfotografie-workshop"),
            ("Karaoke Avond: Nederlandstalige Hits", "karaoke-avond-nederlandstalige-hits"),
            ("Wandeltocht door Stadshistorie", "wandeltocht-door-stadshistorie"),
            ("Wandeling markthal", "wandeling-markthal"),
            ("Boswandeling", "boswandeling"),
            ("Karting", "karting")
        ]
        for parameters in list_of_parameters:
            id = self.__execute_transaction_statement(create_statement, parameters)
        print("✅ Demo data agendas created")
        return id

    def create_demo_users_and_return_last(self):
        create_statement = """
        INSERT INTO users (username, password, is_admin)
        VALUES (?, ?, ?);
        """
        list_of_parameters = [
            ("user", "user", 0),
            ("user2", "user2", 0),
            ("admin", "admin", 1),
        ]
        for parameters in list_of_parameters:
            id = self.__execute_transaction_statement(create_statement, parameters)
        print("✅ Demo data users created")
        return id

    def create_demo_events(self, agenda_id):
        create_statement = """
            INSERT INTO events (name, description, event_date, start_time, end_time, location, agenda_id)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """
        today = datetime.now().date()
        thirty_days_future = today + timedelta(days=30)
        fourty_days_future = today + timedelta(days=40)
        list_of_parameters = [
            (
                "Open avond",
                "Vrij darten, de hele avond, iedereen is welkom",
                thirty_days_future,
                "19:00",
                "23:00",
                "Dartcafe de Schorre",
                agenda_id,
            ),
            (
                "10 euro tournooi",
                "Koppels tournooi, voor gevorde darters. Hoofdprijs is een nieuwe telefoon, een krat bier en een taxi naar huis!",
                fourty_days_future,
                "19:00",
                "23:00",
                "Dartcafe de Schorre",
                agenda_id,
            ),
            (
                "Gezellige Bingo Avond",
                "Kom langs voor een avond vol spanning en mooie prijzen!",
                thirty_days_future,
                "18:30",
                "22:30",
                "Buurtcentrum De Ontmoeting",
                agenda_id,
            ),
            (
                "Filmavond: Nederlandse Klassiekers",
                "Geniet van Nederlandse filmklassiekers met gratis popcorn!",
                fourty_days_future,
                "20:00",
                "23:30",
                "Filmhuis De Hoek",
                agenda_id,
            ),
            (
                "Workshop Schilderen",
                "Leer de basis van schilderen met onze ervaren kunstenaar.",
                thirty_days_future,
                "17:30",
                "21:30",
                "Atelier Kunstplezier",
                agenda_id,
            ),
            (
                "Optreden Lokale Band",
                "Een avond vol live muziek met onze getalenteerde lokale band.",
                fourty_days_future,
                "19:30",
                "22:30",
                "Muziekcafé De Notenbalk",
                agenda_id,
            ),
            (
                "Boekenclub Bespreking",
                "Kom meepraten over het laatst gelezen boek in onze gezellige boekenclub.",
                thirty_days_future,
                "18:30",
                "21:45",
                "Bibliotheek De Leesmuur",
                agenda_id,
            ),
            (
                "Culinaire Proeverij",
                "Ontdek nieuwe smaken tijdens onze culinaire proeverij met lokale chefs.",
                fourty_days_future,
                "20:30",
                "23:15",
                "Restaurant De Smaakmaker",
                agenda_id,
            ),
            (
                "Yoga in het Park",
                "Ontspan je geest en lichaam met een verfrissende yogasessie in het park.",
                thirty_days_future,
                "19:15",
                "22:45",
                "Stadspark Zen",
                agenda_id,
            ),
            (
                "Vlooienmarkt",
                "Snuffel rond en vind unieke schatten op onze gezellige vlooienmarkt.",
                fourty_days_future,
                "21:00",
                "23:30",
                "Evenementenhal De Schatzoeker",
                agenda_id,
            ),
            (
                "Dansworkshop Salsa",
                "Leer de basispassen van salsa tijdens onze swingende dansworkshop.",
                thirty_days_future,
                "18:45",
                "22:15",
                "Dansstudio Ritmo",
                agenda_id,
            ),
            (
                "Lezing: Nederlandse Geschiedenis",
                "Een boeiende lezing over de rijke geschiedenis van Nederland door een lokale historicus.",
                fourty_days_future,
                "20:15",
                "23:45",
                "Cultureel Centrum Historica",
                agenda_id,
            ),
            (
                "Kinderactiviteitenmiddag",
                "Een middag vol plezier en activiteiten voor de jongste leden van onze gemeenschap.",
                thirty_days_future,
                "19:30",
                "22:45",
                "Speeltuin De Vrolijke Hoek",
                agenda_id,
            ),
            (
                "Concert: Nederlandse Folk Muziek",
                "Geniet van traditionele Nederlandse folk muziek tijdens ons intieme concert.",
                fourty_days_future,
                "21:15",
                "23:30",
                "Muziekzaal De Melodie",
                agenda_id,
            ),
            (
                "Kunstmarkt",
                "Ontdek lokale kunstenaars en hun prachtige creaties op onze kunstmarkt.",
                thirty_days_future,
                "18:00",
                "22:30",
                "Kunstplein De Verbeelding",
                agenda_id,
            ),
            (
                "Comedy Avond: Nederlandse Humor",
                "Lach de avond weg met onze Nederlandstalige comedians.",
                fourty_days_future,
                "20:30",
                "23:00",
                "Comedy Club De Lachstuip",
                agenda_id,
            ),
            (
                "Fietstocht door Natuurpark",
                "Verken de natuur tijdens een ontspannen fietstocht door ons prachtige natuurpark.",
                thirty_days_future,
                "19:15",
                "22:45",
                "Startpunt Fietspad Natuurlijk Genieten",
                agenda_id,
            ),
            (
                "Meditatiesessie",
                "Vind innerlijke rust en vrede tijdens onze geleide meditatiesessie.",
                fourty_days_future,
                "21:00",
                "23:30",
                "Meditatiecentrum De Stilte",
                agenda_id,
            ),
            (
                "Lokale Ambachtenmarkt",
                "Ontdek ambachtelijke producten en kunstwerken op onze lokale ambachtenmarkt.",
                thirty_days_future,
                "18:45",
                "22:15",
                "Ambachtsplein De Creatieveling",
                agenda_id,
            ),
            (
                "Afsluitend Barbecuefeest",
                "Sluit de maand af met een gezellig barbecuefeest met lekker eten en live muziek.",
                fourty_days_future,
                "20:15",
                "23:45",
                "Barbecueplein De Smaakexplosie",
                agenda_id,
            ),
            (
                "Kunstlezing: Moderne Nederlandse Kunst",
                "Een boeiende lezing over hedendaagse Nederlandse kunstwerken door een gerenommeerde kunstexpert.",
                thirty_days_future,
                "19:30",
                "22:30",
                "Kunstgalerij De Modernist",
                agenda_id,
            ),
            (
                "Wijnproeverij",
                "Proef de beste Nederlandse wijnen tijdens onze exclusieve wijnproeverij.",
                fourty_days_future,
                "20:00",
                "22:30",
                "Wijnkelder De Smaakvolle Druif",
                agenda_id,
            ),
            (
                "Schrijfworkshop: Nederlandse Literatuur",
                "Ontwikkel je schrijfvaardigheden tijdens onze interactieve workshop over Nederlandse literatuur.",
                thirty_days_future,
                "18:30",
                "21:00",
                "Schrijfcafé De Pennenvrucht",
                agenda_id,
            ),
            (
                "Fototentoonstelling",
                "Bewonder prachtige Nederlandse foto's tijdens onze indrukwekkende fototentoonstelling.",
                fourty_days_future,
                "19:30",
                "22:00",
                "Fotogalerij Het Beeld",
                agenda_id,
            ),
            (
                "Kookworkshop: Hollandse Keuken",
                "Leer heerlijke Hollandse gerechten bereiden tijdens onze gezellige kookworkshop.",
                thirty_days_future,
                "19:15",
                "21:45",
                "Kookstudio De Smaakmakerij",
                agenda_id,
            ),
            (
                "Concert: Nederlandstalige Pop",
                "Geniet van Nederlandstalige popmuziek tijdens ons spetterende concert met lokale artiesten.",
                fourty_days_future,
                "20:30",
                "23:15",
                "Concertzaal De Klank",
                agenda_id,
            ),
            (
                "Mode Show",
                "Bekijk de nieuwste Nederlandse modetrends tijdens onze glamoureuze modeshow.",
                thirty_days_future,
                "18:45",
                "22:30",
                "Modepaleis De Stijl",
                agenda_id,
            ),
            (
                "Fietsclub Avondrit",
                "Ga mee op een avondrit met onze fietsclub en ontdek schilderachtige Nederlandse landschappen.",
                fourty_days_future,
                "19:00",
                "21:30",
                "Startpunt Fietspad Natuurschoon",
                agenda_id,
            ),
            (
                "Debatavond: Nederlandse Politiek",
                "Neem deel aan ons interactieve debat over actuele Nederlandse politieke vraagstukken.",
                thirty_days_future,
                "20:00",
                "22:30",
                "Debatcentrum De Stem",
                agenda_id,
            ),
            (
                "Vogelspotexcursie",
                "Verken de diverse Nederlandse vogelsoorten tijdens onze boeiende vogelspotexcursie.",
                fourty_days_future,
                "18:30",
                "21:00",
                "Natuurreservaat Vogelrijk",
                agenda_id,
            ),
            (
                "Quiz Night: Nederlandse Trivia",
                "Test je kennis over Nederland tijdens onze leuke quizavond vol Nederlandse trivia.",
                thirty_days_future,
                "19:30",
                "22:00",
                "Café De Denker",
                agenda_id,
            ),
            (
                "Creatieve Workshop: Delfts Blauw Schilderen",
                "Ontdek de kunst van Delfts Blauw schilderen tijdens onze creatieve workshop.",
                fourty_days_future,
                "20:15",
                "23:00",
                "Creatief Atelier De Blauwe Kwast",
                agenda_id,
            ),
            (
                "Bezoek aan Historisch Museum",
                "Maak een reis door de Nederlandse geschiedenis tijdens ons bezoek aan het Historisch Museum.",
                thirty_days_future,
                "18:45",
                "21:30",
                "Historisch Museum De Tijdreis",
                agenda_id,
            ),
            (
                "Schuif-aan-Tafel Dineravond",
                "Geniet van een heerlijk diner en gezelligheid tijdens onze Schuif-aan-Tafel Dineravond.",
                fourty_days_future,
                "19:00",
                "22:30",
                "Restaurant Tafelgenot",
                agenda_id,
            ),
            (
                "Natuurfotografie Workshop",
                "Leer de kunst van natuurfotografie tijdens onze praktische workshop in de buitenlucht.",
                thirty_days_future,
                "20:00",
                "22:45",
                "Natuurgebied De Groene Oase",
                agenda_id,
            ),
            (
                "Karaoke Avond: Nederlandstalige Hits",
                "Zing mee met je favoriete Nederlandstalige hits tijdens onze gezellige karaoke avond.",
                fourty_days_future,
                "19:30",
                "22:00",
                "Karaokebar De Zangvogel",
                agenda_id,
            ),
            (
                "Wandeltocht door Stadshistorie",
                "Ontdek de rijke historie van de stad tijdens onze boeiende wandeltocht langs historische locaties.",
                thirty_days_future,
                "18:30",
                "21:30",
                "Startpunt Wandelroute Historica",
                agenda_id,
            ),
            (  
                "Wandeling markthal",
                "Wandel door Martkhal!",
                thirty_days_future, 
                "10:00",
                "12:00",
                "Markthal Rottertdam",
                agenda_id,

            ),
            (
                "Boswandeling",
                "Ontdek het bos!",
                thirty_days_future,
                "15:00",
                "19:00",
                "Het Schollebos",
                agenda_id
            
            ),
            (
                "Karting",
                "Race door de banen",
                fourty_days_future,
                "13:00",
                "15:00",
                "GoKart Delft",
                agenda_id,
            ),
           
           
        ]
        self.__execute_many_transaction_statement(create_statement, list_of_parameters)
        print("✅ Demo data events created")

    def list_demo_events(self, agenda_id):
        query = """
            SELECT * FROM agendas WHERE id = ?; 
        """
        agenda_results = self.__execute_query(query, parameters=(agenda_id,))
        agenda_url = agenda_results[0]["url_name"]

        query = """
        SELECT * FROM events WHERE event_date > ? and agenda_id = ?; 
        """
        # We maken hier een datum object aan met de huidige datum.
        today = datetime.now().date()

        # SQLite kan prima overweg met datetime objecten
        events = self.__execute_query(query, parameters=(today, agenda_id))
        print(f"Upcoming demo events in /agenda/{agenda_url}")
        for event in events:
            dict_event = dict(event)
            print(
                f"{dict_event['name']} op {dict_event['event_date']} in {dict_event['location']}"
            )

    def __execute_many_transaction_statement(
        self, create_statement, list_of_parameters=()
    ):
        c = self.conn.cursor()
        c.executemany(create_statement, list_of_parameters)
        self.conn.commit()

    def __execute_transaction_statement(self, create_statement, parameters=()):
        c = self.conn.cursor()
        c.execute(create_statement, parameters)
        self.conn.commit()
        return c.lastrowid

    def __execute_query(self, query, parameters=()):
        c = self.conn.cursor()
        c.row_factory = sqlite3.Row
        c.execute(query, parameters)
        return c.fetchall()

    def test_file_location(self):
        if not self.database_file.parent.exists():
            raise ValueError(
                f"Database file location {self.database_file.parent} does not exist"
            )
        if self.database_file.exists():
            if not self.database_overwrite:
                raise ValueError(
                    f"Database file {self.database_file} already exists, set overwrite=True to overwrite"
                )
            else:
                # Unlink verwijdert een bestand
                self.database_file.unlink()
                print("✅ Database already exists, deleted")
        if not self.database_file.exists():
            try:
                self.database_file.touch()
                print("✅ New database setup")
            except Exception as e:
                raise ValueError(
                    f"Could not create database file {self.database_file} due to error {e}"
                )


if __name__ == "__main__":
    my_path = Path(__file__).parent.resolve()
    project_root = my_path.parent.parent
    # Deze slashes komen uit de "Path" module. Dit is een module die je kan gebruiken
    # om paden te maken. Dit is handig omdat je dan niet zelf hoeft te kijken of je
    # een / (mac) of een \ (windows) moet gebruiken.
    database_path = project_root / "C:/Users/Zairo\Documents/GitHub/inhaal-wp2-mvc-Ryzairo-1/lib/database" / "event_calendar.db"
    database_generator = WP2DatabaseGenerator(
        database_path, overwrite=True, initial_data=True
    )
    database_generator.generate_database()