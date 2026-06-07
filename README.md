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

MCP server calls the FastAPI app over HTTP. Start the API server first, or set
`SAMPLE_API_BASE_URL` to the API server URL.

The MCP server reuses a lazy `httpx.AsyncClient` with connection pooling,
keep-alive, and explicit timeout settings.

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

## Code Quality

```powershell
uv run ruff check .
uv run ruff format --check .
```
