# Telegram Setup Guide

Use this guide to enable Telegram as a delivery channel for your daily briefing.

## 1. Create a Telegram bot

1. Open Telegram and search for **@BotFather**.
2. Start a chat and send `/newbot`.
3. Follow the prompts to name your bot (e.g., "Chief of Staff") and set a username (must end in `bot`, e.g., `my_chief_bot`).
4. BotFather will reply with a message like:
   ```
   Use this token to access the HTTP API:
   123456789:ABCdefGHIjklMNOpqrSTUvwxyz
   ```
5. Copy that token and add it to `.env`:
   ```env
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxyz
   ```

## 2. Get your chat ID

You need the ID of the chat where the bot will send briefings. The simplest way is to send a message to your bot first, then query the Telegram API.

1. Open your bot in Telegram and send any message (e.g., "hello").
2. In a terminal, run:
   ```bash
   curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
3. Look for the `chat` object in the JSON response:
   ```json
   {
     "message": {
       "chat": {
         "id": 123456789,
         "type": "private"
       }
     }
   }
   ```
4. Copy the `id` value and add it to `.env`:
   ```env
   TELEGRAM_CHAT_ID=123456789
   ```

> For a group chat, add the bot to the group first, then use `getUpdates` to read the group chat ID. Group IDs are usually negative numbers.

## 3. Enable Telegram delivery

Make sure Telegram is selected in `config/chief_of_staff.toml`:

```toml
[delivery]
channel = "telegram"
channels = ["console", "telegram"]
```

## 4. Test it

Run the briefing with Telegram delivery:

```bash
python -m chief_of_staff run --channel telegram
```

The bot will send the rendered briefing to the configured chat.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Unauthorized` | The token is wrong or the bot was deleted. Recreate the bot with @BotFather. |
| `Chat not found` | The chat ID is wrong or the bot has not received a message from that chat yet. |
| No message arrives | Make sure you started the bot by sending `/start` or any message first. |
| Bot cannot post to group | Add the bot as a member of the group and grant it send-message permission. |
