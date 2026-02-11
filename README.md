# Kayseri Nobetçi Eczane Bot

Lightweight Telegram bot for finding on-duty (nöbetçi) pharmacies in Kayseri.

## Requirements

- Python 3.10+
- See `requirements.txt` for Python package dependencies

## Quickstart (Windows)

1. Clone the repo:

	git clone <repo-url>
	cd kayseri-nobetci-eczane-bot

2. Create a virtual environment named `.venv` and activate it:

	python -m venv .venv
	.venv\Scripts\activate       # Command Prompt
	# or
	.\.venv\Scripts\Activate.ps1  # PowerShell

3. Install dependencies:

	pip install -r requirements.txt

4. Provide your Telegram bot token:

	Create a file named `.env` in the project root with the following content:

	BOT_TOKEN=your_telegram_bot_token_here

	Note: Do NOT commit `.env` or any secrets to the repository. Add `.env` to `.gitignore`.

5. Run the bot:

	python -m bot.main

## Project layout

- `bot/` — main application package
- `bot/handlers/` — Telegram update handlers
- `bot/services/` — service helpers (distance, pharmacy lookup)
- `keyboards/` — inline keyboard helpers

## Preparing for GitHub

- Ensure `.env` is listed in your `.gitignore`.
- The repository includes a `.venv` marker file indicating the virtual environment name.
- Keep secrets out of the repo and use GitHub Secrets for CI or deployment.

## Notes

- The bot reads the token from the environment via `python-dotenv` (`BOT_TOKEN`).
- Entry point: run `python -m bot.main`.

---
If you want, I can also add a `.gitignore` with common Python ignores and a simple GitHub Actions workflow for CI.
