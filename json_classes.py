import json


class UserEncoder(json.JSONEncoder):

    def default(self, obj):
        return obj.__dict__


class Error(object):

    def __init__(self, ErrorDescription):
        self.ErrorDescription = ErrorDescription


class AvailableSpecies(object):

    def __init__(self, Species):
        self.Species = Species


class SpeciesChromosomes(object):

    def __init__(self, Chromosomes):
        self.Chromosomes = Chromosomes


class ChromosomeLength(object):

    def __init__(self, Length):
        self.Length = Length


class GeneSequence(object):

    def __init__(self, Sequence):
        self.Sequence = Sequence


class Gene_Info(object):

    def __init__(self, Start, End, Length, Id, Chromosome):
        self.Start = Start
        self.End = End
        self.Length = Length
        self.Id = Id
        self.Chromosome = Chromosome


class Gene_Calculations(object):

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

    def __init__(self, Genes):
        self.Genes = Genes


class User(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
