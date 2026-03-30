import pytest
from app.nokia.mock import MockNokiaClient


@pytest.mark.anyio
async def test_create_qod_session_returns_session_id():
    client = MockNokiaClient()
    session_id = await client.create_qod_session("device-123", "QOS_L", duration=None)
    assert session_id is not None
    assert session_id.startswith("fake-session-")


@pytest.mark.anyio
async def test_delete_qod_session_returns_true():
    client = MockNokiaClient()
    session_id = await client.create_qod_session("device-123", "QOS_L", duration=None)
    result = await client.delete_qod_session(session_id)
    assert result is True


@pytest.mark.anyio
async def test_create_qod_session_logs_call():
    client = MockNokiaClient()
    await client.create_qod_session("device-456", "QOS_M", duration=900)
    assert len(client.call_log) == 1
    assert client.call_log[0]["action"] == "create_qod_session"
    assert client.call_log[0]["device_id"] == "device-456"
    assert client.call_log[0]["profile"] == "QOS_M"
