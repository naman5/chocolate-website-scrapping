import codecademylib3_seaborn
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#exploring the webpage

webpage = requests.get('https://content.codecademy.com/courses/beautifulsoup/cacao/index.html', 'html.parser')
soup = BeautifulSoup(webpage.content)
ratings = []

#to find how ratings are distributed

for i in soup.find_all(attrs = {'class': 'Rating'}):
  j = i.get_text('td')
  if j != "Rating":
    ratings.append(float(j))
print(ratings)
plt.hist(ratings)
plt.show()

#to find which chocolatier makes the best chocolate

print(soup.select(".Company"))
company_names = []
for c in soup.select(".Company"):
  company_names.append(c.get_text(""))
company_names.pop(0)
company_rating = list(zip(company_names, ratings))
df = pd.DataFrame(company_rating, columns = ['company_names', 'ratings'])
print(df)
mean_vals = df.groupby("company_names").ratings.mean()
ten_best = mean_vals.nlargest(10)
print(ten_best)

# To find is more cacao better?

print(soup.select(".CocoaPercent"))
cocoa_percent = []
for c in soup.select(".CocoaPercent"):
  cocoa_percent.append(c.get_text(""))
cocoa_percent.pop(0)
print(cocoa_percent)
percent = []
for n in cocoa_percent:
  n = int(float(n[:-1]))
  percent.append(n)
print(percent)
df["CocoaPercent"] = percent
print(df)
plt.scatter(df.CocoaPercent, df.ratings)
z = np.polyfit(df.CocoaPercent, df.ratings, 1)
line_function = np.poly1d(z)
plt.plot(df.CocoaPercent, line_function(df.CocoaPercent), "r--")
plt.show()
plt.clf()
