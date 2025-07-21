# Slack `/치트` 명령어 봇

Flask로 만든 Slack Slash Command 봇입니다.  
Google Spreadsheet의 데이터를 검색해 응답합니다.

---

## 🔧 사용 기술

- Flask (Slack Slash Command 처리)
- gspread + Google API (Google Sheets 연동)
- Render (자동 배포)

---

## 📁 구조




---

## 🌐 환경 변수

| 이름 | 설명 |
|------|------|
| `SERVICE_ACCOUNT_BASE64` | `service_account.json`을 base64로 인코딩한 값 |

변환 예시 (PowerShell):

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("service_account.json")) > output.txt






