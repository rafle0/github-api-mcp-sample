# GitHub API MCP Sample

Python으로 작성한 예시 HTTP API를 MCP(Model Context Protocol) 서버에서도 호출할 수 있게 만든 샘플입니다.

## 구성

- `src/sample_api/main.py`: FastAPI 예시 API
- `src/sample_api/store.py`: 메모리 기반 데이터 저장소
- `src/sample_mcp/server.py`: MCP 도구 서버
- `tests/test_api.py`: API 동작 테스트

## 설치

```powershell
uv sync --dev
```

## API 실행

```powershell
uv run uvicorn sample_api.main:app --reload
```

API가 실행되면 다음 주소를 열 수 있습니다.

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs`

## MCP 서버 실행

```powershell
uv run python -m sample_mcp.server
```

MCP 서버는 FastAPI 앱을 HTTP로 호출합니다. 먼저 API 서버를 실행하거나,
`SAMPLE_API_BASE_URL` 환경변수에 API 서버 URL을 설정하세요.

MCP 서버는 lazy singleton 방식의 `httpx.AsyncClient`를 재사용하며,
connection pool, keep-alive, 명시적인 timeout 설정을 사용합니다.

MCP 클라이언트 설정 예시:

```json
{
  "mcpServers": {
    "sample-api": {
      "command": "uv",
      "args": ["run", "python", "-m", "sample_mcp.server"],
      "cwd": "/path/to/github-api-mcp-sample"
    }
  }
}
```

## 제공되는 MCP 도구

- `list_items`: 샘플 아이템 목록 조회
- `get_item`: 특정 아이템 조회
- `create_item`: 새 아이템 생성

## 테스트

```powershell
uv run pytest
```
