from flask import Flask, render_template, jsonify, request, redirect, url_for, flash

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

#Loads template for user display
@app.route("/stats/<player_id>")
def results(player_id):
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sf6scraper"
    )
    mycursor = mydb.cursor(dictionary=True)

    mycursor.execute("SELECT * FROM users WHERE player_id = %s", (player_id,))
    userdata = mycursor.fetchone()

    if userdata:
        username = userdata['username']
        avgmr_100 = userdata['avgmr_100']
        avgmr_10 = userdata['avgmr_10']
        matchcount = userdata['matchcount']
    else:
        username = None
        avgmr_100 = None
        avgmr_10 = None
        matchcount = None

    if not userdata:
        flash("No matches found for the player.")
        return redirect(url_for("index"))
    
    return render_template('stats.html', player_id=player_id, username=username, avgmr_100=avgmr_100, avgmr_10=avgmr_10, matchcount=matchcount)

# Information about the characters you've fought
@app.route("/characters/<player_id>")
def characters(player_id):
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sf6scraper"
    )
    mycursor = mydb.cursor(dictionary=True)
    
    # Query matches for the player
    mycursor.execute("SELECT * FROM users WHERE player_id = %s", (player_id,))
    userdata = mycursor.fetchone()

    if userdata:
        username = userdata['username']
        matchcount = userdata['matchcount']
    else:
        username = None
        matchcount = None

    if not userdata:
        flash("No matches found for the player.")
        return redirect(url_for("index"))
    
    return render_template('characters.html', player_id=player_id, username=username, matchcount=matchcount)

# Information about the characters you've fought
@app.route("/matches/<player_id>")
def matches(player_id):
    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sf6scraper"
    )
    mycursor = mydb.cursor(dictionary=True)
    
    mycursor.execute("SELECT * FROM users WHERE player_id = %s", (player_id,))
    userdata = mycursor.fetchone()

    mycursor.execute("SELECT * FROM matches WHERE player_id = %s", (player_id,))
    matches = mycursor.fetchall()

    if userdata:
        username = userdata['username']
        matchcount = userdata['matchcount']
    else:
        username = None
        matchcount = None

    if not userdata:
        flash("No matches found for the player.")
        return redirect(url_for("index"))
    
    return render_template('matches.html', player_id=player_id, matches=matches, username=username, matchcount=matchcount)

# Format JSON stuff for AJAX
@app.route('/data/<player_id>/<query_type>')
def get_data(player_id, query_type):
    import mysql.connector

    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sf6scraper"
    )
    mycursor = mydb.cursor(dictionary=True)

    # Define queries for different chart types
    if query_type == "line_chart":
        query = """
        WITH resolved_username AS (
            SELECT username
            FROM users
            WHERE player_id = %s
        )
        SELECT m.id, m.player1_mr AS mr
        FROM matches m
        WHERE m.player1_username = (SELECT username FROM resolved_username) and player_id = %s
        UNION
        SELECT m.id, m.player2_mr AS mr
        FROM matches m
        WHERE m.player2_username = (SELECT username FROM resolved_username) and player_id = %s
        ORDER BY id desc;
        """
        mycursor.execute(query, (player_id, player_id, player_id))
    elif query_type == "pie_chart":
        query = """
        WITH resolved_username AS (
            SELECT username
            FROM users
            WHERE player_id = %s
        ),
        limited_matches AS (
            SELECT *
            FROM matches
            WHERE 
                player1_username = (SELECT username FROM resolved_username)
                OR player2_username = (SELECT username FROM resolved_username)
            ORDER BY id ASC
            LIMIT 100
        ),
        opponent_characters AS (
            SELECT 
                CASE 
                    WHEN m.player1_username = (SELECT username FROM resolved_username) THEN m.player2_character
                    WHEN m.player2_username = (SELECT username FROM resolved_username) THEN m.player1_character
                END AS opponent_character
            FROM limited_matches m
        )
        SELECT opponent_character, COUNT(*) AS count
        FROM opponent_characters
        WHERE opponent_character IS NOT NULL
        GROUP BY opponent_character
        ORDER BY count DESC;
        """
        mycursor.execute(query, (player_id,))
    else:
        return jsonify({"error": "Invalid query type"}), 400

    # Fetch and return the data
    data = mycursor.fetchall()

    # Close database connections
    mycursor.close()
    mydb.close()

    return jsonify(data)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
