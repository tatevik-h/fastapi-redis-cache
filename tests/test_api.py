import pytest

@pytest.mark.asincio
async def test_create_and_get_payload(client):
    payload = {
        "list_1": ["foo", "bar"],
        "list_2": ["baz", "qux"]
    }

    response = await client.post("/payload/", json=payload)
    assert  response.status_code == 200
    data = response.json()
    assert "id" in data

    pid = data["id"]

    response = await client.get(f"/payload/{pid}")
    assert response.status_code == 200
    out = response.json()
    assert  "output" in out
    assert "FOO" in out["output"]
