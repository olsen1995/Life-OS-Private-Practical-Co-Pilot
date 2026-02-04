import json
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def http_get(url: str) -> dict:
    req = Request(url=url, method="GET")
    with urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_delete(url: str) -> dict:
    req = Request(url=url, method="DELETE")
    with urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_post_form(url: str, form: dict) -> dict:
    data = urlencode(form).encode("utf-8")
    req = Request(url=url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = Request(url=url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    with urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def assert_keys(obj: dict, required_keys: list[str], label: str) -> None:
    missing = [k for k in required_keys if k not in obj]
    if missing:
        raise AssertionError(f"{label}: missing keys {missing}. Got: {obj}")


def main() -> int:
    base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    user_id = "smoke_user"
    message = "hello from smoke test"
    memory_payload = {"example_key": "example_value"}

    print(f"Base URL: {base}")

    try:
        # 1) GET /ask
        ask_get_url = f"{base}/ask?{urlencode({'message': message, 'user_id': user_id})}"
        r1 = http_get(ask_get_url)
        assert_keys(r1, ["summary", "user_id", "memory"], "GET /ask")
        if r1["user_id"] != user_id:
            raise AssertionError(f"GET /ask: user_id mismatch. Got {r1['user_id']} expected {user_id}")
        print("OK: GET /ask")

        # 2) POST /ask (form)
        r2 = http_post_form(f"{base}/ask", {"message": message, "user_id": user_id})
        assert_keys(r2, ["summary", "user_id", "memory"], "POST /ask")
        if r2["user_id"] != user_id:
            raise AssertionError(f"POST /ask: user_id mismatch. Got {r2['user_id']} expected {user_id}")
        print("OK: POST /ask")

        # 3) POST /memory (json)
        r3 = http_post_json(f"{base}/memory", {"user_id": user_id, "memory": memory_payload})
        assert_keys(r3, ["ok", "written"], "POST /memory")
        if r3["ok"] is not True:
            raise AssertionError(f"POST /memory: ok not True. Got: {r3}")
        print("OK: POST /memory")

        # 4) GET /memory
        mem_get_url = f"{base}/memory?{urlencode({'user_id': user_id})}"
        r4 = http_get(mem_get_url)
        if not isinstance(r4, dict):
            raise AssertionError(f"GET /memory: expected dict. Got: {r4}")
        if r4.get("example_key") != "example_value":
            raise AssertionError(f"GET /memory: memory mismatch. Got: {r4}")
        print("OK: GET /memory")

        # 5) DELETE /memory
        mem_del_url = f"{base}/memory?{urlencode({'user_id': user_id})}"
        r5 = http_delete(mem_del_url)
        assert_keys(r5, ["ok", "deleted"], "DELETE /memory")
        if r5["ok"] is not True:
            raise AssertionError(f"DELETE /memory: ok not True. Got: {r5}")
        print("OK: DELETE /memory")

        # 6) GET /memory after delete
        r6 = http_get(mem_get_url)
        if r6.get("example_key") is not None:
            raise AssertionError(f"GET /memory after delete: expected cleared memory. Got: {r6}")
        print("OK: GET /memory after delete")

        print("SMOKE TEST PASSED.")
        return 0

    except (HTTPError, URLError) as e:
        print(f"HTTP ERROR: {e}")
        return 2
    except AssertionError as e:
        print(f"ASSERTION FAILED: {e}")
        return 3
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
