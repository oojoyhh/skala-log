export const temperatureLevels = [
  { max: 0, label: '매우 추움', range: '0℃ 미만', className: 'freezing' },
  { max: 10, label: '추움', range: '0~9℃', className: 'cold' },
  { max: 20, label: '선선함', range: '10~19℃', className: 'cool' },
  { max: 28, label: '따뜻함', range: '20~27℃', className: 'warm' },
  { max: Infinity, label: '더움', range: '28℃ 이상', className: 'hot' },
]

export const convertTemperature = (temp, unit) =>
  unit === 'fahrenheit' ? Math.round((temp * 9) / 5 + 32) : temp

export const getTemperatureLevel = (temp) => temperatureLevels.find((level) => temp < level.max)

export const formatClockTime = (unixSeconds) =>
  new Date(unixSeconds * 1000).toLocaleTimeString('ko-KR', {
    hour: '2-digit',
    minute: '2-digit',
  })
