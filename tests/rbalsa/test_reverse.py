import sys 
sys.path.append("packages/rbalsa/reverse")
import reverse

def test_reverse():
    res = reverse.reverse({"input": "prova"})
    assert res["output"] == "prova"[::-1]
