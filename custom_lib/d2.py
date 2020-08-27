import os
import traceback
import urllib.parse

from custom_lib.base import Base

D2_BASE_URL = os.environ.get('D2_BASE_URL')
THRESHOLD = os.environ.get("D2_THRESHOLD")
D2_TELEGRAM_CHANNEL = os.environ.get("D2_TELEGRAM_CHANNEL")

class D2(Base):
    """
    """
    def send_latest_posts(self):
        try:
            soup = self.get_soup(D2_BASE_URL)
            divs = soup.find_all('div', {'class':'crayons-story__indention'})

            posts = {}
            ids = {}

            for div in divs:
                a = div.find('a')
                id_ = a.get('id').strip()                
                posts[id_] = {
                    "id": id_,
                    "title": a.text.strip(),
                    "link": urllib.parse.urljoin(D2_BASE_URL, a.get('href'))
                }
                ids[id_] = {"id":id_}
                        
            inserted_ids = self.ap.insert(ids, "id")
            inserted_posts = [posts[rec.get('id')] for rec in inserted_ids]

            self.tl.send_message(f"sending {len(inserted_posts)} posts")
            self.tl_send_msg(inserted_posts, "link", parse_mode="")
        
        except Exception as e:
            self.tl.send_message(f"Error: {e}")            
            print(traceback.format_exc())
    
    def remove_posts(self, simulate):        
        """
        remove articles
        """
        try:            
            removed_posts = self.ap.clean_up(THRESHOLD, simulate=simulate)        
            self.tl.send_message(f"{len(removed_posts)} posts deleted")
        except Exception as e:
            self.tl.send_message(f"An error occured while clean-up: {e}")
            print(traceback.format_exc())
        



