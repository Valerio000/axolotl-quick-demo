from dataclasses import dataclass

@dataclass
class CorpusEntry:
    spanish: str
    nahuatl: str
    dialect: str
    document: str
    iso: str = ""
