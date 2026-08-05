const pm10Levels = [
  { max: 30, label: '좋음', type: 'success' },
  { max: 80, label: '보통', type: 'primary' },
  { max: 150, label: '나쁨', type: 'warning' },
  { max: Infinity, label: '매우나쁨', type: 'danger' },
]

const pm25Levels = [
  { max: 15, label: '좋음', type: 'success' },
  { max: 35, label: '보통', type: 'primary' },
  { max: 75, label: '나쁨', type: 'warning' },
  { max: Infinity, label: '매우나쁨', type: 'danger' },
]

export const getPm10Level = (value) => pm10Levels.find((level) => value <= level.max)

export const getPm25Level = (value) => pm25Levels.find((level) => value <= level.max)
