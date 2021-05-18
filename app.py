import imaplib, email, ctypes, pathlib, os, sys, time, json, random
from email.header import decode_header
from termcolor import cprint, colored
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
os.system("cls")

ctypes.windll.kernel32.SetConsoleTitleW("Codex Nike Account Resetter by liamm#0001")
cprint("Please Select the Action:",'cyan')
cprint("\n[1]: Reset Accounts\n[2]: Exit",'green')
action = input("Enter: ")

if action == "1":
    cprint('Loading Credentials', 'cyan')
    # loading account credentials
    with open('settings.json','r') as read_file:
      data = json.load(read_file)
      username = data['username']
      password = data['password']

    def clean(text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)

    cprint('Logging In', 'cyan')
    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)

    status, messages = imap.select("INBOX", readonly=False)

    # number of top emails to fetch
    with open('settings.json','r') as read_file:
        threadct = json.load(read_file)
        N = int(threadct['threadcount'])
    # total number of emails
    messages = int(messages[0])
    typ, msgnums = imap.search(None, '(UNSEEN)')
    msgnums = msgnums[0].split(b" ")
    cprint('\nResetting Accounts:','red')


    for i in range(messages, messages-N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                print("Subject:", subject)
                print("From:", From)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass

                if content_type == "text/html":
                    # if it's HTML, create a new HTML file and open it in browser
                    folder_name = clean(subject)
                    if not os.path.isdir(folder_name):
                        # make a folder for this email (named after the subject)
                        os.mkdir(folder_name)
                    filename = "index.html"
                    filepath = os.path.join(folder_name, filename)
                    open(filepath, "w").write(body)

                    # write the filepath of the folder we just created
                    newfilepath = str(pathlib.Path('app.py').parent.absolute())
                    index = ("" + newfilepath + "\\" + filepath)

                    # open browser of email
                    driver = webdriver.Chrome('chromedriver.exe')
                    driver.get(index)

                    # click on reset link
                    link = driver.find_element_by_partial_link_text("here").click()
                    

                    # gets password from json
                    with open('settings.json','r') as read_file:
                        newpassw = json.load(read_file)
                        npass = newpassw['newpassword']
                    
                    # waits for page to load before continuing
                    timeout = 5
                    try:
                        element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/form/div[1]/input'))
                        WebDriverWait(driver, timeout).until(element_present)
                    except TimeoutException:
                        print ("Timed out waiting for page to load")

                    # finds and inputs new password
                    field = driver.find_element_by_xpath('/html/body/div[2]/form/div[1]/input')
                    field.click()
                    enter = driver.find_element_by_xpath('/html/body/div[2]/form/div[2]/input')
                    time.sleep(2)
                    for element in npass:
                        inputdelay = random.randint(0,2)
                        field.send_keys(element)
                        time.sleep(inputdelay)
                        
                    action = webdriver.common.action_chains.ActionChains(driver)
                    action.move_to_element_with_offset(enter, 5, 5)
                    action.click()
                    action.perform()
                    #driver.close()
                
              
                
if action == "2":
    cprint("Quitting",'red')
    quit()


# close the connection and logout
imap.close()
imap.logout()