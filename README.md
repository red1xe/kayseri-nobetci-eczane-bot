# Kayseri Nöbetçi Eczane Bot

A small Telegram bot that finds on-duty (nöbetçi) pharmacies in Kayseri using the municipal open-data API.

## Features
- Fetches pharmacy data from the Kayseri open data API
- Find nearest on-duty pharmacy by district or by user's location
- Shows contact info and approximate distance

## Requirements
- Python 3.10+ (Dockerfile uses 3.11)
- Docker / docker-compose (optional)
- Internet access to Telegram API and the municipal data endpoint

## Installation (local)
1. Create and activate a virtual environment

Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration
Copy `.env.example` to `.env` and set values:

- `BOT_TOKEN` — your Telegram bot token (required)
- `PHARMACIES_DATA_URL` — municipal API URL (default provided in `.env.example`)

Example `.env`:

```
BOT_TOKEN=your_telegram_bot_token_here
PHARMACIES_DATA_URL=https://acikveri.kayseri.bel.tr/api/kbb/eczane
```

## Usage

Run locally:

```bash
python -m bot.main
```

Build and run with Docker:

```bash
docker build -t kayseri-eczane-bot .
docker run --env-file .env --restart unless-stopped kayseri-eczane-bot
```

Using docker-compose:

```bash
docker compose up --build -d
```

## Files & Structure
- [bot/main.py](bot/main.py#L1) — application entrypoint
- [bot/config.py](bot/config.py#L1) — configuration loader (dotenv)
- [bot/handlers/start.py](bot/handlers/start.py#L1) — /start handler
- [bot/handlers/district.py](bot/handlers/district.py#L1) — district selection flow
- [bot/handlers/location.py](bot/handlers/location.py#L1) — location handling
- [bot/handlers/pharmacy.py](bot/handlers/pharmacy.py#L1) — pharmacy lookup and messages
- [bot/services/pharmacy_service.py](bot/services/pharmacy_service.py#L1) — fetch & normalize API data
- [bot/services/distance_service.py](bot/services/distance_service.py#L1) — distance calculations
- [bot/keyboards/inline.py](bot/keyboards/inline.py#L1) — inline keyboard helpers
- [Dockerfile](Dockerfile#L1) — container image
- [docker-compose.yml](docker-compose.yml#L1) — compose setup
- [.env.example](.env.example#L1) — example environment variables
- [requirements.txt](requirements.txt#L1) — Python dependencies

## Troubleshooting
- Bot not starting / authentication error: ensure `BOT_TOKEN` is set in `.env` and valid.
- API errors: confirm `PHARMACIES_DATA_URL` is reachable and returns expected JSON.
- Missing dependencies: run `pip install -r requirements.txt` inside an active venv.

If you see exceptions related to data fields (KeyError, ValueError), the municipal API schema may have changed — inspect the JSON and update `bot/services/pharmacy_service.py` accordingly.

## Contributing
PRs welcome. Open an issue for discussion before implementing major changes.

## License
This project does not include a license file. Add one if you plan to publish.
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
