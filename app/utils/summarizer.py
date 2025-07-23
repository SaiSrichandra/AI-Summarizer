import requests
from bs4 import BeautifulSoup
from seleniumbase import SB
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Create OpenAI client using API key from env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_page_text(url: str) -> tuple[str, str]:
    """
    Uses requests + Selenium to fetch visible page content.
    Returns (title, body_text).
    """
    # Get page title
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    title = soup.title.string if soup.title else ''
    body_text = "Cannot process theis website"
    # Use headless Selenium to get readable page text
    with SB(uc=True, test=True, locale="en-US", headless2=True) as sb:
        sb.driver.uc_open_with_reconnect(url)
        sb.wait_for_element("body", timeout=10)
        body_text = sb.get_text("body")

    return title, body_text


def summarize_url(url: str) -> str:
    """
    Extracts and summarizes a web article using GPT-4o.
    """
    title, body_text = extract_page_text(url)

    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant that summarizes a website based on its content. "
                "Ignore navigation and accessibility elements. Focus on summarizing any news, blog posts, or long-form content. "
                "Return the summary in 2–4 concise paragraphs."
            ),
        },
        {
            "role": "user",
            "content": (
                f"The website titled '{title}' has the following content:\n\n"
                f"{body_text}\n\n"
                "Please summarize the website in paragraphs."
            ),
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    return response.choices[0].message.content.strip()
