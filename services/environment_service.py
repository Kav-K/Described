import os
import sys
import traceback
from pathlib import Path
from typing import Union

from dotenv import load_dotenv


def app_root_path():
    app_path = Path(sys.argv[0]).resolve()
    try:
        if app_path.parent.name == "bin":  # Installed in unixy hierachy
            return app_path.parents[1]
    except IndexError:
        pass
    return app_path.parent


# None will let direnv do its' thing
env_paths = [Path(".env"), app_root_path() / "etc/environment", None]

for env_path in env_paths:
    print("Loading environment from " + str(env_path))
    load_dotenv(dotenv_path=env_path)


class EnvService:
    # To be expanded upon later!
    def __init__(self):
        self.env = {}

    @staticmethod
    def environment_path_with_fallback(env_name, relative_fallback=None):
        directory = os.getenv(env_name)
        if directory is not None:
            return Path(directory).resolve()

        if relative_fallback:
            app_relative = (app_root_path() / relative_fallback).resolve()
            if app_relative.exists():
                return app_relative

        return Path.cwd()

    @staticmethod
    def save_path():
        share_dir = os.getenv("SHARE_DIR")
        if share_dir is not None:
            return Path(share_dir)
        return app_root_path()

    @staticmethod
    def find_shared_file(file_name):
        share_file_paths = []
        share_dir = os.getenv("SHARE_DIR")
        if share_dir is not None:
            share_file_paths.append(Path(share_dir) / file_name)

        share_file_paths.extend(
            [
                app_root_path() / "share" / file_name,
                app_root_path() / file_name,
                Path(file_name),
            ]
        )

        for share_file_path in share_file_paths:
            if share_file_path.exists():
                return share_file_path.resolve()

        raise ValueError(f"Unable to find shared data file {file_name}")

    @staticmethod
    def get_allowed_guilds():
        # ALLOWED_GUILDS is a comma separated list of guild ids
        # It can also just be one guild ID
        # Read these allowed guilds and return as a list of ints
        try:
            allowed_guilds = os.getenv("ALLOWED_GUILDS")
        except Exception:
            allowed_guilds = None

        if allowed_guilds is None:
            raise ValueError(
                "ALLOWED_GUILDS is not defined properly in the environment file!"
                "Please copy your server's guild ID and put it into ALLOWED_GUILDS in the .env file."
                'For example a line should look like: `ALLOWED_GUILDS="971268468148166697"`'
            )

        allowed_guilds = (
            allowed_guilds.split(",") if "," in allowed_guilds else [allowed_guilds]
        )
        allowed_guilds = [int(guild) for guild in allowed_guilds]
        return allowed_guilds

    @staticmethod
    def get_described_channels():
        # ALLOWED_GUILDS is a comma separated list of guild ids
        # It can also just be one guild ID
        # Read these allowed guilds and return as a list of ints
        try:
            described_channels = os.getenv("DESCRIBED_CHANNELS")
        except Exception:
            described_channels = None

        if described_channels is None:
            raise ValueError(
                "DESCRIBED_CHANNELS is not properly defined in your environment file. All channels will be enabled for image descriptions"
            )

        described_channels = (
            described_channels.split(",")
            if "," in described_channels
            else [described_channels]
        )
        return described_channels

    @staticmethod
    def get_discord_token():
        try:
            e2b_key = os.getenv("DISCORD_TOKEN")
            return e2b_key
        except Exception:
            return None

    @staticmethod
    def get_openai_api_key():
        try:
            openai_key = os.getenv("OPENAI_API_KEY")
            return openai_key
        except Exception:
            return None

    @staticmethod
    def get_admin_roles():
        # ADMIN_ROLES is a comma separated list of string roles
        # It can also just be one role
        # Read these allowed roles and return as a list of strings
        try:
            admin_roles = os.getenv("ADMIN_ROLES")
        except Exception:
            admin_roles = None

        if admin_roles is None:
            print(
                "ADMIN_ROLES is not defined properly in the environment file!"
                "Please copy your server's role and put it into ADMIN_ROLES in the .env file."
                'For example a line should look like: `ADMIN_ROLES="Admin"`'
            )
            print("Defaulting to allowing all users to use admin commands...")
            return [None]

        admin_roles = (
            admin_roles.lower().split(",")
            if "," in admin_roles
            else [admin_roles.lower()]
        )
        return admin_roles
