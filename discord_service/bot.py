import os
import asyncio
import signal
import sys
import threading
import traceback
from pathlib import Path
from platform import system

import discord
from pycord.multicog import apply_multicog

__version__ = "12.2.5"

from discord_service.cogs.image_service_cog import ImageService
from services.environment_service import EnvService

PID_FILE = Path("bot.pid")
PROCESS = None

if sys.platform == "win32":
    separator = "\\"
else:
    separator = "/"

#
# Message queueing for the debug service, defer debug messages to be sent later so we don't hit rate limits.
#
message_queue = asyncio.Queue()
deletion_queue = asyncio.Queue()


#
# Settings for the bot
#
activity = discord.Activity(
    type=discord.ActivityType.watching, name="for chances to describe!"
)
bot = discord.Bot(intents=discord.Intents.all(), command_prefix="!", activity=activity)

@bot.event  # Using self gives u
async def on_ready():  # I can make self optional by
    print("We have logged in as {0.user}".format(bot))


@bot.event
async def on_application_command_error(
    ctx: discord.ApplicationContext, error: discord.DiscordException
):
    if isinstance(error, discord.CheckFailure):
        pass
    else:
        raise error


async def main():
    data_path = EnvService.environment_path_with_fallback("DATA_DIR")

    if not data_path.exists():
        raise OSError(f"Data path: {data_path} does not exist ... create it?")

    bot.add_cog(
        ImageService(
            bot,
        )
    )

    apply_multicog(bot)

    await bot.start(EnvService.get_discord_token())


def check_process_file(pid_file: Path) -> bool:
    """Check the pid file exists and if the Process ID is actually running"""
    if not pid_file.exists():
        return False
    if system() == "Linux":
        with pid_file.open("r") as pfp:
            try:
                proc_pid_path = Path("/proc") / "{int(pfp.read().strip())}"
                print("Checking if PID proc path {proc_pid_path} exists")
            except ValueError:
                # We don't have a valid int in the PID File^M
                pid_file.unlink()
                return False
        return proc_pid_path.exists()
    return True


def cleanup_pid_file(signum, frame):
    # Kill all threads
    if PROCESS:
        print("Killing all subprocesses")
        PROCESS.terminate()
    print("Killed all subprocesses")
    # Always cleanup PID File if it exists
    if PID_FILE.exists():
        print(f"Removing PID file {PID_FILE}", flush=True)
        PID_FILE.unlink()


# Run the bot with a token taken from an environment file.
def init():
    global PROCESS
    # Handle SIGTERM cleanly - Docker sends this ...
    signal.signal(signal.SIGTERM, cleanup_pid_file)

    if check_process_file(PID_FILE):
        print(
            "Process ID file already exists. Remove the file if you're sure another instance isn't running with the command: rm bot.pid"
        )
        sys.exit(1)
    else:
        with PID_FILE.open("w") as f:
            f.write(str(os.getpid()))
            print(f"Wrote PID to file {PID_FILE}")
            f.close()
    try:

        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, killing and removing PID")
    except Exception as e:
        traceback.print_exc()
        print(str(e))
        print("Removing PID file")
    finally:
        cleanup_pid_file(None, None)

    sys.exit(0)


if __name__ == "__main__":
    sys.exit(init())
