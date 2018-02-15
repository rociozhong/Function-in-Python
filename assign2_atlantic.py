# Group members: Wei Zhong(wzhong8); Nan Yang(nanyang4)
# Brief summary: Each of us finished the whole assignment independently, and we combine our code.


from datetime import datetime
from pygeodesy import ellipsoidalVincenty as ev
import math


def preprocess_Lon(longitude: str) -> str:
    """

    checks Longitude entry and convert invalid entry of Longitude to valid entry that is within range (-180, 180)
    :param longitude: original Longitude entry (string)
    :return: valid Longitude value (string)
    """

    if -180 < float(longitude[:-1]) and float(longitude[:-1]) < 180:
        longitude = longitude
    while float(longitude[:-1]) < -180:
        longitude = str(round(float(longitude[:-1]) + 360, 1)) + 'W'
    while float(longitude[:-1]) > 180:
        longitude = str(round(float(longitude[:-1]) - 360, 1)) + 'W'

    return longitude


cycloneList = []
with open("atlantic.csv") as f:
    while True:
        line = f.readline()
        if not line:
            break
        line = list(map(str.strip, line.strip().split(",")))  # map: use function on lists; strip: delete whitespace; and split with comma

        if len(line) == 4:
            cyclone = {}
            cyclone["id"] = line[0]
            cyclone["name"] = line[1]
            cyclone["numberOfRecords"] = int(line[2])
            cyclone["time"] = []
            cyclone["landfall"] = 0
            cyclone["maxSpeed"] = [-math.inf, -1]
            cyclone["isHurricane"] = False
            cyclone["coordinate"] = []
            cyclone["34kt_radii"] = []
            cyclone["50kt_radii"] = []
            cyclone["64kt_radii"] = []

            for i in range(cyclone["numberOfRecords"]):
                line = list(map(str.strip, f.readline().strip().split(",")))
                cyclone["coordinate"].append((line[4], preprocess_Lon(line[5])))
                cyclone["time"].append((line[0], line[1]))
                cyclone["34kt_radii"].append(line[8:12])
                cyclone["50kt_radii"].append(line[12:16])
                cyclone["64kt_radii"].append(line[16:20])
                if line[2] == "L":
                    cyclone["landfall"] += 1
                if line[3] == "HU":
                    cyclone["isHurricane"] = True
                if cyclone["maxSpeed"][0] < int(line[6]):
                    cyclone["maxSpeed"][0] = int(line[6])
                    cyclone["maxSpeed"][1] = i
            cycloneList.append(dict(cyclone))  # since cyclone is mutable, dict() does a copy of cyclone

for cyclone in cycloneList:
    print("Name: {0}".format(cyclone["name"]))
    print("Date range: {0} -- {1}".format(cyclone["time"][0][0], cyclone["time"][-1][0]))
    maxSpeed, timeIndex = cyclone["maxSpeed"]
    print("Maximum speed: {0} knots (Date: {1}, time: {2})".format(maxSpeed, cyclone["time"][timeIndex][0],
                                                                   cyclone["time"][timeIndex][1]))
    print("Number of landfalls: {0}".format(cyclone["landfall"]))
    print("*********************************************************")







def get_storm_occurence(storm: list) -> dict:
    """
    make a dictionary: key- year, value -- occurrence of storms

    :param storm: list of dictionaries, and each dictionary consists of a specific storm
    :return: storm occurrence per year as a dictionary, whose keys are 'year', and values, 'occurrence of storm'
    """
    temp_1 = {}
    for each_cyclone in storm:   # loop each dictionary in the list
        year = each_cyclone["id"][-4::]   # extract the year for each storm in the dictionary
        if temp_1.get(year):  # dict.get(x), if x not in the keys of dict, then return None (first time appearance)
            temp_1[year] += 1
        else:
            temp_1[year] = 1

    return temp_1

storm_frequency = get_storm_occurence(cycloneList)

for key in storm_frequency.keys():
    print("Year: {0}".format(key))
    print("Number of storms: {0}".format(storm_frequency[key]))

######################






def get_hurricane_occurrence(storm: list) -> dict:
    """
     get number of hurricanes per year

    :param storm: list of dictionaries, and each dictionary consists of a specific storm
    :return: hurricane occurrence as a dictionary which has keys of 'year', and values of 'occurrence'
    """

    temp_2 = {}
    for each_cyclone in storm:
        year = each_cyclone["id"][-4::]
        if each_cyclone["isHurricane"]:
          if temp_2.get(year):    # dict.get(x), if x not in the keys of dict, then return None (first time appearance)
            temp_2[year] += 1
          else:
            temp_2[year] = 1

    return temp_2

hurricane_frequency = get_hurricane_occurrence(cycloneList)

for key in hurricane_frequency.keys():
    print("Year: {0}".format(key))
    print("Number of hurricanes: {0}".format(hurricane_frequency[key]))


###### phase B ######
# for each storm, use an accumulator to compute and report TOTAL distance each storm was tracked


def get_storm_distance(storm_coordinate: list) -> float:
    """
    get each storm total moving distance

    :param storm_coordinate: list of tuples, each tuple contains a latitude and longitude
    :return: each storm total distance as a float
    """

    total = 0
    if len(storm_coordinate) <= 1:
        return 0.0
    for i in range(1, len(storm_coordinate)):
        a = ev.LatLon(storm_coordinate[i][0], storm_coordinate[i][1])
        b = ev.LatLon(storm_coordinate[i - 1][0], storm_coordinate[i - 1][1])
        if a == b:
            d = 0.0
        else:
            d = a.distanceTo(b)
        total += d
    return total / 1852 # Divide to convert meters into nautical miles


for cyclone in cycloneList:
    print("Name of storm: {0}".format(cyclone["id"]))
    print("Total distance: {0: .3f}".format(get_storm_distance(cyclone["coordinate"])))


################
def get_storm_maxspeed(eachstorm: dict) -> float:
    """
    extract the maximum speed for each storm moving track

    :param eachstorm: a dictionary contains keys (coordinate, time, id and so on)
    :return: each storm max speed as a float
    """

    max_speed = - math.inf
    storm_coordinate = eachstorm["coordinate"]   # list
    storm_time = eachstorm["time"]   # list

    if len(storm_coordinate) <= 1:
        return 0.0
    for i in range(1, len(storm_coordinate)):
        a = ev.LatLon(storm_coordinate[i - 1][0], storm_coordinate[i - 1][1])
        b = ev.LatLon(storm_coordinate[i][0], storm_coordinate[i][1])
        if a == b:
            d = 0.0
        else:
            d = a.distanceTo(b)

        ta = datetime.strptime(''.join(storm_time[i - 1]), "%Y%m%d%H%M")
        tb = datetime.strptime(''.join(storm_time[i]), "%Y%m%d%H%M")
        t = (tb - ta).total_seconds() / 3600
        speed = (d / 1852) / t
        max_speed = max(speed, max_speed)

    return max_speed


for cyclone in cycloneList:
    print("Name of storm: {0}".format(cyclone["id"]))
    print("Maximum propagation speeds: {0: .3f}".format(get_storm_maxspeed(cyclone)))
    print("xxxxxxxxxxxxxxxxxxx")


def get_storm_avespeed(eachstorm: dict) -> float:
    """
    calculate each storm average moving speed

    :param eachstorm: a dictionary contains keys (coordinate, time, id and so on)
    :return: each storm average speed as float
    """

    total = 0
    storm_coordinate = eachstorm["coordinate"]   # list
    storm_time = eachstorm["time"]   # list

    start = datetime.strptime(''.join(storm_time[0]), "%Y%m%d%H%M")
    stop = datetime.strptime(''.join(storm_time[-1]), "%Y%m%d%H%M")
    total_time = (stop - start).total_seconds() / 3600

    if len(storm_coordinate) <= 1:
        return 0.0
    for i in range(1, len(storm_coordinate)):
        a = ev.LatLon(storm_coordinate[i][0], storm_coordinate[i][1])
        b = ev.LatLon(storm_coordinate[i - 1][0], storm_coordinate[i - 1][1])
        if a == b:
            d = 0.0
        else:
            d = a.distanceTo(b)
        total += d

    return (total / 1852) / total_time


for cyclone in cycloneList:
    print("Name of storm: {0}".format(cyclone["id"]))
    print("Average propagation speeds: {0: .3f}".format(get_storm_avespeed(cyclone)))
    print("xxxxxxxxxxxxxxxxxxx")



########### hypothesis #############

def get_hypo_quadrant(coordinate_1, coordinate_2: tuple) -> int:
    """
    calculate hypothesized quadrant for a moving direction of a storm

    :param coordinate_1: for each storm, each track coordinate as a tuple
    :param coordinate_2: for each storm, each track coordinate as a tuple
    :return: int: quadrant index
    """

    a = ev.LatLon(coordinate_1[0], coordinate_1[1])
    b = ev.LatLon(coordinate_2[0], coordinate_2[1])
    if a == b:
        bearing = 90
    else:
        bearing = (int(a.bearingTo(b)) + 90) % 360
    return bearing // 90


valid = 0
cnt = 0
for cyclone in cycloneList:
    if len(cyclone["coordinate"]) > 1:
        for i in range(1, len(cyclone["coordinate"])):
            hypo_quadrant = get_hypo_quadrant(cyclone["coordinate"][i - 1], cyclone["coordinate"][i])
            m = max(map(int, cyclone["64kt_radii"][i]))
            if m > 0:
                if hypo_quadrant in [idx for idx, j in enumerate(cyclone["64kt_radii"][i]) if int(j) == m]:
                    valid += 1
                cnt += 1

print("The accuracy of the hypothesis is: {0: .1f}%".format((valid / cnt) * 100))




