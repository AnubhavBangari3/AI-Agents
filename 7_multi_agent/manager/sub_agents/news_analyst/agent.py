import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


local_model = LiteLlm(model="ollama_chat/mistral:latest")


def search_news(query: str) -> dict:
    """
    Searches Google News RSS without using a paid API.
    Returns recent news titles and links.
    """

    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)

        items = []
        for item in root.findall(".//item")[:5]:
            title = item.findtext("title", default="")
            link = item.findtext("link", default="")
            pub_date = item.findtext("pubDate", default="")

            items.append(
                {
                    "title": title,
                    "link": link,
                    "published": pub_date,
                }
            )

        return {
            "status": "success",
            "query": query,
            "articles": items,
        }

    except Exception as e:
        return {
            "status": "error",
            "query": query,
            "message": str(e),
        }


news_analyst = Agent(
    name="news_analyst",
    model=local_model,
    description="Agent that searches and summarizes recent news.",
    instruction="""
You are a news analyst.

When the user asks for news, use search_news.

After getting results:
Summarize the top news clearly.
Mention the title and published date if available.
Keep the answer concise.
""",
    tools=[search_news],
)