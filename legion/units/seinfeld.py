# Copyright 2020 John Reese
# Licensed under the MIT License

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Optional

import aiosqlite
from aioseinfeld import Seinfeld
from discord import Message

from legion.unit import Unit, command

LOG = logging.getLogger(__name__)


class SeinfeldQuotes(Unit):
    @command(usage="[subject]", description="post a random Seinfeld quote")
    async def seinfeld(self, message: Message, subject: str) -> str:
        async with Seinfeld(self.bot.config.seinfeld.db_path) as seinfeld:
            quote = await seinfeld.random(subject=subject)
            LOG.debug(f"got quote {quote}")
            if quote:
                passage = await seinfeld.passage(quote)
                episode = passage.episode
                quotes = passage.quotes

                header = (
                    f"Episode s{episode.season.number}e{episode.number} "
                    f'"{episode.title}"'
                )
                lines = [f"{quote.speaker.name}:  {quote.text}" for quote in quotes]
                body = "\n".join(lines)

                return f"{header}\n{body}"
