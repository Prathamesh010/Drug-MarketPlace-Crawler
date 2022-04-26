# script to get links from hiddenWiki.org and save in a csv file with its title and link

import subprocess
from urllib import request

drugs_word_list = ["cocaine", "heroin", "meth", "marijuana", "ecstasy", "lsd", "cannabis", "mushrooms", "opium", "weed","drug","cannabis", "crack", "speed"]

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return output

def request_html(url):
    # get html content using requests
    requestObj = request.Request(url)
    requestObj.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1')
    response = request.urlopen(requestObj)
    html = response.read()
    return html

def get_info_on_links():
    print("Geting info on links...")
    # use onioff to get info on the links
    command = "python3 onioff.py -f links.txt -o links_data.txt"
    run_command(command)
    
    print("Filtering drugs marketplace links..")
    # read links_data.txt and remove links that are not active
    with open("links_data.txt", "r") as f:
        lines = f.readlines()
        lines_to_write = []
        for line in lines: 
            # make all the words in the line lowercase
            line = line.lower()
            if "UNAVAILABLE" not in line and any(ele in line for ele in drugs_word_list):
                # print("appending... " + line)
                lines_to_write.append(line)
        # print list items on new lines to make it easier to read using print
        for line in lines_to_write:
            print(line)
        
        print("writing to links_Data.txt..")
        with open("links_data.txt", "w") as f:
            f.writelines(lines_to_write)
        print("Done")

def prepare_links_to_crawl():
    print("Preparing links to crawl...")
    print("Getting links from theHiddenWiki...")
    # parse links from hiddenWiki.org
    html = request_html("https://thehiddenwiki.org/")
    
    # get all links from the html content
    links = []
    for link in html.decode().split('\n'):
        # if link does not contain onion ignore it
        if "onion" not in link:
            continue
        if '<a href="' in link:
            links.append(link.split('"')[1])

    print("Curating Links from SearchEngines...")
    # onion Search
    run_command("onionsearch --limit 1 drugs --output links_onion_search.txt")

    # append to links from links_onion_search.txt
    with open("links_onion_search.txt", "r") as f:
        onion_links = f.readlines()
        for link in onion_links:
            # split link by comma and get the thrid part
            link = link.split("\",\"")[2]
            # remove the quotes
            link = link.replace('"', '')

            # only get links and not the route after the domain along with http or https
            if "http" in link:
                link = link.split('/')[2]
            if "http://"+link.strip() not in links:
                links.append("http://"+link.strip())

    print("Writing links to links.txt...")
    # save links in a csv file with its title and link
    with open("links.txt", "w") as f:
        for link in links:
            f.write(link + "\n")

    get_info_on_links()

def main():
    prepare_links_to_crawl()

if __name__ == '__main__':
    main()