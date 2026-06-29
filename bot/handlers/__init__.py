"""
Handlers package
"""

from aiogram import Dispatcher

from . import commands
from . import callbacks


def register_handlers(dp: Dispatcher):
    """Register all handlers"""
    commands.register_handlers(dp)
    callbacks.register_handlers(dp)
