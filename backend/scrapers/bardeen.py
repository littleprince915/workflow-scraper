import requests
from bs4 import BeautifulSoup

def scrape_bardeen():
    url = 'https://bardeen.ai/playbooks'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    playbooks = soup.find_all('div', {'class': 'playbook_item'})
    workflows = []
    for playbook in playbooks:
        name = playbook.find('div', {'class': 'playbook_item-verb'}).text.strip()
        description = playbook.find('div', {'class': 'playbook_item-text'}).text.strip()
        category = playbook.find('div', {'class': 'playbook_category-used'})

        if category:
            category = category.text.strip()

        tags = [tag.text.strip() for tag in playbook.find_all('span', {'class': 'tag'})]
        workflows.append({
            'name': name,
            'description': description,
            'category': category,
            'tags': tags,
            'platform': 'Bardeen'
        })
    return workflows

if __name__ == '__main__':
    workflows = scrape_bardeen()
    for workflow in workflows:
        print(workflow)