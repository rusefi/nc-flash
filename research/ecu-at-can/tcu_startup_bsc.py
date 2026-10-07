"""Bounded BCR1/BCR2/WCR initialization; no external bus cycles/timing.

SH7055S REJ09B0045-0200H PDF176 conflicts with184 on WCR reset7777 vsFFFF.
Require explicit initial WCR sample; firmware overwrites it without reading.
"""
from tcu_startup_configuration_words import ConfigurationWords


class Registers(ConfigurationWords):
    MASKS={0xFFFFEC20:15,0xFFFFEC22:65535,0xFFFFEC24:65535}

    def __init__(self,*,wcr_initial):
        super().__init__({0xFFFFEC20:15,0xFFFFEC22:65535,0xFFFFEC24:wcr_initial},self.MASKS)
