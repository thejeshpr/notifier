import os
import traceback

from bs4 import BeautifulSoup
import requests

from .TelePusher import TelePusher

class StatusCodeException(Exception):
    """
    Custom exception class
    """
    pass

class Course(object):
    def __init__(self):
        self.url = os.environ.get("COURSE_URL")
        self.pusher = TelePusher()

    def send_latest_courses(self):
        try:
            res = requests.get(self.url)

            if not res.status_code in [200]:
                raise StatusCodeException(f"An error occurred while retreiving the data, {res.status_code}\n{res.content}")
            
            soup = BeautifulSoup(res.content, 'html.parser')
            ul = soup.find('ul', {'id':'posts-container'})

            courses = []

            for li in ul.find_all('li'):
                link = li.find('h3').find('a').get('href')
                title = li.find('h3').find('a').text.strip()
                courses.append(f"{title}\n{link}\n")
            
            msg = "\n".join(courses)
            error = False

        except Exception as e:
            error = True
            tb = traceback.format_exc()
            msg = f"An error occurred while fetching the courses: {e}\n\n{tb}"

        finally:
            status = "Success" if not error else "Failure"
            msg = f"Courses: {status}\n\n{msg}"            
            self.pusher.send_message(msg, disable_web_page_preview="True")