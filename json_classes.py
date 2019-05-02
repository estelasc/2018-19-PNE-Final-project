# Some useful classes for the advanced level of the final project
import json


class UserEncoder(json.JSONEncoder):
    """Class for encode data in json format"""
    def default(self, obj):
        return obj.__dict__


class Error(object):
    """Class for catching errors"""

    def __init__(self, ErrorDescription):
        self.ErrorDescription = ErrorDescription


class AvailableSpecies(object):
    """Class for showing all or some of the available species in the Ensembl database"""

    def __init__(self, Species):
        self.Species = Species


class SpeciesChromosomes(object):
    """Class for showing the name of all the chromosomes of a given specie"""

    def __init__(self, Chromosomes):
        self.Chromosomes = Chromosomes


class ChromosomeLength(object):
    """Class for showing the length of a given chromosome"""

    def __init__(self, Length):
        self.Length = Length


class GeneSequence(object):
    """Class for showing the sequence of a given human gene"""

    def __init__(self, Sequence):
        self.Sequence = Sequence


class Gene_Info(object):
    """Class for showing some information about a given human gene"""

    def __init__(self, Start, End, Length, Id, Chromosome):
        self.Start = Start
        self.End = End
        self.Length = Length
        self.Id = Id
        self.Chromosome = Chromosome


class Gene_Calculations(object):
    """Class for showing some calculations on the sequence of a given human gene"""

    def __init__(self, LengthA, LengthC, LengthG, LengthT, PercA, PercC, PercG, PercT):
        self.LengthA = LengthA
        self.LengthC = LengthC
        self.LengthG = LengthG
        self.LengthT = LengthT
        self.PercA = PercA
        self.PercC = PercC
        self.PercG = PercG
        self.PercT = PercT


class GenesChromosome(object):
    """Class for showing a list with the genes located in a given region within a given chromosome"""

    def __init__(self, Genes):
        self.Genes = Genes
