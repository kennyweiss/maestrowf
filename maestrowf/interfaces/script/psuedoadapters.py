"""A module containing psuedoasdapters for miscellaneous functionality."""
from collections import defaultdict
from hashlib import md5
import logging

from maestrowf.abstracts.interfaces import ScriptAdapter
from maestrowf.abstracts.enums import JobStatusCode, State, SubmissionCode, \
    CancelCode
from maestrowf.interfaces.script import CancellationRecord, SubmissionRecord

LOGGER = logging.getLogger(__name__)


class DryRunAdapter(ScriptAdapter):
    """A pseudoadapter capable of monkeypatching itself to provide dry run."""

    key = "dryrun"

    def __init__(self, **kwargs):
        """
        Initialize an instance of the DryRunAdapter.

        The DryRunAdapter provides Maestro's support for dry run.
        This adapter works primarily by taking in a complete batch dictionary
        and wrapping the implementation to write scripts and then mocking all
        scheduler calls to mimic success.

        :param **kwargs: A dictionary with default settings for the adapter.
        """

        super(DryRunAdapter, self).__init__(**kwargs)

        # Monkey patch in the methods from the appropriate adapter class
        # that would have been executed.
        from .. import ScriptAdapterFactory
        adapter_type = kwargs.get("scheduler", "local")
        self._adapter = \
            ScriptAdapterFactory.get_adapter(adapter_type)(**kwargs)

    def cancel_jobs(self, joblist):
        return CancellationRecord(CancelCode.OK, 0)

    def check_jobs(self, joblist):
        return JobStatusCode.OK, defaultdict(lambda: State.FINISHED)

    def _write_script(self, ws_path, step):
        return self._adapter._write_script(ws_path, step)

    def submit(self, step, path, cwd, job_map=None, env=None):
        return SubmissionRecord(
            SubmissionCode.OK, 0, md5(step.name).hexdigest())
