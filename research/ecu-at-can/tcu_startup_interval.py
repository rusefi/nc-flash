"""ITVRR configuration only; no TCNT0 edges, interrupt or ADC events.

SH7055S manual section11.2.7, PDF indices339..343; table11.3 indices240/241.
All bits readable/writable; byte accesses; reset zero. This owner only supplies
these three latches, without claiming the TCU's exact silicon identification.
"""
from tcu_startup_configuration_words import ConfigurationWords


class Registers(ConfigurationWords):
    def __init__(self):
        masks={0xFFFFF424:255,0xFFFFF426:255,0xFFFFF428:255}
        super().__init__({a:0 for a in masks},masks,size=1)
