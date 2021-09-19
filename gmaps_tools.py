import googlemaps
API_key = 'AIzaSyAalBg0cbYTnXXWzkr3jkanvpUAhA2WdSA'

gmaps = googlemaps.Client(key=API_key)

origin = gmaps.revese_geocode(29.755537,-95.372003)
destination = gmaps.reverse_geocode(29.716361,-95.409329)

matrix = gmaps.distance_matrix(origins=origin, destinations=destination, mode='driving', traffic_model='best_guess')
