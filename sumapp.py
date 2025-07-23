import os
import time
import requests
from bs4 import BeautifulSoup
from seleniumbase import SB
import argparse
from openai import OpenAI
from dotenv import load_dotenv


class Website():
    def __init__(self, url):
        self.url = url
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        self.title = soup.title.string if soup.title else ''
        with SB(uc=True, test=True, locale="en-US", headless2=True) as sb:
            sb.driver.uc_open_with_reconnect(url)
            sb.wait_for_element("body", timeout=10)
            page_text = sb.get_text("body")
            self.text = page_text
    
    def summarize(self, client):
        prompt_list = self.create_prompts()
        response = client.chat.completions.create(
            model = "gpt-4o",
            messages = prompt_list
        )
        print(response.choices[0].message.content)
    
    def create_prompts(self):
        sp = self.system_prompt()
        up = self.user_prompt()
        return [sp,up]
    
    def system_prompt(self):
        sp = {"role" : "system", "content" : "You are an AI assitant which summarizes a website based on the content of the website given. Ignore any navigational elements or accessibility elements present in the webpage content. If any news or posts are present in the website, summarize them too. Provide output in the form of paragraphs."}
        return sp
    
    def user_prompt(self):
        u_con = f"The website with title {self.title} has the following content:\n"
        u_con += self.text
        u_con += "\nPlease provide the summary of the website in paragraphs. If any news material or blog posts are present in it give the summary of those too."
        up = {"role" : "user", "content" : u_con}
        return up

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help = 'Specify the url website to get the summary' )
    args = parser.parse_args()

    load_dotenv()
    client = OpenAI()
    Website(args.url).summarize(client)

