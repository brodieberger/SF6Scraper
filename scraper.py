def scrapesite(user_input):
    from playwright.sync_api import sync_playwright
    import mysql.connector
    import usertable
    import userpasswords  # This file contains the username and password for the CAPCOM account. (Buckler's Bootcamp)


    print("Input recieved, running playwright")
    with sync_playwright() as p:
        user_URL = f"https://www.streetfighter.com/6/buckler/auth/loginep?redirect_url=/profile/{user_input}/battlelog/rank"

        browser = p.chromium.launch(
            #remove comment for use on pythonplaywright
            #executable_path="/usr/bin/chromium",
            args=["--disable-gpu", "--no-sandbox","--headless"]
        )
        
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page()

        page.goto(user_URL)

        page.wait_for_timeout(500)

        # Enter username and password and click submit
        email_field = page.locator("input[type='email']")
        email_field.fill(userpasswords.emailfill)
        pw_field = page.locator("input[type='password']")
        pw_field.fill(userpasswords.passwordfill)
        page.locator("button[name='submit']").click()

        # Wait for the page to load
        page.wait_for_timeout(4000)

        mydb = mysql.connector.connect(host=userpasswords.host, user=userpasswords.user, password=userpasswords.password, database=userpasswords.database)    
        mycursor = mydb.cursor()
        
        while True:
            # Scrape data from the current page

            # Get username of both players
            name_data = page.locator("span.battle_data_name__IPyjF").all_text_contents()

            #MR Data. Gets MR data in one string, filters out the letters MR and sets LP related values to the previous MR value, or NULL if none is available
            battle_data = page.locator("li.battle_data_lp__6v5G9").all_text_contents()
            for i in range(len(battle_data)):
                if 'LP' in battle_data[i]:
                    battle_data[i] = battle_data[i - 2] if i >= 2 and 'MR' in battle_data[i - 2] else None

            #Get character data by using the image alt text
            images = page.locator("p.battle_data_character__Mnj8l img")
            character_data = [img.get_attribute("alt") for img in images.all()]

            # Get winner of player one, super spaghetti code here
            win_data_raw = page.locator("li.battle_data_player_1__LemvG").all_text_contents()
            win_data = []
            othervariable = 0
            for i in range(0, len(win_data_raw)):
                if win_data_raw[i] == "WINS":
                    win_data.append(name_data[othervariable])  # player1
                else:
                    win_data.append(name_data[othervariable + 1])  # player2
                othervariable += 2

            # Insert data into the database TODO: get date
            for i in range(0, len(battle_data), 2):
                mycursor.execute(
                    "INSERT INTO matches (player1_username, player2_username, player1_character, player2_character, player1_mr, player2_mr, winner, player_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (name_data[i], name_data[i + 1], character_data[i], character_data[i + 1], battle_data[i], battle_data[i + 1], win_data[i // 2], user_input)
                )
            mydb.commit()

            #Click to next page, or exit if last page.
            try:
                next_button = page.locator("li.next")
                if "disabled" in next_button.get_attribute("class"):
                    break
                next_button.click()
                page.wait_for_timeout(2000)  # Wait for the next page to load
            except Exception as e:
                print(f"Error navigating to the next page: {e}")
                break


        # Insert user data
        username = page.locator("span.status_name__gXNo9").all_text_contents()[0]
        mycursor.execute(
            "INSERT INTO users (player_id, username) VALUES (%s, %s)",
            (user_input, username)
        )
        mydb.commit()

        # TODO, find a better way of doing this
        player_id = f"{user_input}"
        usertable.update_user(player_id)

        browser.close()
