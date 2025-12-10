#! /usr/bin/env/ python3

from dataclasses import dataclass
from datetime import date

@dataclass
class Battle:
    battleName: str
    date: date
    countriesInvolved: str
    winner: str
    loser: str
    victorForces: int
    vanquishedForces: int
    totalVictorDeaths: int
    totalVanquishedDeaths: int
    significantFiguresPresent: str
    notableDeaths: str

    @property
    def total_Deaths(self) -> int:
        return self.totalVictorDeaths + self.totalVanquishedDeaths
