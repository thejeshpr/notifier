from notifier.grabbers.base import Base, Internet

class GH(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):

        repos = Internet.get(
            url=obj.sync_type.base_url,
            return_json=True,
            params={"since": "dialy"}
        )

        for repo in repos:
            obj.add_text_task(task_id=repo['url'], data=dict(text=repo['url']))