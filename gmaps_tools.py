import googlemaps


gmaps = googlemaps.Client(key=API_key)

origin = (29.755537,-95.372003)
destination = (29.716361,-95.409329)

matrix = gmaps.distance_matrix(origins=origin, destinations=destination, mode='driving', traffic_model='best_guess')
