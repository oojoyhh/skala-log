const getLocalDate = (timestamp, timezone) => {
  const date = new Date((timestamp + timezone) * 1000)
  return {
    key: date.toISOString().slice(0, 10),
    day: date.getUTCDate(),
    weekday: ['일', '월', '화', '수', '목', '금', '토'][date.getUTCDay()],
    hour: date.getUTCHours(),
  }
}

export const createForecastView = ({ items, timezone }) => {
  const days = new Map()
  const today = getLocalDate(Math.floor(Date.now() / 1000), timezone).key

  items.forEach((item) => {
    const local = getLocalDate(item.timestamp, timezone)
    const day = days.get(local.key) ?? { ...local, items: [] }
    day.items.push(item)
    days.set(local.key, day)
  })

  const daily = [...days.values()].slice(0, 5).map((day) => {
    const center = day.items.reduce((closest, item) => {
      const hour = getLocalDate(item.timestamp, timezone).hour
      const closestHour = getLocalDate(closest.timestamp, timezone).hour
      return Math.abs(hour - 12) < Math.abs(closestHour - 12) ? item : closest
    })

    return {
      date: day.key === today ? '오늘' : `${day.day}일 (${day.weekday})`,
      minTemp: Math.min(...day.items.map((item) => item.tempMin)),
      maxTemp: Math.max(...day.items.map((item) => item.tempMax)),
      status: center.status,
      icon: center.icon,
    }
  })

  const hourly = items.slice(0, 8).map((item) => {
    const { hour } = getLocalDate(item.timestamp, timezone)
    return { ...item, time: `${String(hour).padStart(2, '0')}:00` }
  })

  return { hourly, daily }
}
