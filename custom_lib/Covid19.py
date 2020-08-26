from datetime import datetime
import requests
import traceback

from .TelePusher import TelePusher


class Covid19():
    def __init__(self):
        self.__url = "https://api.covid19india.org/state_district_wise.json"

    def get_stats(self):
        try:            
            res = requests.get(self.__url)
            if res.status_code in [200]:
                data = res.json()
                kar_data = data['Karnataka']['districtData']

                stats = []                
                stats.append("-"*40)

                for dis, val in kar_data.items():
                    if dis == "Mandya":
                        stats.append(f"*District:* {dis}")
                        stats.append(f"*Active:* {val.get('active')}")
                        stats.append(f"*Confirmed:* {val.get('confirmed')}")
                        stats.append(f"*Deceased:* {val.get('deceased')}")
                        stats.append("\n")

                stats.append("https://www.covid19india.org")                            
                
                msg = '\n'.join(stats)
                tb = ""
                error = False
        except Exception as e:
            error = True
            tb = traceback.format_exc()
            msg = "{}\n{}".format(e, tb)

        finally:
            print(tb)
            status = "Success" if not error else "Error"
            msg = f"*Covid-19 Update: {status}*\n\n{msg}"
            pusher = TelePusher()
            pusher.send_message(msg, disable_web_page_preview="True")