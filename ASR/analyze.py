import matplotlib.pyplot as plt
from scipy import stats
import json
from math import log

with open("tst.json") as f:
    s = json.load(f)

def get_total_pdf(dct, length):
    pdfs = []
    for idxs in dct[0][3].values():
       pdfs.append(get_token_pdf(idxs, length))
    return [sum([x[i] for x in pdfs]) for i in range(length)]

def get_token_pdf(idxs, length):
    norms = [stats.norm(float(i), 1) for i in idxs]
    return sum([x.pdf(range(length)) for x in norms])

def get_top_n(pdf, length, n=10):
    top = sorted(range(length), key=lambda x: pdf[x], reverse=True)
    top = top[:n]
    return list(zip(top, [pdf[x] for x in top]))

total = [log(x + 1e-20) for x in get_total_pdf(s, 600)]
plt.plot(total)
plt.savefig("test.jpg")

print(get_top_n(total, 600, 10))