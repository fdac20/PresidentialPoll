
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import plotly.graph_objects as go
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import plotly.offline as offline



############################################
class winner_info:
    name = ''
    candidate_votes = 0
    total_votes = 0
    party = ''
    def __init__(self, name, candidate_votes, total_votes, party):
        self.name = name
        self.candidate_votes = candidate_votes
        self.total_votes = total_votes
        self.party = party

# read in file
my_file = pd.read_csv('1976-2016-president.csv', encoding = 'unicode_escape')


# Locate a specfic file element
state_loc = my_file.loc[my_file['state'] == 'Alabama']
#print(state_loc)

election_years = [1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016]
states = ['New Jersey',
    'Alaska',
    'Hawaii',
    'Rhode Island',
    'Massachusetts',
    'Connecticut',
    'Maryland',
    'New York',
    'Delaware',
    'Florida',
    'Ohio',
    'Pennsylvania',
    'Illinois',
    'California',
    'Virginia',
    'Michigan',
    'Indiana',
    'North Carolina',
    'Georgia',
    'Tennessee',
    'New Hampshire',
    'South Carolina',
    'Louisiana',
    'Kentucky',
    'Wisconsin',
    'Washington',
    'Alabama',
    'Missouri',
    'Texas',
    'West Virginia',
    'Vermont',
    'Minnesota',
    'Mississippi',
    'Iowa',
    'Arkansas',
    'Oklahoma',
    'Arizona',
    'Colorado',
    'Maine',
    'Oregon',
    'Kansas',
    'Utah',
    'Nebraska',
    'Nevada',
    'Idaho',
    'New Mexico',
    'South Dakota',
    'North Dakota',
    'Montana',
    'Wyoming',
    'District of Columbia']

# sort by name so it looks nice
states = sorted(states)

# dict for storing years as key and then dict of states as vals
slides = {}
slides = dict((year,None) for year in election_years)
# create dict 

#for year in election_years:
#    slides[year] = None
print(slides)
print("states len", len(states))
#print(dict(states))
# dict

# go through each year 
for year in election_years:
    
    # create state dict for that year 
    slides[year] = dict((s,None) for s in states)
    
    # get all data for that year
    year_info = my_file.loc[my_file['year'] == year]
    for state in states:
        state_info = year_info.loc[year_info['state'] == state]
        
        state_winner = state_info[state_info['candidatevotes']==state_info['candidatevotes'].max()]
        
        
        name = str(state_winner['candidate'].values[0])
        candidate_votes = int(state_winner['candidatevotes'].values[0])
        total_votes = int(state_winner['totalvotes'].values[0])
        party = str(state_winner['party'].values[0])
        if(party == 'democratic-farmer-labor'): party ='democrat'
            
        slides[year][state] = winner_info(name, candidate_votes, total_votes, party)
        

setColor = {}

#1976    
for YEAR, STATES in slides.items():
    if YEAR == 1976:
        print("Year: ", YEAR)
        setYear = YEAR
        for STATE, WINNER in STATES.items():
            print("\tState: ", STATE)
            print("\tWinner: ", WINNER.name)
            print("\tcandidate_votes: ", WINNER.candidate_votes, ", total_votes: ", WINNER.total_votes, ", party: ", WINNER.party)
            print()
            if WINNER.party == "democrat":
                setColor[STATE] = 50
            if WINNER.party == "republican":
                setColor[STATE] = 100


years = []
WinnerVotes = {}
LoserVotes ={}
PieVotes = {}
votesBar = 0  
votesLine = 0
votesPieD = 0   
votesPieR = 0    
for YEAR, STATES in slides.items():
    #print("Year: ", YEAR)
    years.append(YEAR)
    for STATE, WINNER in STATES.items():
        #print("\tState: ", STATE)
        #print("\tWinner: ", WINNER.name)
        #print("\tcandidate_votes: ", WINNER.candidate_votes, ", total_votes: ", WINNER.total_votes, ", party: ", WINNER.party)
        #print()
        votesBar += WINNER.candidate_votes
        votesLine = WINNER.total_votes - WINNER.candidate_votes 
        if WINNER.party == 'democrat':
            votesPieD += WINNER.candidate_votes       
        if WINNER.party == 'republican':
            votesPieR += WINNER.candidate_votes
    WinnerVotes[YEAR] = votesBar
    LoserVotes[YEAR] = votesLine
    PieVotes["democrat"] = votesPieD
    PieVotes["republican"] = votesPieR
    votesBar = 0  
    votesLine = 0
    votesPieD = 0   
    votesPieR = 0  
    

          
        
###############################################

## Plot U.S. Map

#print(slides)
fig = plt.figure(1)
ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.LambertConformal())

ax.set_extent([-125, -66.5, 20, 50], ccrs.Geodetic())

shapename = 'admin_1_states_provinces_lakes_shp'


states_shp = shpreader.natural_earth(resolution='110m',
                                     category='cultural', name=shapename)


## Maybe here is where we can parse the information from the file into the correct states?


ax.background_patch.set_visible(False)
ax.outline_patch.set_visible(False)


ax.set_title("Presidential Election: " + str(setYear))

#for state in shpreader.Reader(states_shp).geometries():
for astate in shpreader.Reader(states_shp).records():
    

    ### You want to replace the following code with code that sets the
    ### facecolor as a gradient based on the population density above
    #facecolor = [0.9375, 0.9375, 0.859375]

    edgecolor = 'black'

    try:
        # use the name of this state to get pop_density
        state_dens = setColor[ astate.attributes['name'] ]
    except:
        state_dens = 0

    # simple scheme to assign color to each state
    if state_dens == 100:
        facecolor = "red"
    else:
        facecolor = "blue"

    # `astate.geometry` is the polygon to plot
    ax.add_geometries([astate.geometry], ccrs.PlateCarree(),
                      facecolor=facecolor, edgecolor=edgecolor)


#### Code for slider ####
a0 = 5
axcolor = 'lightgoldenrodyellow'
axamp = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
samp = Slider(axamp, 'Amp', 0.1, 10.0, valinit=a0)
plt.savefig('StatesGraph.png')




# Bar Graph Code for Total number of Votes to Win over Time 
plt.figure(2)
yValues =[]
plt.style.use('ggplot')
for i in years:
    yValues.append(WinnerVotes.get(i))
    print(i)

for i in yValues:
    print(i)

plt.bar(years, yValues, color='green')
plt.xlabel("Year")
plt.ylabel("Total Votes")
plt.title("Total Votes to Win Over Time")
plt.savefig('barGraph.png')

# Line Graph Code for difference in vote between winner and loser 
plt.figure(3)
yLine =[]
plt.style.use('ggplot')
for i in years:
    yLine.append(LoserVotes.get(i))
    print(i)

for i in yLine:
    print(i)

plt.plot(years, yLine, color='blue')
plt.xlabel("Year")
plt.ylabel("Total Votes less than Winner Votes")
plt.title("Difference in Vote between Winner/Loser")
plt.savefig('LineGraph.png')


plt.figure(4)
# Pie Graph Code for average % of vote Republican and Democrat 
labels = 'Republican', 'Democrat'
sizes = [PieVotes.get('republican'),PieVotes.get('democrat')]
print("Dem Votes: ", PieVotes.get('democrat'))
print("Rep Votes: ", PieVotes.get('republican'))

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Average Percent of Votes Rep VS Dem")
plt.savefig('PieGraph.png')


plt.show()






