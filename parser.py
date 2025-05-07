from random import randint
import re
import requests
import codecs
from bs4 import BeautifulSoup as BS

__all__ = ("work", "dou", "djinni")

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]

def work(url):
    domain = "https://www.work.ua"
    resp = requests.get(url, headers=headers[randint(0,2)])
    jobs = []
    errors = []
    if resp.status_code == 200:
        soup = BS(resp.content, "html.parser")
        main_div = soup.find("div", attrs={"id": "pjax-job-list"})
        if main_div:
            div_lst = main_div.find_all("div", attrs={"class": "job-link"})
            for div in div_lst:
                title = div.find("h2")
                href = title.a["href"]
                content = div.p.text
                company = "no name"
                logo = div.find("img")
                if logo:
                    company = logo['alt']

                jobs.append({"title": title.text, "url": domain + href, 
                            "description": content, "company_name": company})
        else:
            errors.append({"url": url, "title": "MainDiv does not exist"})

    else: 
        errors.append({"url": url, "title": "Page do not response"})

    return jobs, errors


def dou(url):
    # domain = "https://www.work.ua"
    resp = requests.get(url, headers=headers[randint(0,2)])
    jobs = []
    errors = []
    
    if resp.status_code == 200:
        soup = BS(resp.content, "html.parser")
        main_div = soup.find("div", attrs={"id": "vacancyListId"})
        if main_div:
            li_lst = main_div.find_all("li", attrs={"class": "l-vacancy"})
            for li in li_lst:
                if "__hot" not in li["class"]:
                    title = li.find("div", attrs={"class": "title"})
           
                    href = title.a["href"]
                    content = li.find("div", attrs={"class": "sh-info"}).text
                    company = "no name"
                    a = title.find("a", attrs={"class": "company"})
                    if a:
                        company = a.text

                    jobs.append({"title": title.text, "url": href, 
                                "description": content, "company_name": company})
        else:
            errors.append({"url": url, "title": "MainDiv does not exist"})

    else: 
        errors.append({"url": url, "title": "Page do not response"})

    return jobs, errors

def djinni(url):
    domain = "https://djinni.co"
    resp = requests.get(url, headers=headers[randint(0,2)])
    jobs = []
    errors = []
    if resp.status_code == 200:
        soup = BS(resp.content, "html.parser")
        main_ul = soup.find("ul", attrs={"class": "list-jobs"})
        
        if main_ul:
            # li_lst = soup.select('[id*="jobs-item-"]')
            li_lst = main_ul.find_all("li", attrs={"id": re.compile(r'job-item-\S+')})#attrs={"class": "jobs-item-"}
            for li in li_lst:
                
                am = li.find("a", attrs={"class": "job-item__title-link"})
                title = am.text
                
                href = am.get("href")
                
                cont = li.find("span", attrs={"id": re.compile(r'job-description-\S+')})
                content = cont.find("span", attrs={"class": "js-truncated-text"}).text
                
                company = "no name"
                comp = li.find("a", attrs={"class": "text-body js-analytics-event"})
            
                if comp:
                    company = comp.text

                jobs.append({"title": title, "url": domain + href, 
                                "description": content, "company_name": company})
        else:
            errors.append({"url": url, "title": "MainDiv does not exist"})

    else: 
        errors.append({"url": url, "title": "Page do not response"})

    return jobs, errors


# --------------->> I didn't write robota.ua parser because it was rewrited on Angular

# def robota(url):
#     domain = "https://robota.ua/"
#     resp = requests.get(url, headers=headers)
#     jobs = []
#     errors = []

#     if resp.status_code == 200:
#         soup = BS(resp.content, "html.parser")
#         print(soup)
#         main_div = soup.find("div", attrs={"class": "santa-flex"})
#         print(main_div)
#         if main_div:
#             div_lst = main_div.find_all("div", attrs={"style": "min-height: 100px;"})
#             for div in div_lst:

#                 title = div.find("h2")
#                 print(title)
#                 link_tag = div.find('a')
#                 href = link_tag['href']
#                 content = "No description"
#                 company = div.find('span', class_="santa-mr-20 ng-tns-c122-24 ng-trigger ng-trigger-changeColor ng-star-inserted")

#                 jobs.append({"title": title.text, "url": domain + href, 
#                             "description": content, "company": company})
#         else:
#             errors.append({"url": url, "title": "MainDiv does not exist"})

#     else: 
#         errors.append({"url": url, "title": "Page do not response"})

#     return jobs, errors



if __name__ == "__main__":
    url = "https://djinni.co/jobs/?primary_keyword=Python&region=UKR&location=kyiv"
    jobs, errors = djinni(url)
    
    h = codecs.open("work.txt", "w", "utf-8")
    h.write(str(jobs))
    h.close