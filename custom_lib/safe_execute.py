import traceback

class ExecuteSafe(object):
    def __init__(self):
        pass # define if required

    def execute(self, f, *args, **kwargs):
        data = exeception = tb = None

        try:
            data = f(*args, **kwargs)
            err = False

        except Exception as e:
            err = True
            tb = traceback.format_exc()
            exeception = e
        finally:
            status = not err

        return {
            "status": status,
            "exception": exeception,
            "traceback": tb,
            "data": data
        }