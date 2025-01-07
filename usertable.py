def update_user(player_id):
    import mysql.connector

    # Connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sf6scraper"
    )
    mycursor = mydb.cursor(dictionary=True)

    # Fetch the username
    mycursor.execute("SELECT username FROM users WHERE player_id = %s", (player_id,))
    result = mycursor.fetchone()
    username = result['username'] if result and 'username' in result else None

    if not username:
        print(f"Player with ID {player_id} not found in users table.")
        return

    # Calculate avg MR over 100 games
    mycursor.execute("""
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
        )
        SELECT 
            AVG(
                CASE 
                    WHEN m.player1_username = (SELECT username FROM resolved_username) THEN m.player1_mr
                    WHEN m.player2_username = (SELECT username FROM resolved_username) THEN m.player2_mr
                END
            ) AS avg_mr
        FROM limited_matches m;
    
    """, (player_id,))
    result = mycursor.fetchone()
    averageMR100 = float(result['avg_mr']) if result and result['avg_mr'] else None

    # Calculate avg MR over 10 games
    mycursor.execute("""
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
            LIMIT 10
        )
        SELECT 
            AVG(
                CASE 
                    WHEN m.player1_username = (SELECT username FROM resolved_username) THEN m.player1_mr
                    WHEN m.player2_username = (SELECT username FROM resolved_username) THEN m.player2_mr
                END
            ) AS avg_mr
        FROM limited_matches m;
    
    """, (player_id,))
    result = mycursor.fetchone()
    averageMR10 = float(result['avg_mr']) if result and result['avg_mr'] else None

    # Calculate avg MR over 10 games
    mycursor.execute("SELECT count(id) as matchcount FROM `matches` WHERE player_id = %s", (player_id,))
    result = mycursor.fetchone()
    matchcount = float(result['matchcount']) if result and result['matchcount'] else None

    # Update the users table
    mycursor.execute("""
        UPDATE users
        SET avgmr_100 = %s,
            avgmr_10 = %s,
            matchcount = %s
        WHERE player_id = %s
    """, (averageMR100, averageMR10, matchcount, player_id))

    # Commit the changes
    mydb.commit()

    print(f"Updated player {player_id}: username={username}, mr_100games={averageMR100}, mr_10games={averageMR10}")

    # Close the connection
    mycursor.close()
    mydb.close()
