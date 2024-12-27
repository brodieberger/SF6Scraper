def scrapesite(user_input):
    from playwright.sync_api import sync_playwright
    import mysql.connector
    import userpasswords #This file contains the username and password for the CAPCOM account. (Buckler's Bootcamp)

    with sync_playwright() as p:
        user_URL = f"https://www.streetfighter.com/6/buckler/auth/loginep?redirect_url=/profile/{user_input}/battlelog/rank"

        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page()

        page.goto(user_URL)
    
        # Enter country, date of birth, and click submit
        dropdown = page.locator("select[id='country']")            
        dropdown.select_option("United States")
        page.locator("select[id='birthYear']").select_option('2000') 
        page.locator("select[id='birthMonth']").select_option('12')
        page.locator("select[id='birthDay']").select_option('25')
        page.locator("button[name='submit']").click()    
    
        # Enter username and password click submit
        email_field = page.locator("input[type='email']")
        
        #ENTER EMAIL HERE
        email_field.fill(userpasswords.emailfill)
        pw_field = page.locator("input[type='password']")

        #ENTER PASSWORD HERE
        pw_field.fill(userpasswords.passwordfill)
        page.locator("button[name='submit']").click()
    
        # Wait for the page to load and navigate to the profile
        page.wait_for_timeout(8000)
    
        # Get MR data and convert it all to integers
        battle_data = page.locator("li.battle_data_lp__6v5G9").all_text_contents()
        battle_data = [int(data.replace(' MR', '')) for data in battle_data]

        # Get Names of each player
        name_data = page.locator("span.battle_data_name__IPyjF").all_text_contents()

        # Print or return the scraped data
        data_amount = len(battle_data)
    
        username = page.locator("span.status_name__gXNo9").all_text_contents()[0]
        browser.close()

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sf6scraper"
        )
        mycursor = mydb.cursor()
        
        for i in range(0, data_amount, 2):
            #current_data=(str(name_data[i]) + " (" + str(battle_data[i]) + "MR) VS " + str(name_data[i+1]) + "(" + str(battle_data[i+1]) + "MR)")
            mycursor.execute(
                "INSERT INTO matches (player1_username, player2_username, player1_mr, player2_mr, winner, player_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (name_data[i], name_data[i+1], battle_data[i], battle_data[i+1],'Temp Player', user_input)  # TODO, get winner logic
            )
            mydb.commit()