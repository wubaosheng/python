# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author : wubaosheng 2020-10-25
import requests
import random
from lxml import etree
import openpyxl
import xlsxwriter
import time
import os,sys,re
root = os.getcwd()

  
    # user_agent列表
# user_agent_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER', \
#     'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)', \
#     'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0', \
#     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36', \
#     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36']
user_agent_list =["Mozilla/5.0 (Windows NT 10.0; win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.1","Mozilla/5.0 (Windows NT 10.0; win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.1"]
    # referer列表
referer_list = ['https://www.genecards.org/cgi-bin/carddisp.pl?gene=STRC&keywords=GJB6', \
    'https://www.genecards.org/cgi-bin/carddisp.pl?gene=TPRN&keywords=TPRN',\
    'https://www.genecards.org/cgi-bin/carddisp.pl?gene=DAPK3&keywords=DAPK3',\
    'https://www.genecards.org/cgi-bin/carddisp.pl?gene=RFX4&keywords=RFX4']

headers = {"User-Agent": random.choice(user_agent_list),"Referer":random.choice(referer_list)}
base_url = 'https://www.genecards.org'
url = 'https://www.genecards.org/Search/Keyword?queryString=%20Cholinesterase'
def get_cookies(url):
    try:
        requests.session()
        sessions = requests.get(url, headers=headers)
        cookie = sessions.cookies
    except:
        cookie = ''
    return cookie

def get_search_response(url, cookies):
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        # print(response)
        content = response.content.decode()
        data = etree.HTML(content)
        print(data.text)
       # Entrez_gene = data.xpath("/html/body/div[1]/div[3]/div/div/main/div[2]/div/div/section[2]/div[1]/ul/li/p/text()")[0]
        uniport_summary = data.xpath("/html/body/div/div/div[@id='Gene']/div/main/div[@class='row'][2]/div/div/section[@id='summaries']/div[@class='gc-subsection']/ul/li/div/text()")[0]
        #Entrez_gene2 = data.xpath("")
        # uniport_summary2 = data.xpath("/html/body/div[1]/div[3]/div/div/main/div[2]/div/div/section[2]/div[2]/ul/li/div/text()")[0]

    except:
        # Entrez_gene = 'NA'
        uniport_summary = "NA"
        # Entrez_gene2 = "NA"
        # uniport_summary2 = "NA"
    # print(Entrez_gene2,"\n")
    print(uniport_summary,"\n")
   # print(trocris_summary,"\n")
    return uniport_summary

#### get the function
if __name__ == '__main__':
    table = open(root + "/%s.uniport.database" %(sys.argv[0]),"w")
    table.writelines(str("Entrez Gene" + "\t" + "UniProtKB/Swiss-Prot Summary" + "\t" + "Tocris Summary ") + "\n")
    counter =1
    with open(root + "/human_gene.txt","r") as fs:
        for line in fs:
            counter+=1
            if line.startswith("ENSG"):
                li = line.strip().split(",")[-1]
                time.sleep(10)
                new_url = 'https://www.genecards.org/cgi-bin/carddisp.pl?gene=' + li
                print(new_url)
                cookies = get_cookies(base_url)
                name = get_search_response(new_url, cookies)
                table.writelines(str(line.strip().split(",")[0]) + "\t"+ str(li) + "\t" + name + "\n")
                print(counter)
    fs.close()
    table.close()
