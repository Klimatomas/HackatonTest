"""
Vzor řešení najdeš tady: https://repl.it/DZyw

Představ si, že vyvíjíš seznamovací portál. Portál zároveň vyvíjíš a sám na sobě testuješ jako uživatel. Do systému zadávej
 svoje údaje dle následujících instrukcí:
- Napiš kód, který bude vyžadovat rok tvého narození (např. 1993) - na jeho základě vygeneruj kolik je ti let.
- Zaveď podmínku, která říká, že zbytek kódu mohou vykonat jen ti, kteří mají 18 a více let. Pokud je ti méně než 18,
 vnech program vygenerovat větu "nebylo ti 18"
- Je potřeba, aby se program zeptal na tvoje pohlaví.
- Na portále je také potřeba vystupovat pod svým jménem. Zadejte tedy do programu svoje jméno a následně svoje příjmení.
- Portál by měl vytvořit tvoje uživatelské jméno. To uděláš funkcí, která ho ze tvého jména a příjemní
vygeneruje - použij první 3 znaky tvého jména a první 3 znaky tvého příjmení.
Nakonec už jenom zbývá vygenerovat welcome zprávu typu "vítej na seznamce, vaše přihlašovací jméno je: "<username>"
Pod uvítací zprávou bude výzva navázaná na tvoje pohlaví. Pokud jsi muž, nech program vypsat větu "jsem sexy
kodér a umím to se šroubovákem". Pokud jsi žena, nech program vypsat větu "kromě kódování umím i vařit".
Pokud nejsi ani muž ani žena, vypiš větu "osoby s pohlavím <pohlaví> najdeš v IT"
"""

import datetime
import json
import psycopg2


class Users:
    def __init__(self, year_of_birth, gender, name, surname, nickname):
        config = json.load(open('config.json'))
        self.con = psycopg2.connect(database=config["db"], user=config["user"])
        print(self.con)
        self.cur = self.con.cursor()
        self.year_of_birth = year_of_birth
        self.gender = gender
        self.name = name
        self.surname = surname
        self.nickname = nickname
        self.greeting()

    def greeting(self):
        print("vítej na seznamce, vaše přihlašovací jméno je: {}".format(self.nickname))
        if self.gender == "muž":
            print("jsem sexy kodér a umím to se šroubovákem")
        elif self.gender == "žena":
            print("kromě kódování umím i vařit")
        else:
            print("osoby s pohlavím {} najdeš v IT".format(self.gender))
        self.add_to_db()

    def add_to_db(self):
        query = "INSERT INTO Users (name, surname, nickname, year) VALUES (%s, %s, %s, %s);"
        data = (self.name, self.surname, self.nickname, self.year_of_birth)
        self.cur.execute(query, data)
        self.con.commit()


def create_user():
    year_of_birth = int(input("zadej rok narození"))
    now = datetime.datetime.now().year
    if now - year_of_birth < 18:
        print("nebylo ti 18")
    else:
        gender = input("zadej pohlaví")
        name = input("zadej své jméno")
        surname = input("zadej své příjmení")
        nickname = name[:3] + surname[:3]
        Users(year_of_birth, gender, name, surname, nickname)


create_user()
