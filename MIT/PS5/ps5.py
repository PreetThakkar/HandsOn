# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

from numpy import true_divide
import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re
# Import to resolve issue with feedparsing and Python 3.10
import collections
collections.Callable = collections.abc.Callable


def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("EST"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

# ======================
# Data structure design
# ======================


class NewsStory:
    def __init__(self, guid, title, description, link, pubdate) -> None:
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self) -> str:
        return self.guid

    def get_title(self) -> str:
        return self.title

    def get_description(self) -> str:
        return self.description

    def get_link(self) -> str:
        return self.link

    def get_pubdate(self) -> datetime:
        return self.pubdate

# ======================
# Triggers
# ======================


class Trigger(object):
    def evaluate(self, story: NewsStory):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


class PhraseTrigger:
    def __init__(self, phrase: str) -> None:
        self.phrase = phrase.lower()

    def is_phrase_in(self, text: str) -> bool:
        clean_word_list = re.split(r"\W+", text.lower())
        # check for boundary after the phrase
        if re.findall(rf"\b{self.phrase}\b", " ".join(clean_word_list)):
            return True
        else:
            return False


class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase: str) -> None:
        super().__init__(phrase)

    def evaluate(self, story: NewsStory) -> bool:
        # ?? create a variable to pass to is_phrase_in function
        return self.is_phrase_in(story.get_title())


class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase: str) -> None:
        super().__init__(phrase)

    def evaluate(self, story: NewsStory) -> bool:
        return self.is_phrase_in(story.get_description())


class TimeTrigger(Trigger):
    def __init__(self, time_str: str) -> None:
        self.time = datetime.strptime(time_str, "%d %b %Y %H:%M:%S")
        self.time = self.time.replace(
            tzinfo=pytz.timezone("EST"))  # set timezone


class BeforeTrigger(TimeTrigger):
    def __init__(self, time_str: str) -> None:
        super().__init__(time_str)

    def evaluate(self, story: NewsStory) -> bool:
        story_time = story.get_pubdate()
        # Make sure both timezones are same
        story_time = story_time.replace(tzinfo=pytz.timezone("EST"))
        return self.time > story_time


class AfterTrigger(TimeTrigger):
    def __init__(self, time_str: str) -> None:
        super().__init__(time_str)

    def evaluate(self, story: NewsStory) -> bool:
        story_time = story.get_pubdate()
        # Make sure both timezones are same
        story_time = story_time.replace(tzinfo=pytz.timezone("EST"))
        return self.time < story_time


class NotTrigger(Trigger):
    def __init__(self, trigger: Trigger) -> None:
        self.trigger = trigger

    def evaluate(self, story: NewsStory) -> bool:
        return not self.trigger.evaluate(story)


class AndTrigger(Trigger):
    def __init__(self, trigger_1: Trigger, trigger_2: Trigger) -> None:
        self.trigger_1 = trigger_1
        self.trigger_2 = trigger_2

    def evaluate(self, story: NewsStory) -> bool:
        return self.trigger_1.evaluate(story) and self.trigger_2.evaluate(story)


class OrTrigger(Trigger):
    def __init__(self, trigger_1: Trigger, trigger_2: Trigger) -> None:
        self.trigger_1 = trigger_1
        self.trigger_2 = trigger_2

    def evaluate(self, story: NewsStory) -> bool:
        return self.trigger_1.evaluate(story) or self.trigger_2.evaluate(story)

# ======================
# Filtering
# ======================


def filter_stories(stories: list[NewsStory], triggerlist: list[Trigger]) -> list[NewsStory]:
    """
    Returns a list of only the stories for which a trigger in triggerlist fires.
    """
    filtered_stories = [
        story for story in stories for trigger in triggerlist if trigger.evaluate(story)]
    print(len(filtered_stories))
    return filtered_stories


# ======================
# User-Specified Triggers
# ======================
def read_trigger_config(filename: str) -> list[Trigger]:
    # Eliminate blanks and comments
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    triggers = {}
    follow_triggers = []
    for line in lines:
        parts = line.split(",")
        if parts[0] != "ADD":
            if parts[1] == "TITLE":
                triggers[parts[0]] = TitleTrigger(parts[2])
            if parts[1] == "DESCRIPTION":
                triggers[parts[0]] = DescriptionTrigger(parts[2])
            if parts[1] == "AFTER":
                triggers[parts[0]] = AfterTrigger(parts[2])
            if parts[1] == "BEFORE":
                triggers[parts[0]] = BeforeTrigger(parts[2])
            if parts[1] == "NOT":
                triggers[parts[0]] = NotTrigger(triggers[parts[2]])
            if parts[1] == "AND":
                triggers[parts[0]] = AndTrigger(
                    triggers[parts[2]], triggers[parts[3]])
            if parts[1] == "OR":
                triggers[parts[0]] = OrTrigger(
                    triggers[parts[2]], triggers[parts[3]])
        else:
            for t in parts[1::]:
                follow_triggers.append(triggers[t])
    return follow_triggers


SLEEPTIME = 120  # seconds -- how often to poll


def main_thread(master):
    try:
        triggerlist = read_trigger_config('triggers.txt')

        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14),
                    yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(
                    END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(
                    END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # RSS Schema difference
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)
            print(stories[0].get_title())
            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
