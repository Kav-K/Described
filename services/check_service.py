from typing import Callable

import discord
from services.environment_service import EnvService


class Check:
    @staticmethod
    def check_admin_roles() -> Callable:
        async def inner(ctx: discord.ApplicationContext):
            admin_roles = EnvService.get_admin_roles()
            if EnvService.get_admin_roles() == [None]:
                admin_roles = ["admin"]

            if not any(role.name.lower() in admin_roles for role in ctx.user.roles):
                await ctx.defer(ephemeral=True)
                await ctx.respond(
                    f"You don't have permission, list of roles is {admin_roles}",
                    ephemeral=True,
                    delete_after=10,
                )
                return False
            return True

        return inner
