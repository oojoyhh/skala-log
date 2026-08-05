import axios from 'axios'

const BASE_URL = '/kma-api/api/typ01/url'

const getErrorMessage = (response) => {
  if (typeof response !== 'string') return response?.result?.message

  try {
    return JSON.parse(response).result?.message
  } catch {
    return undefined
  }
}

// 기상청 API는 파일마다 구분자가 다름: wrn_reg.php는 공백(고정폭 정렬용 패딩 포함),
// wrn_now_data.php는 쉼표로 필드를 구분함. 두 경우 모두 fields 순서 = 실제 컬럼 순서
const parseTable = (text, fields, { delimiter = 'whitespace' } = {}) => {
  const lines = text.split(/\r?\n/)

  return lines
    .filter((line) => line.trim() && !line.trimStart().startsWith('#'))
    .map((line) => {
      const values =
        delimiter === 'comma'
          ? line.split(',').map((value) => value.trim())
          : line.trim().split(/\s+/)

      return Object.fromEntries(fields.map((name, index) => [name, values[index] ?? '']))
    })
    .filter((row) => row[fields[0]])
}

const requestText = async (path, params) => {
  const authKey = import.meta.env.VITE_KMA_API_KEY
  if (!authKey) throw new Error('.env.local 파일에 기상청 API 키를 입력하세요.')

  try {
    const { data } = await axios.get(`${BASE_URL}/${path}`, {
      params: { ...params, authKey },
      responseType: 'text',
    })
    return data
  } catch (error) {
    throw new Error(
      getErrorMessage(error.response?.data) ??
        '기상청 특보를 불러오지 못했습니다. API 활용신청과 인증키를 확인하세요.',
      { cause: error },
    )
  }
}

export const fetchWarningRegions = async () => {
  const text = await requestText('wrn_reg.php', { tmfc: 0 })
  return parseTable(text, ['REG_ID', 'TM_ST', 'TM_ED', 'REG_SP', 'REG_UP', 'REG_KO', 'REG_NAME'])
}

export const fetchCurrentWarnings = async () => {
  const text = await requestText('wrn_now_data.php', { fe: 'f', tm: '', disp: 0, help: 1 })
  return parseTable(
    text,
    ['REG_UP', 'REG_UP_KO', 'REG_ID', 'REG_KO', 'TM_FC', 'TM_EF', 'WRN', 'LVL', 'CMD'],
    { delimiter: 'comma' },
  )
}
