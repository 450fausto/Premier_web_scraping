from links_premier import partidos
import requests as rq
from lxml import html
import pathlib as pl
import csv

# partidos = []

hdr = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
} 
data = []
contador = 0
for partido in partidos:
    contador += 1

    partido = partido.split('/')
    partido.insert(-1,'stats')
    partido = '/'.join(partido)

    ans = rq.get(partido, headers=hdr)
    parser = html.fromstring(ans.text)

    local = parser.xpath('//span[@class="sdc-site-match-stats__team-name"]/text()')
    visit = parser.xpath('//span[@class="sdc-site-match-stats__team-name sdc-site-match-stats__team-name--away"]/text()')
    goals = parser.xpath('//span[@class="sdc-site-match-header__team-score-block"]')
    g_loc = goals[0].xpath('./text()')
    g_vis = goals[1].xpath('./text()')
    m_loc = parser.xpath('//ul[@class="sdc-site-match-header__team-synopsis"][1]/descendant::*/text()')
    m_vis = parser.xpath('//ul[@class="sdc-site-match-header__team-synopsis"][2]/descendant::*/text()')
    fecha = parser.xpath('//time/text()')

    stats = parser.xpath('//div[@class="sdc-site-match-stats__inner"]//div[@class="sdc-site-match-stats__stats"]')

    PossH, PossA = stats[0].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    TSH, TSA = stats[1].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    On_TargetH, On_TargetA = stats[2].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    Off_TargetH, Off_TargetA = stats[3].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    BlockedH, BlockedA = stats[4].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    PassingpcH, PassingpcA = stats[5].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    ClearCutChancesH, ClearCutChancesA = stats[6].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    CornersH, CornersA = stats[7].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    OffsidesH, OffsidesA = stats[8].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    TacklespcH, TacklespcA = stats[9].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    AerialDuelspcH, AerialDuelspcA = stats[10].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    SavesH, SavesA = stats[11].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    FoulsCommittedH, FoulsCommittedA = stats[12].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    FoulsWonH, FoulsWonA = stats[13].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    YellowCardsH, YellowCardsA = stats[14].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    RedCardsH, RedCardsA = stats[15].xpath('.//span[@class="sdc-site-match-stats__val"]/text()')
    detail = parser.xpath('//div[@class="sdc-site-match-header__detail"]/descendant::*/text()')

    partido = partido.replace('stats','teams')
    ans = rq.get(partido, headers=hdr)
    parser = html.fromstring(ans.text)

    Match_Officials = parser.xpath('//dl[@class="sdc-site-team-lineup__officials-list"]/descendant::*/text()')

    data.append([fecha, local, visit, goals, g_loc, g_vis, m_loc, m_vis, PossH, PossA, TSH, TSA, On_TargetH, On_TargetA, Off_TargetH, Off_TargetA, BlockedH, BlockedA, PassingpcH, PassingpcA, ClearCutChancesH, ClearCutChancesA, CornersH, CornersA, OffsidesH, OffsidesA, TacklespcH, TacklespcA, AerialDuelspcH, AerialDuelspcA, SavesH, SavesA, FoulsCommittedH, FoulsCommittedA, FoulsWonH, FoulsWonA, YellowCardsH, YellowCardsA, RedCardsH, RedCardsA, detail, Match_Officials])
    print(contador)

    # if contador>10:
    #     break

home = pl.Path('C:/Users/Usuario/Documents/Web_Scraping_Udemy/Premier_League')
name = 'premier_data.csv'

doc = home / name

if not doc.exists():
    doc.touch()

with doc.open(mode='w', encoding='utf-8') as new:
    
    writer = csv.writer(new, lineterminator='\n')

    for i in data:
        writer.writerow(i)

# with doc.open(mode = 'w') as archivo_script:
#     archivo_script.write('data = ' + str(data))