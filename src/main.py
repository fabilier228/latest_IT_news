import requests
from bs4 import BeautifulSoup
import pprint


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k["votes"], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for inx, item in enumerate(links):
        anchor = item.find('a')
        title = anchor.getText() if anchor else None
        href = anchor.get("href") if anchor else None
        vote = subtext[inx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({"title": title, "link": href, "votes": points})
    return hn


def view_few_pages(numOfPages):
    result = []
    for i in range(1, numOfPages + 1):
        res = requests.get(f"https://news.ycombinator.com/news?p={i}")
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.titleline')
        subtext = soup.select('.subtext')
        result.extend(create_custom_hn(links, subtext))

    return sort_stories_by_votes(result)


pprint.pprint(view_few_pages(3))
