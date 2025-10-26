import pytest
from bot.bot import start  # Adjust the import based on your actual bot structure

@pytest.mark.asyncio
async def test_start_command(mocker):
    mock_update = mocker.Mock()
    mock_context = mocker.Mock()
    mock_update.message.reply_text = mocker.AsyncMock()

    await start(mock_update, mock_context)

    mock_update.message.reply_text.assert_called_once_with("Hallo! Dies ist ein Beispiel-Bot (Webhook-Modus).")