import asyncio
from playwright.async_api import async_playwright, Playwright, Browser, BrowserContext, Page,Response
from playwright_stealth import stealth_async
import json,os,re, pandas as pd
from requests_html import HTML
from multiprocessing.pool import ThreadPool

class Crazing:
    def __init__(self):
        self.url = 'https://www.carzing.com/find-dealership?zip=94108&miles=5000&page={page_no}&perPage=200'
        self.base_url = 'https://www.carzing.com'
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.total_matches = 0
        self.city = ''
    
    def scrape(self, response):
        html = HTML(html=response)
        dealers = []
        for dealer in html.find('.find-dealer-results-item'):
            dealer_info = dealer.find('.dealer-info',first=True)
            dealer_name = dealer_info.find('.dealer-result-name',first=True).text
            dealer_location = dealer_info.find('.dealer-result-location',first=True).text
            dealer_phone = dealer_info.find('.dealer-result-phone',first=True).text
            dealer_distance = dealer_info.find('.dealer-result-distance',first=True).text
            inventory = dealer.find('.dealer-result-inventory a',first=True)
            dealer_inventory = re.findall(r'\d+',inventory.text)[0]
            dealer_inventory_url = f"{self.base_url}{inventory.attrs['href']}"
            dealer_zip = inventory.attrs['data-zip']
            dealers.append({
                "DEALER NAME":dealer_name,
                "LOCATION":dealer_location,
                "PHONE":dealer_phone,
                "DISTANCE":dealer_distance,
                "INVENTORY":dealer_inventory,
                "ZIP":dealer_zip,
                "CITY":self.city,
                "INVENTORY URL":dealer_inventory_url,
            })
                                    
        return dealers
    
    async def setup(self, page_number: int, initial: bool = False):
        playwright = await async_playwright().start()
        browser = await playwright.firefox.launch(headless=True)
        if os.path.exists(f"{self.current_path}/CREDENTIALS/storage_state.json"):
            with open(f"{self.current_path}/CREDENTIALS/storage_state.json") as file:
                storage_state = json.load(file)
            context = await browser.new_context(storage_state=storage_state)
        else:
            context = await browser.new_context()
        page = await context.new_page()
        await stealth_async(page)
        response = await page.goto(self.url.format(page_no=page_number))
        
        if initial:
            os.makedirs(f"{self.current_path}/CREDENTIALS", exist_ok=True)
            context_storage = await context.storage_state(path=f"{self.current_path}/CREDENTIALS/storage_state.json")
            self.total_matches = await page.locator('[id="vlp-finddealer-title"] p strong').inner_text()
            finddealer = await page.locator('[id="vlp-finddealer-title"] h1').inner_text()
            self.city = finddealer.split('Dealerships near ')[1]
        else:
            response = await response.text()
        
        try:
            await context.close()  # Close the context
            await browser.close()  # Close the browser
            await playwright.stop()  # Stop the playwright
        except:
            pass
        return response
        
    def main(self,page_number:int):
        response = asyncio.run(self.setup(page_number))
        return self.scrape(response)
    
    def run(self):
        df = pd.DataFrame()
        asyncio.run(self.setup(1,initial=True))
        total_pages = int(int(self.total_matches)/200)
        if total_pages > 0:
            with ThreadPool(4) as pool:
                results = pool.map(self.main,range(1,total_pages+1))
                for result in results:
                    df = pd.concat([df,pd.DataFrame(result)])
                df.to_csv(f"{self.current_path}/dealers.csv",index=False)
                print(f"Total Dealers: {self.total_matches}")
                print(f"Total Dealers Scraped: {len(df)}")
        else:
            print("No Dealers found")

if __name__ == '__main__':
    crazing = Crazing()
    crazing.run()