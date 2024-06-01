import requests
import whois
import threading
import random
import socket
import argparse
import dns.resolver
from bs4 import BeautifulSoup
import builtwith
from playwright.sync_api import sync_playwright
import re
import sqlite3
from flask import Flask,redirect,url_for,request,render_template



#open file
savefile1 = open("save1.txt", "a", encoding="utf-8")
savefile2 = open("save2.txt", "a", encoding="utf-8")

#open file

#args
parser = argparse.ArgumentParser(description='Find all URLs to 2 layers.')
parser.add_argument('url1', type=str, help='Please enter the first URL to run.')
parser.add_argument('url2', type=str, help='Please enter the second URL to run.')
args = parser.parse_args()
#args

chekfu = 0


def All_code (furl,savefile):

    
    #get 
    response  = requests.get(furl)
    soup = BeautifulSoup(response.content)
    #get 

    #port
    ports = [21,22,23,25,53,80,110,119,123,143,161,194,443,445,993,995]
    textfile = open("wordlist.txt","r")
    mysubs = textfile.readlines()

    #port

    #whois
    domain = furl.replace('http://', '').replace('https://', '')
    dm_info =  whois.whois(str(domain))
    #whois

    #SQLite

    db = sqlite3.connect("data1.db")

    cur = db.cursor()
    
    domainf = domain.replace('.', '')
    
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS {str(domainf)}(
        id INTEGER PRIMARY KEY,
        urlweb VARCHAR,
        whois VARCHAR,
        title VARCHAR,
        wappalyzer VARCHAR,
        email VARCHAR,
        mobilnumber VARCHAR,
        subdomain_ip VARCHAR,
        port VARCHAR,
        orginalurls VARCHAR,
        statuscode VARCHAR,
        suburl VARCHAR
        )"""
    )

    #SQLite

    #regex
    txt = str(soup)
    #regex

    #/////////////////////defs



    def download_img (url):
        
        

        try:

            response  = requests.get(url)
            soup = BeautifulSoup(response.content)


            for img in soup.find_all('img', src=True):

                test = int(random.uniform(1, 100000000000000000000000000))

                try:
                
                    var = requests.get(img["src"])

                    with open("C:\\Users\Asus\Pictures\\"+str(test)+".png", 'wb') as f:
                        f.write(var.content)

                except:
                    pass

                
            for img in soup.find_all('img', srcset=True):

                test = int(random.uniform(1, 100000000000))
            

                try:
                    
                    find825 = r'\b828\b'

                    pattern = r'https?://[^/]+'
                    match = re.search(pattern, url)

                    var = requests.get(str(match.group()) + img["srcset"])

                    

                    with open("C:\\Users\Asus\Pictures\\"+str(test)+".png", 'wb') as f:
                        f.write(var.content)

                    
                except:
                    
                    pass
        except:
            pass
            
    def find_title (url):

        try:

            response  = requests.get(url)
            soup = BeautifulSoup(response.content)
        
            title = soup.title.string
            print (title)
            savefile.write("\n" + title)

            cur.execute(
                f"""INSERT INTO {domainf}(title) VALUES(?)""", (title,)
            )
            
            db.commit()
            
        except:
            print("can't find title")

    def find_whois (url):

        try:
        
            domain = url.replace('http://', '').replace('https://', '')
            dm_info =  whois.whois(domain)
            
            whoisf = str(dm_info)
            
            print (whoisf)
            savefile.write("\n" + whoisf)
            
            
            cur.execute(
                f"""INSERT INTO {domainf}(whois) VALUES(?)""",(whoisf,)
            )
            
            db.commit()


        except:
            print("can't find whois.........................................................................................................")
    
    def find_Email_mobilenumber (txt):

        try:
            email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', txt)
            mobile_numbers = re.findall(r'\b09\d{9}\b', txt)

            print(email)
            print(mobile_numbers)
            savefile.write("\n" + str(email) + "\n" + str(mobile_numbers))

            emailf= str(email)
            mobile_numbersf= str(mobile_numbers)

            cur.execute(
                f"""INSERT INTO {domainf}(email,mobilnumber) VALUES(?,?)""", (emailf,mobile_numbersf,)
            )
            
            db.commit()

        except:
            pass

    def find_subdomai_ip_port (url):

        global chekfu
        domain = url.replace('http://', '').replace('https://', '')
        furl_tesst = furl.replace('http://', '').replace('https://', '')
        pattern = r'(\.ir|\.com|\.org)(/.*)?'

        furl_tesst = re.sub(pattern, r'\1', furl_tesst)
        domain = re.sub(pattern, r'\1', domain)

        print(furl_tesst)
        print(domain)
        print(chekfu)

        if furl_tesst != domain or chekfu ==0:

            for subdomain in mysubs:


                print("\n" , "-----------------------------------------------------" , "\n")

                subdomain = subdomain.replace("\n","")

                try:

                    answers = dns.resolver.query(subdomain + "." + domain, "A")

                    for ip in answers:
                    
                        print(subdomain + "." + domain + "-" + str(ip)+ "\n")
                        savefile.write("\n" + str(subdomain) + "." + str(domain) + "-" + str(ip) )

                        cur.execute(
                            f"""INSERT INTO {domainf}(subdomain_ip) VALUES(?)""",((str(subdomain) + "." + str(domain) + "-" + str(ip)),)
                        )
                
                        db.commit()

                        for port in ports:

                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                            result = sock.connect_ex((str(ip),port))

                            if result == 0:

                                print( "Port ", port ,": open")
                                savefile.write("\n" + "Port "+ str(port) +": open") 

                                cur.execute(
                                    f"""INSERT INTO {domainf}(port) VALUES(?)""",((str(ip) + "Port "+ str(port) +": open"),)
                                )
                
                                db.commit()


                except:
                    print("no subdoman :" + str(subdomain))
                    savefile.write("\n" + "no subdoman :" + str(subdomain))

        chekfu+=1

    def sublink (url):

        try:
            
            print("\n")
            print("sublink = **************************************************************************** ")
            savefile.write("\n" + "sublink = **************************************************************************** ")

            response2  = requests.get(url)

            soup2 = BeautifulSoup(response2.content)

            for a in soup2.find_all('a', href=True):

                print ("-------------------------:", a['href'] )
                savefile.write("\n" + "-------------------------:"+ str(a['href']) )
                
                cur.execute(
                   f"""INSERT INTO {domainf}(suburl) VALUES(?)""",(str(a['href']),)
                )
                db.commit()

        except: 

            print("no url")
            savefile.write("no url")

    def wappalyzer (url):

        print("\n")

        def get_website_technologies(url):

            try:
            
                technologies = builtwith.parse(url)
                return technologies
        
            except:
                pass
        


        website_url = url


        technologies = get_website_technologies(website_url)

        if technologies:
            print("Technologies used on", website_url, ":")

            for category, techs in technologies.items():
                print(f"- {category}:")
                savefile.write("\n" + f"- {category}:")

                for tech in techs:
                    print(f"  - {tech}")
                    savefile.write(f"  - {tech}")

                    cur.execute(
                        f"""INSERT INTO {domainf}(wappalyzer) VALUES(?)""",(str((f"- {category}:" + f"  - {tech}" )),)
                    )
            
                    db.commit()
        else:
            print("Failed to retrieve technologies.")

    def screenshot (url):

        tester = int(random.uniform(1, 1000000000000000000000))

        try:
            
            
            with sync_playwright() as playwright:

                browser = playwright.chromium.launch(executable_path=r"C:\Users\Asus\AppData\Local\Chromium\Application\chrome.exe")
                page = browser.new_page()
                page.goto(url)
                page.screenshot(path='C:/Users/Asus/Pictures/screenshot'+ str(tester)+ ".png", full_page=True)
                browser.close()

        except:
            pass

    #/////////////////////defs

    savefile.write(furl)
    cur.execute(
        f"""INSERT INTO {domainf}(urlweb) VALUES(?)""", (str(furl),)
    )

    find_whois(furl)

    find_title(furl)

    wappalyzer(furl)

    download_img(furl)

    screenshot(furl)

    find_Email_mobilenumber(txt)

    find_subdomai_ip_port(furl)
                



    for a in soup.find_all('a', href=True):

        try:
            response3  = requests.get(a['href'])

            

            print("\n\n")
            print (" URL: ^^^^^^^^^^^^^^^^^^^", a['href'] , "------------",response3.status_code)
            print("\n\n")
            savefile.write("\n" + " URL: ^^^^^^^^^^^^^^^^^^^"+ str(a['href']) + "------------"+str(response3.status_code))

            savefile.write(furl)

            cur.execute(
                f"""INSERT INTO {domainf}(orginalurls,statuscode) VALUES(?,?)""", (str(a['href']),str(response3.status_code),)
            )

            txt = str(soup)

            find_whois (a['href'])

            find_title (a['href'])

            wappalyzer (a['href'])

            download_img(a['href'])

            screenshot(a['href'])
            
            find_Email_mobilenumber(txt)

            find_subdomai_ip_port (a['href'])

            sublink (a['href'])

        except: 
            print(f"The address {a['href']} is invalid")
    
    db.close()
#//////////////////////////////////////////////////
   
db = sqlite3.connect("data1.db")

cur = db.cursor()

app = Flask(__name__)

@app.route("/" , methods =['POST','GET'])
def Login():
    
    # username = request.args.get('username')
    # email = request.args.get('email')

    # username = request.form['username']
    # email = request.form['email']

    name = cur.execute(f"SELECT * FROM {args.url1}")

    return render_template("index.html", user = name)

#//////////////////////////////////////////////////


url1 = threading.Thread(target=All_code, args=(args.url1,savefile1,))
url2 = threading.Thread(target=All_code, args=(args.url2,savefile2,))

url1.start()
url2.start()

url1.join()
url2.join()

savefile1.close()
savefile2.close()


