"""Bounded SH7055S UBC configuration registers; no break matching/events.

REJ09B0045-0200H PDF160..166: four full-word address/mask registers,
UBBR low8 controls and UBCR low3 controls. Word accesses only in this fixture.
"""


from tcu_startup_configuration_words import ConfigurationWords


class Registers(ConfigurationWords):
    MASKS={0xFFFFEC00:0xFFFF,0xFFFFEC02:0xFFFF,
           0xFFFFEC04:0xFFFF,0xFFFFEC06:0xFFFF,0xFFFFEC08:0xFF,0xFFFFEC0A:7}

    def __init__(self):
        super().__init__({a:0 for a in self.MASKS},self.MASKS)
