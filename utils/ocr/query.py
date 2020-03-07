import json

dict = {
  "Italy": [
    "https://www.football-italia.net/Azzurri",
    "https://www.football-italia.net/Azzurri"
  ],
  "Puma": [
    "http://www.puma.com/",
    "http://www.puma.com/"
  ],
  "Fifa": [
    "https://www.fifa.com",
    "https://www.fifa.com"
  ],
  "Tottenham-Hotspur": [
    "https://www.tottenhamhotspur.com/",
    "https://www.tottenhamhotspur.com/"
  ],
  "Inter-Milan": [
    "https://www.inter.it/en/hp",
    "https://www.inter.it/en/hp"
  ],
  "Borussia-Dortmund": [
    "https://www.bvb.de/eng",
    "https://www.bvb.de/eng"
  ],
  "Lazio": [
    "http://www.sslazio.it/en",
    "http://www.sslazio.it/en"
  ],
  "adidas": [
    "https://www.adidas.com/us",
    "https://www.adidas.com/us"
  ],
  "Tornino": [
    "http://torinofc.it/en",
    "http://torinofc.it/en"
  ],
  "Uefa": [
    "https://www.uefa.com/",
    "https://www.uefa.com/"
  ],
  "Bayern-Munich": [
    "https://fcbayern.com/en",
    "https://fcbayern.com/en"
  ],
  "Volkswagen": [
    "http://www.vw.com/",
    "http://www.vw.com/"
  ],
  "Paris-saint-Germain": [
    "https://www.psg.fr/",
    "https://www.psg.fr/"
  ],
  "Valencia": [
    "http://en.valenciacf.com/",
    "http://en.valenciacf.com/"
  ],
  "Torino": [
    "http://torinofc.it/en",
    "http://torinofc.it/en"
  ],
  "Milan": [
    "https://www.acmilan.com/en",
    "https://www.acmilan.com/en"
  ],
  "Manchester-United": [
    "https://www.manutd.com/",
    "https://www.manutd.com/"
  ],
  "Liverpool": [
    "https://www.liverpoolfc.com/welcome-to-liverpool-fc",
    "https://www.liverpoolfc.com/welcome-to-liverpool-fc"
  ],
  "Barcelona": [
    "https://www.fcbarcelona.com/",
    "https://www.fcbarcelona.com/"
  ],
  "Atletico-Madrid": [
    "http://en.atleticodemadrid.com/",
    "http://en.atleticodemadrid.com/"
  ],
  "LaLiga": [
    "https://www.laliga.es/en",
    "https://www.laliga.es/en"
  ],
  "Porto": [
    "http://www.fcporto.pt/en/Pages/fc-porto.aspx",
    "http://www.fcporto.pt/en/Pages/fc-porto.aspx"
  ],
  "LFP": [
    "https://www.lfp.fr/",
    "https://www.lfp.fr/"
  ],
  "Ajax": [
    "http://english.ajax.nl/",
    "http://english.ajax.nl/"
  ],
  "Olympique-Lyonnais": [
    "https://www.ol.fr/en",
    "https://www.ol.fr/en"
  ],
  "Volksvagen": [
    "http://www.vw.com/",
    "http://www.vw.com/"
  ],
  "Nottingham-Forest": [
    "https://www.nottinghamforest.co.uk/",
    "https://www.nottinghamforest.co.uk/"
  ],
  "Premier-league": [
    "https://www.premierleague.com/matchweek/3261/blog",
    "https://www.premierleague.com/matchweek/3261/blog"
  ],
  "Manchester-city": [
    "https://www.mancity.com/",
    "https://www.mancity.com/"
  ],
  "Juventus": [
    "http://www.juventus.com/en/",
    "http://www.juventus.com/en/"
  ],
  "Nike": [
    "https://www.nike.com/",
    "https://www.nike.com/"
  ],
  "Olympique-de-Marseille": [
    "https://www.om.net/en",
    "https://www.om.net/en"
  ],
  "Fulham": [
    "http://www.fulhamfc.com/",
    "http://www.fulhamfc.com/"
  ],
  "Everton": [
    "http://www.evertonfc.com/",
    "http://www.evertonfc.com/"
  ],
  "Benfica": [
    "https://www.slbenfica.pt/en-us",
    "https://www.slbenfica.pt/en-us"
  ],
  "Roma": [
    "http://www.asroma.com/en/tag/en/gallery",
    "http://www.asroma.com/en/tag/en/gallery"
  ],
  "Real-Madrid": [
    "https://www.realmadrid.com/en",
    "https://www.realmadrid.com/en"
  ],

  "Premier-League": [
    "https://www.premierleague.com/matchweek/3261/blog",
    "https://www.premierleague.com/matchweek/3261/blog"
  ],
  "Leicester-City": [
    "https://www.lcfc.com/",
    "https://www.lcfc.com/"
  ],
  "Celtic": [
    "http://www.celticfc.net/",
    "http://www.celticfc.net/"
  ],
  "Adidas": [
    "https://www.adidas.com/us",
    "https://www.adidas.com/us"
  ],
  "Paris-Saint-Germain": [
    "https://www.psg.fr/",
    "https://www.psg.fr/"
  ],
  "Arsenal": [
    "https://www.arsenal.com/live#!timeline",
    "https://www.arsenal.com/live#!timeline"
  ],
  "Chelsea": [
    "https://www.chelseafc.com/en",
    "https://www.chelseafc.com/en"
  ],
  "Real-madrid": [
    "https://www.realmadrid.com/en",
    "https://www.realmadrid.com/en"
  ],
  "Monako": [
    "http://www.asmonaco.com/en/",
    "http://www.asmonaco.com/en/"
  ],
  "Manchester-City": [
    "https://www.mancity.com/",
    "https://www.mancity.com/"
  ],
  "Santos": [
    "https://www.santosfc.com.br/en/",
    "https://www.santosfc.com.br/en/"
  ],
  "Laliga": [
    "https://www.laliga.es/en",
    "https://www.laliga.es/en"
  ],
  "FedEx": [
    "https://www.fedex.com/en-us/home.html",
    "https://www.fedex.com/en-us/home.html"
  ],
  "Beko": [
    "http://www.beko.com/",
    "http://www.beko.com/"
  ],
  "Sevilla": [
    "https://www.sevillafc.es/en",
    "https://www.sevillafc.es/en"
  ],
  "Napoli": [
    "http://www.sscnapoli.it/prehome/html/index.html",
    "http://www.sscnapoli.it/prehome/html/index.html"
  ],
  "McDonald's": [
    "https://www.mcdonalds.com/",
    "https://www.mcdonalds.com/"
  ],
  "Audi": [
    "https://www.audi.com/",
    "https://www.audi.com/"
  ],
  "Kappa": [
    "https://kappa-usa.com/",
    "https://kappa-usa.com/"
  ],
  "Chevrolet": [
    "https://www.chevrolet.com/",
    "https://www.chevrolet.com/"
  ],
  "Hyundai": [
    "https://www.hyundai.com/worldwide/en",
    "https://www.hyundai.com/worldwide/en"
  ],
  "Ford": [
    "https://www.ford.com/",
    "https://www.ford.com/"
  ],
  "Bayer-04-Leverkusen": [
    "https://www.bayer04.de/en-us/page/business",
    "https://www.bayer04.de/en-us/page/business"
  ],
  "TSG-1899-Hoffenheim": [
    "https://www.bundesliga.com/en/clubs/tsg-1899-hoffenheim.jsp",
    "https://www.bundesliga.com/en/clubs/tsg-1899-hoffenheim.jsp"
  ],
  "Parma-Calcio-1913": [
    "http://parmacalcio1913.com/?lang=en",
    "http://parmacalcio1913.com/?lang=en"
  ],
  "Fortuna-D\u00fcsseldorf": [
    "https://www.f95.de/home/",
    "https://www.f95.de/home/"
  ],
  "TAG-Heuer": [
    "https://www.tagheuer.com/en",
    "https://www.tagheuer.com/en"
  ],
  "Eintracht-Frankfurt": [
    "https://www.eintracht.de/en/news/",
    "https://www.eintracht.de/en/news/"
  ],
  "FSV-Mainz-05": [
    "https://www.mainz05.de/en/",
    "https://www.mainz05.de/en/"
  ],
  "FC-Schalke-04": [
    "https://schalke04.de/en/",
    "https://schalke04.de/en/"
  ],
  "TEDi": [
    "https://www.tedi.com/en/",
    "https://www.tedi.com/en/"
  ],
  "Hannover-96": [
    "https://www.hannover96.de/startseite.html",
    "https://www.hannover96.de/startseite.html"
  ],
  "SC-Freiburg": [
    "https://www.scfreiburg.com/",
    "https://www.scfreiburg.com/"
  ],
  "VfB-Stuttgart": [
    "https://www.vfb.de/en/",
    "https://www.vfb.de/en/"
  ],
  "RB-Leipzig": [
    "https://www.bundesliga.com/en/clubs/rb-leipzig.jsp",
    "https://www.bundesliga.com/en/clubs/rb-leipzig.jsp"
  ],
  "FC-K\u00f6ln": [
    "https://us.soccerway.com/teams/germany/1-fc-koln/980/",
    "https://us.soccerway.com/teams/germany/1-fc-koln/980/"
  ],
  "Hertha-BSC": [
    "https://www.herthabsc.de/en/",
    "https://www.herthabsc.de/en/"
  ],
  "Germany": [
    "https://www.facebook.com/DFBTeamEN/",
    "https://www.facebook.com/DFBTeamEN/"
  ],
  "FC-Nurnberg": [
    "https://www.fcn.de/home/",
    "https://www.fcn.de/home/"
  ],
  "SV-Werder-Bremen": [
    "https://www.werder.de/en",
    "https://www.werder.de/en"
  ],
  "Serie-A": [
    "http://www.legaseriea.it/en/",
    "http://www.legaseriea.it/en/"
  ],
  "Beretta": [
    "http://www.beretta.com/en/",
    "http://www.beretta.com/en/"
  ],
  "Borussia-Mönchengladbach": [
    "https://www.borussia.de/english/home.html",
    "https://www.borussia.de/english/home.html"
  ],
  "SAP": [
    "https://www.sap.com/index.html",
    "https://www.sap.com/index.html"
  ],
  "Umbro": [
    "https://www.umbro.com/en-us/",
    "https://www.umbro.com/en-us/"
  ],
  "Lotto-Sport-Italia": [
    "https://www.lotto.it/",
    "https://www.lotto.it/"
  ]
}

with open('data/search/training_data/team_links_with_previous', 'w') as output_file:
    json.dump(dict, output_file)
