

class T(object):

    def test(self, url, d=None):
        print(url, d)


d = [
    {
        "url": "url1",
        "d": "d1"
    },
    {
        "url": "url2"
    }
]        

t = T()
for x in d:
    t.test(**x)
