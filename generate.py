import datetime, forecastio, statistics
import GenerativePieceClass as gp

api_key = "4322ff0f22d1eb90e2f4fa5ce615296c"
lat = 30.443054
lon = -84.291370
yesterday = datetime.datetime(2017, 10, 23)
tomorrow = datetime.datetime(2017, 10, 25)

def makeContour(points):
    log = []
    # create initial direction. Do nothing if same
    if points[1] > points[0]:
        log.append((0,'+'))
    elif points[1] < points[0]:
        log.append((0,'-'))

    for i in range(len(points)):
        if i == 0 or i == len(points)-1:
            pass
        else:
            if (log[-1][1] == '+' or len(log) == 0) and points[i+1] < points[i]:
                log.append((i,'-'))

            if (log[-1][1] == '-' or len(log) == 0) and points[i+1] > points[i]:
                log.append((i,'+'))

    return log

#current_time = datetime.datetime.now()

forecastToday = forecastio.load_forecast(api_key, lat, lon)
forecastYesterday = forecastio.load_forecast(api_key, lat, lon, time=yesterday)
forecastTomorrow = forecastio.load_forecast(api_key, lat, lon, time=tomorrow)

todayHour = forecastToday.hourly()
yesterdayHour = forecastYesterday.hourly()
tomorrowHour = forecastTomorrow.hourly()

raw = [d.temperature for d in todayHour.data]
piece = gp.GenerativePiece(todayHour.summary, int(statistics.mean(raw)))

soprano = [round(x) for x in raw]
bass = [round(x.temperature)-7 for x in yesterdayHour.data]
alto = [round(x.temperature) for x in tomorrowHour.data]
# retrograde = raw[::-1]
# inversion = [(-round(x) + 127) for x in raw]
# print(statistics.pvariance([round(v) for v in raw]))

piece.setSoprano(soprano, makeContour(soprano))
piece.setBass(bass)
piece.setAlto(alto)
piece.createSong()
