

import pytest

from unittest.mock import AsyncMock, _Call
from bot.routers.base import start, START_MESSAGE

def parse_answer(answer: AsyncMock) -> list[dict]:
    calls: list[_Call] = answer._mock_mock_calls

    answers = []

    for call in calls:
        data: dict = call.kwargs
        data.update(text = call.args[0])

        answers.append(data)
    
    return answers

@pytest.mark.asyncio
async def test_start_handler():
    text_mock = "/start"
    message_mock = AsyncMock(text=text_mock)
    await start(message=message_mock)

    answers = parse_answer(message_mock.answer)
    assert any(a.get('text') == START_MESSAGE for a in answers)
