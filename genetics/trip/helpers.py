import time


flight_data = open('flights.txt')

# POA - Porto Alegre, GYN - Goiania, CNF - Belo Horizonte,
# FLN - Floripa, GIG - Rio de Janeiro, CWB - Curitiba
friends = [('Aildson', 'POA'), ('Thiago', 'GYN'), ('George', 'CNF'),
           ('Julian', 'FLN'), ('Péricles', 'GIG'), ('Maigan', 'CWB')]

# qty. flights * (qty. friends * 2)
# 2 = 1 flight to destination + 1 flight from destination
domain = [(0, 9)] * (len(friends) * 2)

destination = 'REC'

flights = {}  # flight dictionary

for flight in flight_data:
    origin, destination, departure, arrival, price = flight.split(',')
    flights.setdefault((origin, destination), [])  # () => (key, value)
    flights[(origin, destination)].append((departure, arrival, int(price)))


def build_schedule(schedule):  # build a schedule based on a given solution
    flight_id = -1

    for i in range(len(schedule) // 2):
        name = friends[i][0]
        origin = friends[i][1]

        flight_id += 1
        trip = flights[(origin, destination)][schedule[flight_id]]

        flight_id += 1
        homecoming = flights[(destination, origin)][schedule[flight_id]]

        print(
            '%10s%6s -> %s %5s-%5s, $%3s %6s -> %s %5s-%5s, $%3s' %
            (name, origin, destination, trip[0],
             trip[1],
             trip[2],
             destination,
             origin,
             homecoming[0],
             homecoming[1],
             homecoming[2]))


def get_minutes(hour):  # converts a time string to time in minutes (int)
    parsed_hour = time.strptime(hour, '%H:%M')
    minutes = parsed_hour[3] * 60 + parsed_hour[4]
    return minutes  # ('2:00') -> 120


def cost_function(solution):  # fitness function
    cost = 0
    wait_time = 0  # wait time of the first arrival to the last one
    last_arrival = 0  # last person to arrive at destination
    first_departure = get_minutes('23:59')  # first person to go back home
    flight_id = -1

    for i in range(len(solution) // 2):
        origin = friends[i][1]

        flight_id += 1
        trip = flights[(origin, destination)][solution[flight_id]]

        flight_id += 1
        homecoming = flights[(destination, origin)][solution[flight_id]]

        cost += trip[2]
        cost += homecoming[2]

        if last_arrival < get_minutes(trip[1]):
            last_arrival = get_minutes(trip[1])

        if first_departure > get_minutes(homecoming[0]):
            first_departure = get_minutes(homecoming[0])

    flight_id = -1

    for i in range(len(solution) // 2):
        origin = friends[i][1]

        flight_id += 1
        trip = flights[(origin, destination)][solution[flight_id]]

        flight_id += 1
        homecoming = flights[(destination, origin)][solution[flight_id]]

        wait_time += last_arrival - get_minutes(trip[1])
        wait_time += get_minutes(homecoming[0]) - first_departure

    if last_arrival > first_departure:
        cost += 50  # penalty for delays

    return cost + wait_time  # fitness score
