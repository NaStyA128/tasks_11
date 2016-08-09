import logging

log = logging.getLogger(__name__)
SH = logging.StreamHandler()
SH.setLevel(logging.DEBUG)
f = logging.Formatter('%(name)s:%(levelname)s - %(message)s')
SH.setFormatter(f)
log.addHandler(SH)
