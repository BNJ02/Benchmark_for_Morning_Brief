from GoogleNews import GoogleNews
googlenews = GoogleNews()

googlenews.set_lang('fr')
googlenews.set_period('1d')
googlenews.set_encode('utf-8')
# googlenews.set_time_range('08/11/2024','08/11/2024')

googlenews.get_news('Sports')


result = googlenews.results()
print("Total news : ",len(result))
for x in result:
    print("Title-->",x['title'])
    print("Media-->",x['media'])
    print("Date and Time-->",x['date'])
    print("Link-->",x['link'])
    print("-"*50)

media_set = set()  # Crée un ensemble vide pour stocker les médias uniques

for x in result:
    media_set.add(x['media'])  # Ajoute le média à l'ensemble

print("Liste des médias du jour :")
for media in media_set:
    print(media)

googlenews.clear()