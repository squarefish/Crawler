#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 16:12:34 2020

@author: fyh
"""
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import time

'''
2020 Jun. 21:
This crawler requires some manual operations:
Searching keywords = '前端工程師'
Feed the searching keywords to the 104 search tab 
Check the search results and look up the total page numbers
Change the page number in the script where applicable
'''

pre_url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=%E5%89%8D%E7%AB%AF%E5%B7%A5%E7%A8%8B%E5%B8%AB&order=15&asc=0&page='
post_url = '&mode=s&jobsource=2018indexpoc'

def getHtmlContent(input_url):
    try:
        with urlopen(input_url) as x:
            output = x.read().decode('utf-8') 
            # utf-8 encoding ensures proper display of Chinese
    except ValueError:
        pass
    return output

jobs = pd.DataFrame()

for i in range(1,121): # manually change the page number here
    url = pre_url+str(i)+post_url
    content = getHtmlContent(url)
    print('Crawling page'+ str(i))
    
    if type(content) == str:
        soup = BeautifulSoup(content, 'html.parser')
        tags = soup.find_all(["article"]) # find all the positions shown on this page
        
        for t in tags:
            if len(t) == 5 and '接案' not in t.text:
                a_tags = t.find_all("a")
                position_link = a_tags[0].get("href")
                job_id = position_link.replace('//www.104.com.tw/job/', '')
                job_id = job_id.replace('?jobsource=hotjob_chr', '')
                num_application = t.find_all('a', class_= 'b-link--gray gtm-list-apply')[0].string
                js_link = 'https://www.104.com.tw/job/ajax/content/'+job_id
                header = 'https://www.104.com.tw/job/'+job_id                
                headers = {"Referer": header}
                response = requests.get(url = js_link, headers = headers)
                job_content = json.loads(response.text)
                
                try:
                    job_name = job_content['data']['header']['jobName']
                except IndexError:
                    job_name = ''
                
                try:
                    company_name = job_content['data']['header']['custName']
                except IndexError:
                    company_name = ''
                
                try:
                    acceptRole = job_content['data']['condition']['acceptRole']['role'][0]['description']
                except IndexError:
                    acceptRole = ''
                    
                try:
                    workExp = job_content['data']['condition']['workExp'] 
                except IndexError:
                    workExp = ''
                    
                try:
                    edu = job_content['data']['condition']['edu']
                except IndexError:
                    edu = ''
                
                try:
                    major = job_content['data']['condition']['major']
                except IndexError:
                    major = ''

                try:
                    skill = job_content['data']['condition']['skill']
                except IndexError:
                    skill = ''
                
                try:
                    other = job_content['data']['condition']['other']
                except IndexError:
                    other = ''
                    
                try:
                    industry = job_content['data']['industry']
                except IndexError:
                    industry = ''
                    
                try:
                    salary = job_content['data']['jobDetail']['salary']
                except IndexError:
                    salary = ''
                
                try:
                    region = job_content['data']['jobDetail']['addressRegion']
                except IndexError:
                    region = ''
            
                df = pd.DataFrame({'職缺': [job_name], 
                                   '公司': [company_name],
                                   '應徵人數': [num_application], 
                                   '職缺連結': [position_link],
                                   '地點': [region],
                                   '產業類型': [industry],
                                   '薪資': [salary],
                                   '經歷': [workExp],
                                   '科系': [major],  
                                   '學歷': [edu],
                                   '要求技能': [skill],
                                   '接受身份': [acceptRole], 
                                   '其他': [other]})
                jobs = jobs.append(df, ignore_index = True)
                time.sleep(0.5) # pauses for 0.5s to lessen the server burden  

jobs.to_excel('~/104Search_Result.xls')