import re
import xdist.scheduler as xdist_scheduler


def _split_scope(self, nodeid):
    return re.search(r'\[(\w+)-', nodeid).group(1)


xdist_scheduler.loadscope.LoadScopeScheduling._split_scope = _split_scope
