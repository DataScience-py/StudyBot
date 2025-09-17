import asyncio
import json
from asyncio import Task, create_task, gather
from time import perf_counter
from typing import Any, cast

import aiofiles

from studybot.config import config, get_logger

logger = get_logger(__name__)


class DB:
    def __init__(self) -> None:
        self.ram_data: dict[str, dict[str, Any]] = {}
        self.DB_DIR_USERS_PATH = config.BASE_PATH / "data" / "users"
        self.TASK_DIR_PATH = config.BASE_PATH / "data" / "tasks"
        self._not_save_data = {
            config.TASK_ANSWER,
            config.TASK_TEXT,
            config.LAST_USE_RAM,
        }
        if not self.DB_DIR_USERS_PATH.exists():
            self.DB_DIR_USERS_PATH.mkdir(parents=True, exist_ok=True)
        if not self.TASK_DIR_PATH.exists():
            self.TASK_DIR_PATH.mkdir(parents=True, exist_ok=True)

    async def get_user_db(self, user_id: int) -> Task[dict[str, Any]]:
        return create_task(self._get_user_data(user_id))

    async def _get_user_data(self, user_id: int) -> dict[str, Any]:
        user_db: dict[str, Any] = {}
        # RAM
        if self.ram_data.get(str(user_id), None) is not None:
            return self.ram_data[str(user_id)]

        # find file
        user_path = self.DB_DIR_USERS_PATH.joinpath(f"{user_id}.json")
        if user_path.exists():
            async with aiofiles.open(user_path, encoding="utf-8") as f:
                content = await f.read()
                user_db = cast("dict[str, Any]", json.loads(content))
        else:
            async with aiofiles.open(
                user_path,
                mode="w",
                encoding="utf-8",
            ) as f:
                await f.write(json.dumps(user_db))
            return user_db
        user_db[config.LAST_USE_RAM] = int(perf_counter() // 60)

        return user_db

    async def update_user_data(
        self,
        user_id: int,
        data: dict[str, Any],
    ) -> None:
        if data.get(config.LAST_USE_RAM) is None:
            data[config.LAST_USE_RAM] = int(perf_counter() // 60)
        self.ram_data[str(user_id)] = data

    async def _save_user_data(self, user_id: str) -> None:
        user_path = self.DB_DIR_USERS_PATH.joinpath(f"{user_id}.json")
        data_to_save = {
            k: v
            for k, v in self.ram_data[user_id].items()
            if k not in self._not_save_data
        }
        async with aiofiles.open(user_path, mode="w+", encoding="utf-8") as f:
            await f.write(json.dumps(data_to_save))

    async def clear_user_ram(self) -> None:
        await self.save_all_user_data()
        for user_id, value in self.ram_data.items():
            if (
                int(perf_counter() // 60) - value[config.LAST_USE_RAM]
                >= config.RAM_TIME_MIN
            ):
                del self.ram_data[user_id]

    async def save_all_user_data(self) -> None:
        logger.info("Save all user data to files")
        tasks = [self._save_user_data(user_id) for user_id in self.ram_data]
        if tasks:
            await gather(*tasks)

    async def add_task(
        self,
        subjects: str,
        number: int,
        text: str,
        answer: str,
    ) -> None:
        json_task = {
            config.TASK_TEXT: text,
            config.TASK_ANSWER: answer,
        }
        full_path_task = self.TASK_DIR_PATH.joinpath(f"{subjects}/{number}/")
        task_ids_file_path = full_path_task.joinpath(config.ID_TASK_FILE)
        if not full_path_task.exists():
            full_path_task.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(
                task_ids_file_path,
                mode="w",
                encoding="utf-8",
            ) as f:
                await f.write("0")
        async with aiofiles.open(
            task_ids_file_path,
            mode="w+",
            encoding="utf-8",
        ) as f:
            last_id = int(await f.read())
            logger.info("load task %s %i", last_id, last_id)
        task_id: int = last_id + 1
        task_path = full_path_task.joinpath(f"{task_id}.json")
        async with aiofiles.open(
            task_path,
            mode="w+",
            encoding="utf-8",
        ) as f:
            await f.write(json.dumps(json_task))

    async def remove_task(
        self,
        subjects: str,
        number: str,
        task_id: int,
    ) -> None: ...
    async def get_task(
        self,
        subject: str,
        number: int,
        task_id: str,
    ) -> dict[str, Any]:
        path_to_file = self.TASK_DIR_PATH.joinpath(
            f"{subject}/{number}/{task_id}.json",
        )
        async with aiofiles.open(path_to_file, encoding="utf-8") as f:
            content = await f.read()
            return cast("dict[str, Any]", json.loads(content))

    async def get_all_task(self, subject: str, number: str) -> list[str]:
        return [
            p.name[:-5]
            for p in self.TASK_DIR_PATH.joinpath(
                subject,
                number,
            ).iterdir()
            if p.is_file()
        ]

    async def get_subjects(self) -> list[str]:
        return [i.name for i in self.TASK_DIR_PATH.iterdir() if i.is_dir()]

    async def get_numbers(self, subject: str) -> list[str]:
        return [
            i.name
            for i in self.TASK_DIR_PATH.joinpath(subject).iterdir()
            if i.is_dir()
        ]


db = DB()


async def clear_user_ram_time() -> None:
    counter = 0
    logger.info("Start clear user ram time %s", config.RUN)
    while config.RUN:
        try:
            logger.info("Clear user ram time %s", counter)
            counter += config.CHECK_INTERVAL
            if counter >= config.INTERVAL_SAVE_RAM_SEC:
                await db.clear_user_ram()
                counter = 0
        except Exception:
            logger.exception("Error in monitor_app:")

        await asyncio.sleep(config.CHECK_INTERVAL)
