# Pieter Verhoef
# Webapplicatie voor raadplegen student database

from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Deze functie is voor de startpagina van de website.
    Hierbij kan iemand vanuit de webapplicatie inloggen in de studenten
    database en hierbij worden de berichten van studenten uit de
    database opgehaald, het is ook mogelijk om te zoeken op een specifiek
    woord in een bericht.
    """

    # Na klikken op de verzend button.
    if request.method == 'POST':

        gebruikersnaam = request.form["gebruikersnaam"]
        wachtwoord = request.form["wachtwoord"]

        try:
            # Maak connectie met de gebruikersnaam en het wachtwoord
            # dat ingevuld is in het formulier.
            connectie = mysql.connector.connect(
            host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database."
                 "azure.com",
            user=gebruikersnaam, db="arcgc",
            password=wachtwoord)
        # Fout bij het maken van connectie (gebruikersnaam of wachtwoord
        #                                    verkeer)
        except mysql.connector.Error as e:

            return render_template("index.html", bericht="Foutieve combinatie"
                                                         " van gebruikersnaam"
                                                         " en wachtwoord")

        # Combinatie van gebruikersnaam en wachtwoord is correct
        else:

            cursor = connectie.cursor()
            zoekwoord = request.form["zoekwoord"]
            # Zoekwoord ingevuld
            if zoekwoord != '':
                cursor.execute("select s.voornaam, p.datum, p.tijd, p.bericht "
                               "from piep p join student s on p.student_nr ="
                               " s.student_nr where bericht LIKE "
                               "concat('%', %s, '%')"
                               "order by 2 desc, 3 desc", (zoekwoord,))
            # Zoekwoord niet ingevuld
            else:
                cursor.execute("select s.voornaam, p.datum, p.tijd, p.bericht "
                               "from piep p join student s on p.student_nr ="
                               " s.student_nr")

            return render_template("index.html", cursor=cursor,
                                   bericht=None)

    else:
        return render_template("index.html", bericht=None)


if __name__ == '__main__':
    app.run()
