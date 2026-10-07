"""TCNR word configuration; no compare-match or down-counter events.

Compatible SH7055S section11.2.12, PDFindex354: all16 bits R/W/reset0.
"""
from tcu_startup_configuration_words import ConfigurationWords


class Registers(ConfigurationWords):
    def __init__(self):
        super().__init__({0xFFFFF662:0},{0xFFFFF662:65535})
