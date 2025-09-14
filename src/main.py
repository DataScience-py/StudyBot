"""Run the application."""

import asyncio

import nest_asyncio

from studybot import run_study_bot

nest_asyncio.apply()
loop = asyncio.get_event_loop()
loop.run_until_complete(run_study_bot())
