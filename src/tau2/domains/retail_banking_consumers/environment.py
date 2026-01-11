# Copyright Sierra
from pathlib import Path
from typing import Optional

from tau2.data_model.tasks import Task
from tau2.domains.retail_banking_consumers.data_model import RetailBankingDB
from tau2.domains.retail_banking_consumers.tools import RetailBankingTools
from tau2.domains.retail_banking_consumers.utils import (
    RETAIL_BANKING_DB_PATH,
    RETAIL_BANKING_POLICY_PATH,
    RETAIL_BANKING_TASK_SET_PATH,
)
from tau2.environment.environment import Environment
from tau2.utils import load_file


def get_environment(
    db: Optional[RetailBankingDB] = None,
    solo_mode: bool = False,
) -> Environment:
    """
    Get the environment for the retail banking consumers domain.

    Args:
        db: Optional database instance. If None, loads from RETAIL_BANKING_DB_PATH
        solo_mode: Whether to run in solo mode (not currently supported)

    Returns:
        Environment instance configured for retail banking consumers domain

    Raises:
        ValueError: If solo_mode is True (not yet supported)
    """
    if solo_mode:
        raise ValueError("Retail banking consumers domain does not support solo mode yet")

    if db is None:
        db = RetailBankingDB.load(RETAIL_BANKING_DB_PATH)

    tools = RetailBankingTools(db)

    with open(RETAIL_BANKING_POLICY_PATH, "r") as fp:
        policy = fp.read()

    return Environment(
        domain_name="retail-banking-consumers",
        policy=policy,
        tools=tools,
    )


def get_tasks(task_split_name: Optional[str] = "base") -> list[Task]:
    """
    Get tasks for the retail banking consumers domain.

    Args:
        task_split_name: Name of the task split to load. If None, returns all tasks.
                         Must be a valid split defined in split_tasks.json.
                         Default is 'base'.

    Returns:
        List of tasks for the specified split

    Raises:
        ValueError: If the task split name is invalid
    """
    tasks = load_file(RETAIL_BANKING_TASK_SET_PATH)
    tasks = [Task.model_validate(task) for task in tasks]

    if task_split_name is None:
        return tasks

    task_splits = get_tasks_split()
    if task_split_name not in task_splits:
        raise ValueError(
            f"Invalid task split name: {task_split_name}. Valid splits are: {list(task_splits.keys())}"
        )

    tasks = [task for task in tasks if task.id in task_splits[task_split_name]]
    return tasks


def get_tasks_split() -> dict[str, list[str]]:
    """
    Get the task splits configuration.

    Returns:
        Dictionary mapping split names to lists of task IDs
    """
    split_file = (
        Path(RETAIL_BANKING_TASK_SET_PATH).parent
        / f"split_{Path(RETAIL_BANKING_TASK_SET_PATH).stem}.json"
    )
    return load_file(split_file)
