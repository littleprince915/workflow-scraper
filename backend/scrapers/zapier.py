# import requests
# import mechanize
# from bs4 import BeautifulSoup
# import urllib2 
# import cookielib ## http.cookiejar in python3


def scrape_zapier():
    # url = 'https://zapier.com/app/templates/use-cases'

    # cj = cookielib.CookieJar()
    # br = mechanize.Browser()
    # br.set_cookiejar(cj)
    # br.open(url)

    # br.select_form(nr=0)
    # br.form['username'] = 'username'
    # br.form['password'] = 'password.'
    # br.submit()

    # response = br.response().read()

    # soup = BeautifulSoup(response.content, 'html.parser')
    zapier_workflows = []
    # categories = soup.find_all('section', {'class': 'ContentSection_root__fqyO8'})

    # for categoryHTML in categories:
    #     category = template.find('h2', {'class': 'ContentSection_title__2jY5d'}).text.strip()
    #     templates = categoryHTML.find_all('div', {'class': 'template-card'})

    #     for template in templates:
    #         name = ""
    #         description = template.find('span', {'class': 'ZapCard_title__FuQrI'}).text.strip()
    #         category = template.find('span', {'class': 'category'}).text.strip()
    #         tags = template.find_all('div', {'class': '_service-icons_667aj_1'})[0]['aria-label'].split(',')
    #         zapier_workflows.append({
    #             'name': name,
    #             'description': description,
    #             'category': category,
    #             'tags': tags,
    #             'platform': 'Zapier'
    #         })
    return zapier_workflows

if __name__ == '__main__':
    workflows = scrape_zapier()
    print(workflows)