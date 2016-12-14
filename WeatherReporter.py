import datetime
import pyowm


class WeatherReporter:
    def __init__(self, apiKey):
        self.api = pyowm.OWM(API_key=apiKey, language="ru")

    def GenerateWeatherReport(self, observation):
        location = observation.get_location()
        weather = observation.get_weather()

        forecastTemperature = self.api.daily_forecast(location.get_name(), limit=1).get_forecast().get_weathers()[
            0].get_temperature(
            "celsius")

        data = dict(
            city=location.get_name(),
            cityID=location.get_ID(),
            time="{0:%H:%M}".format(datetime.datetime.now()),
            status=weather.get_detailed_status(),
            cloudiness=weather.get_clouds(),
            pressure=round(weather.get_pressure()["press"] * 0.75006375541921),
            currentTemp=round(weather.get_temperature("celsius")["temp"]),
            windSpeed=round(weather.get_wind()["speed"]),
            windDirection=self.GetWindDirectionName(weather.get_wind()["deg"]),
            nightTemp=round(forecastTemperature["night"]),
            dayTemp=round(forecastTemperature["day"])
        )

        return '''
Погода в городе {city} (#{cityID}) на сегодня в {time}:
{status}, облачность составляет {cloudiness}%, давление — {pressure} мм рт. ст., температура — {currentTemp}°C.
Ветер {windDirection}, {windSpeed} м/с.
Температура воздуха ночью — {nightTemp}°C, днём — {dayTemp}°C.'''.format(**data)

    def GetWeatherReportByID(self, ID):
        try:
            observation = self.api.weather_at_id(ID)

            return True, self.GenerateWeatherReport(observation)
        except:
            return False, "Не удалось получить прогноз погоды для места с таким ID :-(\nВы точно ввели правильный ID?"

    def GetWeatherReportByPlaceName(self, placeName):
        observations = self.api.weather_at_places(placeName, 'like', 6)

        if len(observations) == 0:
            return False, "По вашему запросу ничего не нашлось :-("
        elif len(observations) == 1:
            return True, self.GenerateWeatherReport(observations[0])
        else:
            output = "По вашему запросу найдено несколько мест. Для выбора конкретного места укажите его ID, " \
                     "используя команду <ID>.\n"

            i = 0

            while i < len(observations):
                output += \
                    "\n" + str(observations[i].get_location().get_ID()) + ": " + \
                    observations[i].get_location().get_name()
                i += 1

            return True, output

    def GetWindDirectionName(self, degrees):
        if degrees <= 22.5:
            return "северный"
        elif degrees <= 67.5:
            return "северо-восточный"
        elif degrees <= 112.5:
            return "восточный"
        elif degrees <= 157.5:
            return "юго-восточный"
        elif degrees <= 202.5:
            return "южный"
        elif degrees <= 247.5:
            return "юго-западный"
        elif degrees <= 292.5:
            return "западный"
        elif degrees <= 337.5:
            return "северо-западный"
        else:
            return "северный"
