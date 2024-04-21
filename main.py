#!/usr/bin/python3
from colorama import Fore,Back,Style
import yaml
import time as t
import random 
from googleapiclient.discovery import build
import os
import re
import csv
from collections import defaultdict


leadCounter = 0
red =  Fore.RED
green = Fore.GREEN
magenta = Fore.MAGENTA
cyan = Fore.CYAN
mixed = Fore.RED + Fore.BLUE
blue = Fore.BLUE
yellow = Fore.YELLOW
white = Fore.WHITE
reset = Style.RESET_ALL
colors = [red, green, yellow, cyan, blue, magenta]
random_color = random.choice(colors)
res = 0
banner ="""
  _      _       _            _ _       _____             _             
 | |    (_)     | |          | (_)     |  __ \           | |            
 | |     _ _ __ | | _____  __| |_ _ __ | |  | | ___  _ __| | _____ _ __ 
 | |    | | '_ \| |/ / _ \/ _` | | '_ \| |  | |/ _ \| '__| |/ / _ \ '__|
 | |____| | | | |   <  __/ (_| | | | | | |__| | (_) | |  |   <  __/ |   
 |______|_|_| |_|_|\_\___|\__,_|_|_| |_|_____/ \___/|_|  |_|\_\___|_|   
                                                                        
                                                                        
"""


#config file
def config_file():

    filename = "google_dorker.yaml"
    path = "/development/dorker/GoogleDorker/"
    for root,dirs,files in os.walk(path):
        
        if filename in files:
            file_path = os.path.join(root, filename)            
            return file_path
    exit()



def query(filename, theme, api_key, cse):

        
    results_per_page = 10
    total_results = 100
    
    research_index = 1
    
    while research_index < total_results:

        service = build('customsearch', 'v1', developerKey=api_key)

        if research_index > total_results:
            break      
        
        try:
            results = service.cse().list(
            q=  theme +  "( \"@gmail.com\" OR \"yahoo.com\" OR \"outlook.com\" OR \"hotmail.com\") -intitle:\"profiles\" -inurl:\"dir/ \" site:fr.linkedin.com/in/",
            cx=cse,
            num=results_per_page,
            start=research_index
            ).execute()

        except Exception as e:
            if("Quota exceeded" in str(e)):
                add_after_string("/development/dorker/GoogleDorker/google_dorker.yaml", chosen_key, " used")
                print("api key already used, changing...")
                api_key, cse = load_keys(filename)
                if(api_key == -1):
                    return -1
                continue 
            else:
                print(f"Error occured due to {e}")
                return -1
        
        for i, item in enumerate(results.get('items', []), start=research_index):
            
            title = item['title']
            titles = title.split(' - ')
            names = titles[0].split(' ')
            firstname = names[0]
            try: 
                if(len(names) > 2):
                    lastname = names[1] + " " + names[2]
                else:
                    lastname = names[1]
            except:
                lastname = ""
                
            try: 
                if not '@' in titles[1]:
                    job = titles[1]
                else:
                    job = ""
            except:
                job = ""
            snippet = item['snippet']
            email = extract_email_from_snippet(snippet)
            try:
                if(len(email) > 0):
                    appendLead(firstname, lastname, email[0], job)
            except Exception as e:
                print(e)
        
        research_index += results_per_page




def choose_random_api_key(api_keys):
    # Filtrer les clés API qui ne contiennent pas "used"
    valid_keys = [key for key in api_keys if "used" not in key]
    # Choisir une clé API au hasard parmi celles valides
    chosen_key = random.choice(valid_keys)
    return chosen_key


def add_after_string(file, target_string, added_string):
    with open(file, 'r') as f:
        content = f.read()

    # Remplace toutes les occurrences de target_string par target_string + added_string
    modified_content = content.replace(target_string, target_string + added_string)

    with open(file, 'w') as f:
        f.write(modified_content)


def appendLead(firstname, lastname, email, job):

    filename = 'leads.csv'

    def check_empty_file(filename):
        with open(filename, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            # Check if the file is empty
            try:
                headers = next(csv_reader)
                return False
            except StopIteration:
                return True
            
    def fill_csv_file(filename, headers):
        with open(filename, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            # Write column headers
            csv_writer.writerow(headers)


    fieldnames = ['First Name', 'Last Name', 'Email', 'Accepts Email Marketing', 'Default Address Company',
                'Default Address Address1', 'Default Address Address2', 'Default Address City', 'Default Address Province Code',
                'Default Address Country Code', 'Default Address Zip', 'Default Address Phone', 'Phone',
                'Accepts SMS Marketing', 'Tags', 'Note', 'Tax Exempt']
    
    # Check if the file is empty
    if check_empty_file(filename):
        fill_csv_file(filename, fieldnames)
        
    
    with open(filename, 'a', newline='') as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow({
            'First Name': firstname,
            'Last Name': lastname,
            'Email': email,
            'Accepts Email Marketing': 'no',
            'Default Address Company': '',
            'Default Address Address1': '',
            'Default Address Address2': '',
            'Default Address City': '',
            'Default Address Province Code': '',
            'Default Address Country Code': '',
            'Default Address Zip': '',
            'Default Address Phone': '',
            'Phone': '',
            'Accepts SMS Marketing': 'no',
            'Tags': '',
            'Note': job,
            'Tax Exempt': ''
        })


def extract_email_from_snippet(snippet):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email = re.findall(pattern, snippet)
    return email   
        
def extract():
    def extract_emails_from_file(filename):
        with open(filename, 'r') as file:
            text = file.read()
            pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(pattern, text)
        return emails

    def save_emails_to_file(emails, filename):
        with open(filename, 'w') as file:
            for email in emails:
                file.write(email + '\n')

    if __name__ == "__main__":
        input_filename = 'google_dorks.txt'  # Modifier le nom du fichier d'entrée selon votre besoin
        output_filename = 'emails.txt'

        emails = extract_emails_from_file(input_filename)
        save_emails_to_file(emails, output_filename)
        print("Les adresses email ont été extraites du fichier '{}' et sauvegardées dans le fichier '{}'.".format(input_filename, output_filename))

def remove_duplicates():

    filename = "leads.csv"

    # Read all lines into memory
    with open(filename, 'r', newline='') as file:
        lines = list(csv.reader(file))

    # Identify unique lines
    unique_lines = []
    seen = set()
    for line in lines:
        line_str = ','.join(line)
        if line_str not in seen:
            unique_lines.append(line)
            seen.add(line_str)

    # Write unique lines back to the CSV file
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(unique_lines)

    global leadCounter
    leadCounter = len(unique_lines)



def load_keys(filename):
        with open (filename, "r") as keys:
            
            data = yaml.safe_load(keys)
        
        # google_api = random.choice(data.get("Google-API", []))
        google_api_keys = data['Google-API']
        global chosen_key

        try:
            chosen_key = choose_random_api_key(google_api_keys)
        except Exception as e:
            if("list index out of range" in str(e)):
                print("no more valid api key")  
            return -1,-1

        google_csi = random.choice(data.get("Google-CSE-ID", []))
                
        if chosen_key is None or google_csi is None:
            
                # print(f"[{red}ALERT{reset}]: There is no api keys found for Google-API or Google-CSI-ID. Without these keys and ID dorking cannot perform")
                        
                exit()
            
        else:
                pass 
        
        return chosen_key, google_csi

def remove_themes_duplicates(filename):
    # Ouvre le fichier d'entrée en mode lecture
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Supprime les doublons tout en préservant l'ordre d'origine
    unique_lines = list(dict.fromkeys(lines))

    # Ouvre le fichier de sortie en mode écriture
    with open(filename, 'w') as f:
        # Écrit les lignes uniques dans le fichier de sortie
        f.writelines(unique_lines)




def main():
    
    print(f"{random_color}{banner}{reset}")
    
    filename = config_file()

    remove_themes_duplicates("themes.txt")
        
    #load api keys
    api_key, cse = load_keys(filename)
    if(api_key == -1):
        return
    
    with open("/development/dorker/GoogleDorker/themes.txt", "r") as file:
        for line in file:

            #get the current theme keyword
            theme = line.strip()  # Supprimer les espaces et les sauts de ligne
            print("scrapping with keyword: " + theme)

            #start query process
            if(query(filename, theme, api_key, cse) == -1):
                break

    remove_duplicates()

    print("number of scraped leads: " + str(leadCounter))

            

if __name__ == "__main__":
    
    main()