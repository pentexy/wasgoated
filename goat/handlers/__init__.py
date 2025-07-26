from .start import register_start
from .owner import register_owner
from .add_account import register_add_account
from .add_smtp import register_add_smtp
from .report import register_report

def register_handlers(dp):
    register_start(dp)
    register_owner(dp)
    register_add_account(dp)
    register_add_smtp(dp)
    register_report(dp)
