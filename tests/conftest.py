import importlib.util
import sys
import types
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_module(module_name, path):
    sys.modules.pop(module_name, None)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class FakeAuthHandler:
    instances = []

    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = None
        self.access_token_secret = None
        self.__class__.instances.append(self)

    def set_access_token(self, access_token, access_token_secret):
        self.access_token = access_token
        self.access_token_secret = access_token_secret


class FakeAPI:
    instances = []

    def __init__(self, auth):
        self.auth = auth
        self.updated_statuses = []
        self.__class__.instances.append(self)

    def update_status(self, msg):
        self.updated_statuses.append(msg)


@pytest.fixture
def fake_tweepy(monkeypatch):
    FakeAuthHandler.instances = []
    FakeAPI.instances = []
    module = types.ModuleType("tweepy")
    module.OAuthHandler = FakeAuthHandler
    module.API = FakeAPI
    module.auth_instances = FakeAuthHandler.instances
    module.api_instances = FakeAPI.instances
    monkeypatch.setitem(sys.modules, "tweepy", module)
    return module


@pytest.fixture
def app_module(fake_tweepy):
    return load_module("app_under_test", ROOT / "app.py")


@pytest.fixture
def main_module():
    return load_module("main_under_test", ROOT / "main.py")


@pytest.fixture
def clock_module(monkeypatch):
    class FakeScheduler:
        def __init__(self):
            self.jobs = []
            self.started = False

        def scheduled_job(self, *args, **kwargs):
            def decorator(func):
                self.jobs.append({"args": args, "kwargs": kwargs, "func": func})
                return func

            return decorator

        def start(self):
            self.started = True

    apscheduler = types.ModuleType("apscheduler")
    schedulers = types.ModuleType("apscheduler.schedulers")
    blocking = types.ModuleType("apscheduler.schedulers.blocking")
    blocking.BlockingScheduler = FakeScheduler

    monkeypatch.setitem(sys.modules, "apscheduler", apscheduler)
    monkeypatch.setitem(sys.modules, "apscheduler.schedulers", schedulers)
    monkeypatch.setitem(sys.modules, "apscheduler.schedulers.blocking", blocking)

    return load_module("clock_under_test", ROOT / "clock.py")