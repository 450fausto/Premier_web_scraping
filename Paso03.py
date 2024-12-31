import numpy as np
import pandas as pd

column_names = ['Date', 'local', 'visit', 'goals', 'g_loc', 'g_vis', 'm_loc', 
                'm_vis', 'PossH', 'PossA', 'TSH', 'TSA', 'On_TargetH', 
                'On_TargetA', 'Off_TargetH', 'Off_TargetA', 'BlockedH', 
                'BlockedA', 'PassingpcH', 'PassingpcA', 'ClearCutChancesH', 
                'ClearCutChancesA', 'CornersH', 'CornersA', 'OffsidesH', 
                'OffsidesA', 'TacklespcH', 'TacklespcA', 'AerialDuelspcH', 
                'AerialDuelspcA', 'SavesH', 'SavesA', 'FoulsCommittedH', 
                'FoulsCommittedA', 'FoulsWonH', 'FoulsWonA', 'YellowCardsH', 
                'YellowCardsA', 'RedCardsH', 'RedCardsA', 'detail', 
                'Match_Officials']

dirty00 = pd.read_csv("premier_data.csv")

dirty01 = dirty00.copy()
dirty01.loc[dirty01.shape[0],:] = dirty00.columns    # insert the columns into the dataframe
dirty01.columns = column_names   # change the column names

dirty02 = dirty01.copy()
dirty02.drop(columns='goals', inplace=True)                                     # The goals column is an undesired column

dirty03 = dirty02.copy()
def extract_time(x):
  time = x.split(',')[0]
  if time[-2:]=='pm':
    hour = int(time.split(':')[0].replace("['", ''))+12
    return str(hour)+':'+time.split(':')[1][:2]
  else:
    return time.replace('am', '')
dirty03['Time'] = dirty02.Date.apply(extract_time)
new_columns = column_names[:]
new_columns.remove('goals')
new_columns.insert(1,'Time')
dirty03 = dirty03.reindex(columns = new_columns)

date = dirty03.Date.str.extract('([0-9]*[a-z]+ [A-Z][a-z]+ [0-9]+)')         # extract the date as: '22nd May 2022'
def date_transform(x):                                                           # make a function to transform the format '22nd May 2022' in '22/05/2022'
  if type(x)==float:
    return x
  new = x.split(' ')
  day = ''.join(i for i in new[0] if i in '0123456789')
  month = new[1]
  dict_months = {'January':'01', 'February':'02', 'March':'03', 'April':'04',
                 'May':'05', 'August':'08', 'September':'09', 'October':'10',
                 'November':'11', 'December':'12'}
  year = new[2]
  return '/'.join([day, dict_months[month], year])
dirty04 = dirty03.copy()
dirty04['Date'] = date[0].apply(date_transform)

dirty05 = dirty04.copy()
dirty05['local'] = dirty04.local.apply(lambda x: ''.join([i for i in x if i not in "[']"]))
dirty05['visit'] = dirty04.visit.apply(lambda x: ''.join([i for i in x if i not in "[']"]))
dirty05['g_loc'] = dirty04.g_loc.apply(lambda x: int(''.join([i for i in x if i not in "[']"])))
dirty05['g_vis'] = dirty04.g_vis.apply(lambda x: int(''.join([i for i in x if i not in "[']"])))

import re
dirty06 = dirty05.copy()
for i in range(dirty05.shape[0]):
  patron = re.compile('["][0-9]+')
  numloc = int(dirty05.g_loc[i])
  numvis = int(dirty05.g_vis[i])
  if numloc>0:
    dirty06.m_loc[i] = [int(i[1:]) for i in patron.findall(dirty05.m_loc[i])[:numloc]]
  else:
    dirty06.m_loc[i] = []
  if numvis>0:
    dirty06.m_vis[i] = [int(i[1:]) for i in patron.findall(dirty05.m_vis[i])[:numvis]]
  else:
    dirty06.m_vis[i] = []

dirty07 = dirty06.copy()
dirty07['Stadium'] = ''
for i in range(dirty06.shape[0]):
  dirty07['Stadium'][i] = dirty06['detail'][i].split('\\n')[5].split(',')[1].replace("'",'').strip()

dirty08 = dirty07.copy()
dirty08['Attendance'] = ''
patron = re.compile('\d+,\d+')
for i in range(dirty07.shape[0]):
  found = patron.findall(dirty07['detail'][i])
  if len(found)>0:
    dirty08['Attendance'][i] = ''.join([i for i in found[0] if i not in ','])
  else:
    dirty08['Attendance'][i] = None
dirty08.drop(columns='detail', inplace=True)

dirty09 = dirty08.copy()
dirty09['Referee'] = ''
dirty09['Assistants'] = ''
dirty09['Fourth_official'] = ''
# dirty09['VAR'] = ''
# dirty09['Assistant_VAR'] = ''
for i in range(dirty08.shape[0]):
  lst = dirty08['Match_Officials'][i][2:-2].split("', '")
  if len(lst)>0:
    print(i)
    dirty09['Referee'][i] = lst[1]
    dirty09['Assistants'][i] = lst[3]
    if i not in  [117,133, 161, 162, 191]:
      dirty09['Fourth_official'][i] = lst[5]
    # dirty09['VAR'][i] = lst[7]
    # if i!=314:
    #   dirty09['Assistant_VAR'][i] = lst[9]
dirty09.drop(columns = 'Match_Officials', inplace = True)

dirty09.to_csv('premier_cleaned.csv', index = False)

