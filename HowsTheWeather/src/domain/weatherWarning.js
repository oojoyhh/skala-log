// 기상청 wrn_now_data.php는 WRN/LVL/CMD를 코드가 아닌 한글 텍스트("폭염", "중대경보", "변경" 등)로 내려줌
const excludedCommands = new Set(['해제', '대치해제', '변경해제'])

const formatDate = (value) =>
  value?.length === 12
    ? `${value.slice(0, 4)}.${value.slice(4, 6)}.${value.slice(6, 8)} ${value.slice(8, 10)}:${value.slice(10)}`
    : value

const normalizeWarning = (warning) => ({
  regionId: warning.REG_ID,
  upperRegion: warning.REG_UP_KO,
  region: warning.REG_KO,
  type: warning.WRN,
  level: warning.LVL || '특보',
  command: warning.CMD || '',
  issuedAt: formatDate(warning.TM_FC),
  effectiveAt: formatDate(warning.TM_EF),
})

export const getActiveWarnings = (warnings) => {
  const seen = new Set()

  return warnings
    .filter((warning) => warning.WRN && !excludedCommands.has(warning.CMD))
    .filter((warning) => {
      const key = `${warning.REG_ID}-${warning.WRN}-${warning.LVL}-${warning.CMD}-${warning.TM_EF}`
      if (seen.has(key)) return false
      seen.add(key)
      return true
    })
    .map(normalizeWarning)
}

const actionGuides = [
  {
    match: '폭염',
    tips: [
      '한낮(정오~오후 5시) 야외활동과 격한 운동을 피하세요.',
      '갈증을 느끼지 않아도 물을 자주 마시세요.',
      '어지럼증·두통이 있으면 즉시 시원한 곳으로 이동하세요.',
    ],
  },
  {
    match: '열대야',
    tips: ['자기 전 미지근한 물로 샤워해 체온을 낮추세요.', '실내 온도를 26~28℃로 유지하고 자주 환기하세요.'],
  },
  {
    match: '한파',
    tips: [
      '내복·장갑·목도리로 체온을 유지하세요.',
      '노약자는 이른 아침·늦은 밤 외출을 피하세요.',
      '수도관과 계량기 동파에 대비하세요.',
    ],
  },
  {
    match: '호우',
    tips: ['하천변, 지하차도, 저지대 이동을 피하세요.', '외출을 자제하고 배수구 상태를 미리 확인하세요.'],
  },
  {
    match: '대설',
    tips: ['보행 시 미끄럼에 주의하고 여유 있게 이동하세요.', '차량 운행 전 월동장비를 미리 갖추세요.'],
  },
  {
    match: '강풍',
    tips: ['간판, 공사장 등 낙하물 위험 지역을 피하세요.', '창문·베란다의 물건을 단단히 고정하세요.'],
  },
  {
    match: '풍랑',
    tips: ['해안가 접근과 어선 운항을 자제하세요.'],
  },
  {
    match: '건조',
    tips: ['화기 사용에 주의하고 산불 위험 지역 방문을 피하세요.'],
  },
  {
    match: '황사',
    tips: ['외출 시 마스크를 착용하고 창문을 닫아두세요.', '렌즈 대신 안경 착용을 권장합니다.'],
  },
  {
    match: '태풍',
    tips: ['외출을 자제하고 창문 파손에 대비해 테이핑하세요.', '해안가, 저지대 접근을 피하세요.'],
  },
  {
    match: '안개',
    tips: ['운전 시 감속하고 안개등을 사용하세요.'],
  },
]

const defaultGuideTips = ['공식 재난문자와 지자체 안내를 확인하세요.', '무리한 외출을 자제하고 주변 안전에 유의하세요.']

// 특보 종류(문자열)에 맞는 행동 요령을 찾음. 없으면 일반 안내로 대신함
export const getActionGuide = (type) => {
  const matched = actionGuides.find((guide) => type.includes(guide.match))
  return matched?.tips ?? defaultGuideTips
}

export const getCityWarnings = (warnings, regions, cityName) => {
  const metropolitanRegionNames = {
    서울: '서울특별시',
    부산: '부산광역시',
    대구: '대구광역시',
    대전: '대전광역시',
    광주: '광주광역시',
    제주: '제주특별자치도',
  }
  const metropolitanRegionName = metropolitanRegionNames[cityName]
  const activeWarnings = getActiveWarnings(warnings)

  // 이름이 같은 다른 시·군(예: 경기도 광주시)이 섞이지 않도록 광역 행정구역을 우선함
  if (metropolitanRegionName) {
    return activeWarnings.filter(
      (warning) =>
        warning.upperRegion === metropolitanRegionName || warning.region === metropolitanRegionName,
    )
  }

  const regionCodes = new Set(
    regions
      .filter((region) => `${region.REG_KO} ${region.REG_NAME}`.includes(cityName))
      .map((region) => region.REG_ID),
  )

  return activeWarnings.filter(
    (warning) =>
      regionCodes.has(warning.regionId) ||
      warning.region.includes(cityName) ||
      warning.upperRegion?.includes(cityName),
  )
}
