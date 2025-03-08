import os, requests as req

def test_reverse():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/rbalsa/reverse"
    res = req.post(url, json = {"input": "prova"}).json()
    assert res.get("output") == "prova"[::-1]
