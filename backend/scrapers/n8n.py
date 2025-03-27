# import requests
# from bs4 import BeautifulSoup

# def scrape_n8n():
#     url = 'https://n8n.io/workflows'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     workflows = soup.find_all('div', {'class': 'workflow-card'})
#     n8n_workflows = []
#     for workflow in workflows:
#         # name = workflow.find('h2').text.strip()
#         description = workflow.find('h3', {'class': 'text-lg'}).text.strip()
#         category = workflow.find('span', {'class': 'category'}).text.strip() # TODO: figuring out category
#         # tags = [tag.text.strip() for tag in workflow.find_all('span', {'class': 'tag'})] # TODO: figuring out tags

#         n8n_workflows.append({
#             'name': "",
#             'description': description,
#             'category': category,
#             'tags': tags,
#             'platform': 'N8N'
#         })
#     return n8n_workflows

import asyncio
from playwright.async_api import async_playwright

async def scrape_n8n():
    n8n_workflows = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://n8n.io/workflows/")

        # Wait for the workflow cards to load
        await page.wait_for_selector("[data-v-8d0cdc00]")

        # Get all workflow cards
        workflow_cards = await page.query_selector_all("[data-v-8d0cdc00]")

        # Loop through each workflow card
        for card in workflow_cards:
            # Get the workflow name
            # Loop through each tag
            tags_array = []
            tags = []
            workflow_name = await card.query_selector("h3")
            if workflow_name == None: break
            workflow_name = await workflow_name.text_content()
            print(workflow_name)
            # Get all tags for the workflow
            try:
                await card.wait_for_selector("ul > *", timeout=1000)
                tags = await card.query_selector_all("ul > *")
            except Exception as e:
                print(f"Error: {e}")
                continue
            # tags = await card.query_selector_all("ul > *", timeout=1000)


            for tag in tags:
                # Hover over the tag to show the tooltip
                await tag.hover()

                # Wait for the tooltip to appear
                await page.wait_for_selector("div.v-popper__inner")

                # Get the tag description from the tooltip
                tag_description = await page.query_selector("div.v-popper__inner > div > div")
                tag_description = await tag_description.text_content()
                # print(await tag_description.text_content())
                # Print the workflow name and tag description
                if ',' in tag_description:
                    tags_tokenized = tag_description.split(',')
                    tags_array.extend(tags_tokenized)

                else:
                    tags_array.append(tag_description)

                await page.hover("footer.footer-main")
                await page.wait_for_function("document.querySelector('div.v-popper__inner') === null")

            print(f"Workflow: {workflow_name}, Tag: {tags_array}")

            n8n_workflows.append({
                'name': workflow_name,
                'description': workflow_name,
                'category': "",
                'tags': tags_array,
                'platform': 'N8N'
            })


    await browser.close()
    return n8n_workflows


if __name__ == '__main__':
    workflows = asyncio.run(scrape_n8n())
    # workflows = scrape_n8n()
    for workflow in workflows:
        print(workflow)