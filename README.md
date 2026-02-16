# Purge Bot

A lightweight Discord bot for bulk deleting messages in your server using a single slash command.

---

## Features

- Delete up to 100 messages at once with `/purge`
- Fast bulk deletion via Discord's batch API
- Permission checks for both the user and the bot
- All responses are ephemeral (only visible to the user who ran the command)
- Works independently across multiple servers

---

## Requirements

- Python 3.8+
- [discord.py](https://github.com/Rapptz/discord.py) v2.0+

Install dependencies:

```bash
pip install discord.py
```

---

## Setup

1. **Clone or download** this repository.

2. **Create a bot** on the [Discord Developer Portal](https://discord.com/developers/applications) and copy your bot token.

3. **Enable the following intents** in the Developer Portal under your bot's settings:
   - Message Content Intent
   - Server Members Intent (optional but recommended)

4. **Paste your token** into `yourbot.py`:
   ```python
   TOKEN = ('your_token_here')
   ```

5. **Invite the bot** to your server with the following permissions:
   - Manage Messages
   - Read Messages / View Channels
   - Send Messages

6. **Run the bot:**
   ```bash
   python yourbot.py
   ```

---

## Commands

| Command | Description |
|---|---|
| `/purge <amount>` | Deletes the specified number of messages (1–100) in the current channel |

### Notes

- Only users with the **Manage Messages** permission can use `/purge`.
- Discord only allows bulk deletion of messages **less than 14 days old**. Older messages cannot be deleted and will be reported back to you.
- All command responses are only visible to you.

---

## Example Output

```
Deleted 100 messages.
```
```
Couldn't delete any messages due to Discord limitations. All of the affected messages were too old.
```

---

## License

This project is open source and free to use.
