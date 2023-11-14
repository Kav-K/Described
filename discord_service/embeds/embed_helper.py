from typing import List

import discord


class EmbedStatics:
    def __init__(self):
        pass

    def status_to_string(status):
        if status:
            return "enabled"
        else:
            return "disabled"

    @staticmethod
    def build_status_display_embed(status):
        embed = discord.Embed(
            title="Describer",
            description=f"The image descriptions status for this server is: `{EmbedStatics.status_to_string(status)}`",
            color=discord.Color.blurple(),
        )
        embed.set_thumbnail(url="https://i.imgur.com/txHhNzL.png")
        return embed

    @staticmethod
    def build_status_change_success_embed(status):
        embed = discord.Embed(
            title="Describer",
            description=f"Successfully changed image descriptions for this server to the status:\n`{EmbedStatics.status_to_string(status)}`",
            color=discord.Color.green(),
        )
        # thumbnail of https://i.imgur.com/I5dIdg6.png
        embed.set_thumbnail(url="https://i.imgur.com/I5dIdg6.png")
        return embed

    @staticmethod
    def build_status_set_failure_embed(message):
        embed = discord.Embed(
            title="Describer",
            description=f"There was an error changing the image descriptions status for this server: "
            + message,
            color=discord.Color.red(),
        )
        embed.set_thumbnail(url="https://i.imgur.com/hbdBZfG.png")
        return embed

    @staticmethod
    def build_image_analysis_failure_embed(message):
        embed = discord.Embed(
            title="Describer",
            description=f"There was an error describing the image sent: " + message,
            color=discord.Color.red(),
        )
        embed.set_thumbnail(url="https://i.imgur.com/hbdBZfG.png")
        return embed

    @staticmethod
    def build_described_image_embed(
        message: discord.Message, image_url: str, description: str
    ):
        embed = discord.Embed(
            title=f"{message.author.display_name} sent an image that was automatically described",
            description=f"{description}",
            color=discord.Color.light_gray(),
        )
        embed.set_thumbnail(url=image_url)
        embed.set_author(
            name=message.author.display_name, icon_url=message.author.avatar.url
        )
        embed.set_footer(
            text=f"Automatically described for an image sent by {message.author.display_name}",
            icon_url=message.author.avatar.url,
        )
        return embed
