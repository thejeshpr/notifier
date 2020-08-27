from airtable import Airtable


class AirPost(object):
    def __init__(self, base: str, table: str):               
        self.table = table
        self.at = Airtable(base, table)

    def get_all_posts(self):
        """
        return all posts
        """
        return self.at.get_all()
    
    def insert(self, posts, unique_id: str):
        """
        compare and insert new post
        posts = {
            "unique_id":{
                data
            }
        }
        """
        result = self.get_all_posts()
        existing_posts_id = [rec.get('fields').get(unique_id) for rec in result]
        fetched_posts_id = list(posts.keys())
        new_posts_id = list(set(fetched_posts_id) - set(existing_posts_id))
        
        new_posts = [posts[uid] for uid in new_posts_id]        
                
        self.at.batch_insert(new_posts)
        return new_posts
        
    def clean_up(self, threshold, simulate=False):
        """
        clean up posts based on created time by comparing threshold value
        """
        posts_to_remove = []
        formula = f"( DATETIME_DIFF(TODAY(), CREATED_TIME(), 'days') >= {threshold})"
        records = self.at.get_all(formula=formula)

        posts_to_remove = [rec.get("id") for rec in records]
        if not simulate:
            self.at.batch_delete(posts_to_remove)

        return posts_to_remove
        