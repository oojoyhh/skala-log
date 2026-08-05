import axios from 'axios'

export const cities = [
  { id: 'city_01', name: '서울', lat: 37.5665, lon: 126.978 },
  { id: 'city_04', name: '속초', lat: 38.207, lon: 128.5918 },
  { id: 'city_05', name: '청주', lat: 36.6424, lon: 127.489 },
  { id: 'city_06', name: '대전', lat: 36.3504, lon: 127.3845 },
  { id: 'city_07', name: '전주', lat: 35.8242, lon: 127.148 },
  { id: 'city_08', name: '광주', lat: 35.1595, lon: 126.8526 },
  { id: 'city_09', name: '대구', lat: 35.8714, lon: 128.6014 },
  { id: 'city_03', name: '부산', lat: 35.1796, lon: 129.0756 },
  { id: 'city_10', name: '제주', lat: 33.4996, lon: 126.5312 },
]

export const fetchCityWeather = async (city) => {
  const apiKey = import.meta.env.VITE_OPENWEATHER_API_KEY

  if (!apiKey) throw new Error('.env.local 파일에 OpenWeather API 키를 입력하세요.')

  const { data } = await axios.get('https://api.openweathermap.org/data/2.5/weather', {
    params: { lat: city.lat, lon: city.lon, appid: apiKey, units: 'metric', lang: 'kr' },
  })

  return {
    ...city,
    temp: Math.round(data.main.temp),
    feelsLike: Math.round(data.main.feels_like),
    status: data.weather[0].description,
    icon: data.weather[0].icon,
    humidity: data.main.humidity,
    pressure: data.main.pressure,
    wind: data.wind.speed,
    sunrise: data.sys.sunrise,
    sunset: data.sys.sunset,
  }
}

export const fetchCityAirQuality = async (city) => {
  const apiKey = import.meta.env.VITE_OPENWEATHER_API_KEY

  if (!apiKey) throw new Error('.env.local 파일에 OpenWeather API 키를 입력하세요.')

  const { data } = await axios.get('https://api.openweathermap.org/data/2.5/air_pollution', {
    params: { lat: city.lat, lon: city.lon, appid: apiKey },
  })
  const components = data.list[0].components

  return {
    pm10: Math.round(components.pm10),
    pm25: Math.round(components.pm2_5),
  }
}

export const fetchCityForecast = async (city) => {
  const apiKey = import.meta.env.VITE_OPENWEATHER_API_KEY

  if (!apiKey) throw new Error('.env.local 파일에 OpenWeather API 키를 입력하세요.')

  const { data } = await axios.get('https://api.openweathermap.org/data/2.5/forecast', {
    params: { lat: city.lat, lon: city.lon, appid: apiKey, units: 'metric', lang: 'kr' },
  })

  return {
    timezone: data.city.timezone,
    items: data.list.map((item) => ({
      timestamp: item.dt,
      temp: Math.round(item.main.temp),
      tempMin: Math.round(item.main.temp_min),
      tempMax: Math.round(item.main.temp_max),
      status: item.weather[0].description,
      icon: item.weather[0].icon,
      rainChance: Math.round(item.pop * 100),
    })),
  }
}
