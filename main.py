from flask import Flask, render_template, request
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def run(user_input):
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
        email_field.fill(" ")
        pw_field = page.locator("input[type='password']")

        #ENTER PASSWORD HERE
        pw_field.fill(" ")
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

        MRList = []
        MRTotal = 0
        history_list = []
        
        for i in range(0, data_amount, 2):
            if name_data[i] == username:
                #If the left name (i) matches user
                current_data=(str(name_data[i]) + " (" + str(battle_data[i]) + "MR) VS " + str(name_data[i+1]) + "(" + str(battle_data[i+1]) + "MR)")
                MRList.append(battle_data[i])
            else:
                #If the right name (i+1) matches user
                current_data=(str(name_data[i+1]) + " (" + str(battle_data[i+1]) + "MR) VS " + str(name_data[i]) + "(" + str(battle_data[i]) + "MR)")
                MRList.append(battle_data[i+1])
            history_list.append(current_data)
        
        for item in MRList:
            MRTotal += item
       
        averagetoReturn = str(MRTotal / (data_amount / 2))

        browser.close()
    return username, averagetoReturn, history_list

#start web app
@app.route("/", methods=["GET", "POST"])
def index():
    player_results = None
    if request.method == "POST":
        user_code = request.form["user_code"]
        player_results = run(user_code)
    return render_template("index.html", player_results=player_results)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
