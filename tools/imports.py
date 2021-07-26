import discord
import json
import requests
import asyncio
import youtube_dl
import functools
import itertools
import math
import random
import ffmpeg
import glob
import os
import imp

from typing import Union
from async_timeout import timeout

from discord.ext import commands
from discord.ext.commands import CommandNotFound

from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash import cog_ext, ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import wait_for_component
from discord_slash.utils.manage_components import create_select, create_select_option
