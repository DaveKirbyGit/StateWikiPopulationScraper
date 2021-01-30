# necessary import statements
import urllib.request
from bs4 import BeautifulSoup
import re
import numpy as np
from matplotlib import pyplot as plt

# create some objects with urllib.request and BS4 to target the appropriate webpage
url = "https://en.wikipedia.org/wiki/Hawaii"
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'lxml')

# our target table is the only one with class='toccolours'
table = soup.find('table', class_='toccolours')

# create some empty lists for our scraped data
year_list = []
population_list = []

# the numerical data we want begins on the second table row,
# and our desired data cells are tagged as either <th> or <td>,
# so a for-loop on a targeted slice can use a regular expression to filter the data
for row in table.find_all('tr')[1:]:
    columns = row.find_all(re.compile(r"^t[hd]"))
    if len(columns) == 3:
        year_list.append(columns[0].text)
        population_list.append(columns[1].text)
        
print(year_list)
print(population_list)

# time to clean up our data and convert it to integers!

year_list_ints = []
population_list_ints = []

# we use a regular expression object to convert each of the various entry formats
# in the original table's year cells to a uniform 4-digit format,
# and we convert to integers
year_pattern = re.compile(r"\b\d{4}")
for i in range(len(year_list)):
    year = year_pattern.findall(year_list[i])
    year_list_ints.append(int(year[0]))

# we use the .replace() method to remove commas from the entries in the
# original table's population cells, and we convert to integers
for i in range(len(population_list)):
    population = population_list[i].replace(',','')
    population_list_ints.append(int(population))
    
print(year_list_ints)
print(population_list_ints)

# convert our integer lists to NumPy arrays
x = np.array(year_list_ints)
y = np.array(population_list_ints)

# create and format a MatPlotLib plot
plt.figure(figsize=(20,12))
plt.plot(x,y, linewidth=5, marker='o', markersize=12)

plot_font = {'size' : 24,
        'weight': 'bold'
       }

axis_font = {'size' : 15,
        'weight': 'bold'
       }

plt.title("Historical Population of Hawaii", fontdict=plot_font)

# the original string values for year entries will be our xticks
plt.xticks(year_list_ints, year_list, rotation=90)

# format the y-axis ticks to display full numbers rather than scientific notation
plt.ticklabel_format(axis='y', style='plain')

# format the axis labels
plt.xlabel('Year', fontdict=axis_font)
plt.ylabel('Population', fontdict=axis_font)


# display the plot
plt.show()