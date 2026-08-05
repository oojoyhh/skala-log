import { cities, fetchCityAirQuality, fetchCityForecast, fetchCityWeather } from '@/api/weatherApi'
import { createForecastView } from '@/domain/weatherForecast'

export const fetchCityForecastView = async (city) =>
  createForecastView(await fetchCityForecast(city))

export const fetchCityWeatherSummary = async (city) => {
  const [weather, forecast, airQuality] = await Promise.all([
    fetchCityWeather(city),
    fetchCityForecastView(city),
    fetchCityAirQuality(city),
  ])
  const today = forecast.daily[0]

  return {
    ...weather,
    ...airQuality,
    // 현재 기온이 예보 min/max 범위 밖일 수 있어서 같이 비교해서 보정
    minTemp: Math.min(weather.temp, today.minTemp),
    maxTemp: Math.max(weather.temp, today.maxTemp),
    hourly: forecast.hourly,
    daily: forecast.daily,
  }
}

export const fetchWeatherList = () => Promise.all(cities.map(fetchCityWeatherSummary))
