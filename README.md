# xemexpy
Notification engine for twitter feed (@nem.xem)

Executes on Heroku @ xemexpy.herokuapp.com

## Twitter environment variables

Set these before running the app if you want Twitter posting enabled:

- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`

If these are not set, the app will skip sending Twitter updates.

## Development setup

Install the project with development dependencies:

- `uv sync --dev`

Run the test suite:

- `uv run pytest`

