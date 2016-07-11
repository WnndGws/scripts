'''Tasks:
1) save it all in a dictionary?
2) present us each with 2 options for teams
3) once 16 teams (8 each) have been chosen, progress to second round
    a) print out score from 1st round so we know who won etc.
4) once 2 legs have been played, halve the bracket, if one player has more than 4 teams go through they choose 1 team to keep and 1 team to eliminate
5) repeat'''

import random
import sys

# Get absolute path of the dir script is run from
cwd = sys.path[0]

opponents_dict = {}
scores_dict = {}

with open(cwd + '/wynnammBracket_possible_teams.txt', 'r') as file:
    #possible_teams=file.readlines()
    possible_teams=file.read().splitlines()
random.shuffle(possible_teams) # Randomise teams

if len(possible_teams) < 32:
    raise Exception("Minimum of 32 teams required in text file")

# Create random list of 16 teams each
possible_wyn_teams = possible_teams[:16]
possible_amm_teams = possible_teams[16:32]

# Present 2 teams at a time and have each choose their 8 teams
chosen_wyn_teams = []
chosen_amm_teams = []
print('***Choosing Wyn teams***')
for i, team in enumerate(possible_wyn_teams):
    if i % 2 == 0:
        selection = input("Wyn - Enter 1 for {0} or 2 for {1}: ".format(possible_wyn_teams[i], possible_wyn_teams[i+1]))
        if selection == '1':
            chosen_wyn_teams.append(possible_wyn_teams[i])
        elif selection == '2':
            chosen_wyn_teams.append(possible_wyn_teams[i+1])
print('***Choosing Amm teams***')
for i, team in enumerate(possible_amm_teams):
    if i % 2 == 0:
        selection = input("Amm - Enter 1 for {0} or 2 for {1}: ".format(possible_amm_teams[i], possible_amm_teams[i+1]))
        if selection == '1':
            chosen_amm_teams.append(possible_amm_teams[i])
        elif selection == '2':
            chosen_amm_teams.append(possible_amm_teams[i+1])

print('*****************************')
print(chosen_wyn_teams)
print('*****************************')
print(chosen_amm_teams)

            
#next step: present each with two teams, and save the choice to teams list, and the matchup to opponentsDict
