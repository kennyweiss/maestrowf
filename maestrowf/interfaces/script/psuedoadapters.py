import getpass
import logging
import os
import re

from maestrowf.abstracts.interfaces import SchedulerScriptAdapter
from maestrowf.abstracts.enums import JobStatusCode, State, SubmissionCode, \
    CancelCode
from maestrowf.interfaces import ScriptAdapterFactory
from maestrowf.interfaces.script import CancellationRecord, SubmissionRecord
from maestrowf.utils import start_process

LOGGER = logging.getLogger(__name__)

class DryRunAdapter(SchedulerScriptAdapter):
    """A pseudoadapter capable of monkeypatching itself to provide dry run."""