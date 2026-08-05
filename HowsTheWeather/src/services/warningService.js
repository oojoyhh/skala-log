import { fetchCurrentWarnings, fetchWarningRegions } from '@/api/kmaWarningApi'
import { getCityWarnings } from '@/domain/weatherWarning'

const fetchWarningData = async () => {
  const [regions, currentWarnings] = await Promise.all([
    fetchWarningRegions(),
    fetchCurrentWarnings(),
  ])
  return { regions, currentWarnings }
}

export const fetchCityWarnings = async (cityName) => {
  const { regions, currentWarnings } = await fetchWarningData()
  return getCityWarnings(currentWarnings, regions, cityName)
}

export const fetchAllCityWarnings = async (cities) => {
  const { regions, currentWarnings } = await fetchWarningData()
  return cities.map((city) => ({
    city,
    warnings: getCityWarnings(currentWarnings, regions, city.name),
  }))
}
