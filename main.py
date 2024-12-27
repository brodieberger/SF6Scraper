from flask import Flask, render_template, request, redirect, url_for, flash
from scraper import scrapesite # type: ignore
import mysql.connector
import userpasswords

app = Flask(__name__)
app.secret_key = userpasswords.supersecretkey

#start web app
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        player_id = request.form.get("player_id")
        
        # Validate input
        if not player_id:
            flash("Player ID cannot be empty!")
            return redirect(url_for("index"))
        
        # Connect to database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sf6scraper"
        )
        mycursor = mydb.cursor(dictionary=True)
        
        # Query for matches
        mycursor.execute("SELECT * FROM matches WHERE player_id = %s", (player_id,))
        matches = mycursor.fetchall()
        
        if matches:
            # Redirect to results page if matches exist
            return redirect(url_for("results", player_id=player_id))
        else:
            # Run scraper and populate the database
            scrapesite(player_id)
            return redirect(url_for("results", player_id=player_id))
    
    return render_template("index.html")

@app.route("/results/<player_id>")
def results(player_id):
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sf6scraper"
    )
    mycursor = mydb.cursor(dictionary=True)
    
    # Query matches for the player
    mycursor.execute("SELECT * FROM matches WHERE player_id = %s", (player_id,))
    matches = mycursor.fetchall()
    
    if not matches:
        flash("No matches found for the player.")
        return redirect(url_for("index"))
    
    return render_template("results.html", player_id=player_id, matches=matches)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
