# This is a file with all the functions which search the information I want in the Ensembl database
import http.client
import json
from json_classes import Error
from json_classes import UserEncoder
from json_classes import AvailableSpecies
from json_classes import SpeciesChromosomes
from json_classes import ChromosomeLength
from json_classes import GeneSequence
from json_classes import Gene_Info
from json_classes import GenesChromosome
from json_classes import Gene_Calculations
from Seq import Seq


# -- API information
HOSTNAME = "rest.ensembl.org"
METHOD = "GET"


def get_name(json_format):
    """Function for getting the name of the species available in the database"""
    try:
        # -- Connect to the server
        conn = http.client.HTTPSConnection(HOSTNAME)

        ENDPOINT = "/info/species?content-type=application/json"

        # -- Send the request
        conn.request(METHOD, ENDPOINT, None)

        # -- Read the response message from the server
        r1 = conn.getresponse()

        # -- Read the response's body
        data = r1.read().decode("utf-8")

        info = json.loads(data)

        info_species = info['species']
        names = []
        for info_group in info_species:
            names.append(info_group['name'])  # List with the name of all species available in the database

        if not json_format:
            contents = "All species available in the database:<br> " + ', '.join(names) + '.'
        else:
            list_species = AvailableSpecies(names)

            # Serialize the object. The parameter cls corresponds to the encoder we wanna use.
            # In our case is UseEncoder
            contents = json.dumps(list_species, cls=UserEncoder, indent=4)
    except:
        contents = "An error has been produced"
        if json_format:
            reqError = Error(contents)
            contents = json.dumps(reqError, cls=UserEncoder, indent=4)

    return contents


def get_limit_name(txt_limit, json_format):
    """Function for getting x species available in the database being x the limit number"""
    try:
        limit = int(txt_limit)

        conn = http.client.HTTPSConnection(HOSTNAME)

        ENDPOINT = "/info/species?content-type=application/json"

        # -- Send the request
        conn.request(METHOD, ENDPOINT, None)

        # -- Read the response message from the server
        r1 = conn.getresponse()

        # -- Read the response's body
        data = r1.read().decode("utf-8")

        info = json.loads(data)

        info_species = info['species']
        if len(info_species) >= limit >= 0:
            names = []
            for info_group in info_species:
                names.append(info_group['name'])  # List with the name of x species available in the database
            if not json_format:
                contents = str(limit) + " species available in the database:<br> " + ', '.join(
                    names[:limit]) + '.'
            else:
                list_nspecies = AvailableSpecies(names[:limit])
                contents = json.dumps(list_nspecies, cls=UserEncoder, indent=4)
        else:
            contents = "ERROR: The limit introduced is not valid."  # The limit introduced by the user does not
            # belong to the interval [0, number of available species]
            if json_format:
                reqError = Error(contents)
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)

    except ValueError:
        contents = "ERROR: Limit must be an integer"  # The user push SEND in the limit form but
        # write nothing or write a word different than an integer.
        if json_format:
            reqError = Error(contents)
            contents = json.dumps(reqError, cls=UserEncoder, indent=4)
    except:
        contents = "An error has been produced"
        if json_format:
            reqError = Error(contents)
            contents = json.dumps(reqError, cls=UserEncoder, indent=4)

    return contents


def get_karyotype(specie, json_format):
    """Function for getting the name of all the chromosomes of a given specie"""
    try:
        # -- Connect to the server
        conn = http.client.HTTPSConnection(HOSTNAME)

        ENDPOINT = "/info/assembly/" + specie + "?content-type=application/json"

        # -- Send the request
        conn.request(METHOD, ENDPOINT, None)

        # -- Read the response message from the server
        r1 = conn.getresponse()

        # -- Read the response's body
        data = r1.read().decode("utf-8")

        info = json.loads(data)

        list_karyotype = info["karyotype"]
        if json_format:
            chromos = SpeciesChromosomes(list_karyotype)
            contents = json.dumps(chromos, cls=UserEncoder, indent=4)
        else:
            contents = "All the chromosomes of the specie " + specie + ":<br>" + ', '.join(list_karyotype) + '.'
    except KeyError:
        contents = "ERROR: The specie introduced is not correct"
        if json_format:
            reqError = Error(contents)
            contents = json.dumps(reqError, cls=UserEncoder, indent=4)
    except:
        contents = "An error has been produced"
        if json_format:
            reqError = Error(contents)
            contents = json.dumps(reqError, cls=UserEncoder, indent=4)

    return contents


def get_len_chromo(specie, chromo, json_format):
    """Function for getting the length of a given chromosome"""
    try:
        # -- Connect to the server
        conn = http.client.HTTPSConnection(HOSTNAME)

        ENDPOINT = "/info/assembly/" + specie + "?content-type=application/json"

        # -- Send the request
        conn.request(METHOD, ENDPOINT, None)

        # -- Read the response message from the server
        r1 = conn.getresponse()

        # -- Read the response's body
        data = r1.read().decode("utf-8")

        info = json.loads(data)

        length = ''
        compact_info = info["top_level_region"]
        for chromo_name in compact_info:
            if chromo_name['name'] == chromo:
                length = chromo_name['length']
                break
        if length == '':
            contents = "ERROR: The chromosome introduced is not valid."
            if json_format:
                reqError = Error(contents)
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
        else:
            if not json_format:
                contents = "The length of the chromosome " + chromo + " that belongs to the specie " + specie \
                           + " is: " + str(length)
            else:
                chromo_len = ChromosomeLength(length)
                contents = json.dumps(chromo_len, cls=UserEncoder, indent=4)

    except KeyError:
        contents = "ERROR: The specie introduced is not valid"
        if json_format:
            reqError = Error(contents)
            contents = json.dumps(reqError, cls=UserEncoder, indent=4)
    except:
        contents = "An error has been produced"
        if json_format:
            reqError = Error(contents)
            contents = json.dumps(reqError, cls=UserEncoder, indent=4)

    return contents


def get_id(gene):
    """Function for getting the id number of a gene"""
    try:
        # -- Connect to the server
        conn = http.client.HTTPSConnection(HOSTNAME)

        ENDPOINT = "/homology/symbol/homo_sapiens/" + gene + "?content-type=application/json"

        # -- Send the request
        conn.request(METHOD, ENDPOINT, None)

        # -- Read the response message from the server
        r1 = conn.getresponse()

        # -- Read the response's body
        data = r1.read().decode("utf-8")

        info = json.loads(data)

        id_num = info['data'][0]['id']  # Obtain the id of a gene for using in the following functions
    except KeyError:
        id_num = "Error"

    return id_num


def get_sequence(gene, json_format):
    """Function for getting the sequence of a human gene"""
    try:
        # -- Connect to the server
        conn = http.client.HTTPSConnection(HOSTNAME)

        id_num = get_id(gene)
        if id_num == "Error":
            contents = "ERROR: The gene introduced is not recognized as a human gene."
            if json_format:
                reqError = Error(contents)
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
        else:
            ENDPOINT = "sequence/id/" + id_num + "?content-type=text/plain"

            # -- Send the request
            conn.request(METHOD, ENDPOINT, None)

            # -- Read the response message from the server
            r1 = conn.getresponse()

            # -- Read the response's body

            if json_format:
                seq = GeneSequence(r1.read().decode("utf-8"))
                contents = json.dumps(seq, cls=UserEncoder, indent=4)
            else:
                contents = 'Sequence: ' + r1.read().decode("utf-8")
    except:
        contents = "An error has been produced"
        if json_format:
            reqError = Error(contents)
            contents = json.dumps(reqError, cls=UserEncoder, indent=4)

    return contents


def get_gene_info(gene, json_format):
    """Function for getting some information about a human gene"""
    try:
        # -- Connect to the server
        conn = http.client.HTTPSConnection(HOSTNAME)

        id_num = get_id(gene)
        if id_num == "Error":
            contents = "ERROR: The gene introduced is not recognized as a human gene."
            if json_format:
                reqError = Error(contents)
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
        else:
            ENDPOINT = "overlap/id/" + id_num + "?feature=gene;content-type=application/json"

            # -- Send the request
            conn.request(METHOD, ENDPOINT, None)

            # -- Read the response message from the server
            r1 = conn.getresponse()

            # -- Read the response's body
            data = r1.read().decode("utf-8")

            info = json.loads(data)

            start = 0
            end = 0
            length = 0
            chromosome = ''
            for gene1 in info:
                if gene1['id'] == id_num:
                    start = gene1['start']
                    end = gene1['end']
                    length = end - start
                    chromosome = gene1['seq_region_name']
                    break

            contents = "Start position: {}<br> End position: {}<br>" \
                       "Chromosome to which it belongs: {}<br>" \
                       " Length: {}<br> Id: {}.".format(start, end, chromosome, length, id_num)
            if json_format:
                gene_info = Gene_Info(start, end, length, id_num, chromosome)
                contents = json.dumps(gene_info, cls=UserEncoder, indent=4)
    except:
        contents = "An error has been produced"
        if json_format:
            reqError = Error(contents)
            contents = json.dumps(reqError, cls=UserEncoder, indent=4)

    return contents


def get_calcs(gene, json_format):
    """Function for getting the sequence of a human gene, and then for doing some calculations on it"""
    try:
        # -- Connect to the server
        conn = http.client.HTTPSConnection(HOSTNAME)

        id_num = get_id(gene)
        if id_num == "Error":
            contents = "ERROR: The gene introduced is not recognized as a human gene."
            if json_format:
                reqError = Error(contents)
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
        else:
            ENDPOINT = "sequence/id/" + id_num + "?content-type=text/plain"

            # -- Send the request
            conn.request(METHOD, ENDPOINT, None)

            # -- Read the response message from the server
            r1 = conn.getresponse()

            Sequence = Seq(r1.read().decode("utf-8"))  # Use the class Seq we create in the first practice
            totA = Sequence.count('A')  # Number of As
            totC = Sequence.count('C')  # Number of Cs
            totG = Sequence.count('G')  # Number of Gs
            totT = Sequence.count('T')  # Number of Ts
            percA = Sequence.perc('A')  # percentage of As
            percC = Sequence.perc('C')  # percentage of Cs
            percG = Sequence.perc('G')  # percentage of Gs
            percT = Sequence.perc('T')  # percentage of Ts
            if json_format:
                gene_calcs = Gene_Calculations(totA, totC, totG, totT, percA, percC, percG, percT)
                contents = json.dumps(gene_calcs, cls=UserEncoder, indent=4)
            else:
                contents = "Length of As: {}.<br> Length of Cs: {}.<br> Length of Gs: {}.<br>" \
                           "Length of Ts: {}.<br> Percentage of As: {}%<br> " \
                           "Percentage of Cs: {}%.<br> Percentage of Gs: {}%.<br> " \
                           "Percentage of Ts: {}%.".format(totA, totC, totG, totT, percA, percC, percG, percT)
    except:
        contents = "An error has been produced"
        if json_format:
            reqError = Error(contents)
            contents = json.dumps(reqError, cls=UserEncoder, indent=4)

    return contents


def get_name_genes(chromo, start, end, json_format):
    """Function for getting a list with all the genes of a human chromosome in a specific region"""
    try:
        # -- Connect to the server
        conn = http.client.HTTPSConnection(HOSTNAME)

        ENDPOINT = "overlap/region/human/{}:{}-{}?feature=gene;content-type=application/json".format(chromo, start, end)

        # -- Send the request
        conn.request(METHOD, ENDPOINT, None)

        # -- Read the response message from the server
        r1 = conn.getresponse()

        # -- Read the response's body
        data = r1.read().decode("utf-8")

        info = json.loads(data)

        genes = []
        for gene_info in info:
            genes.append(gene_info['external_name'])
        if genes == []:
            contents = "Not genes located in that region."
            if json_format:
                reqError = Error(contents)
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
        else:
            contents = "The names of the genes located in the chromosome introduced " \
                       "from the start to end positions are:<br>" + ', '.join(genes)
            if json_format:
                genes_name = GenesChromosome(genes)
                contents = json.dumps(genes_name, cls=UserEncoder, indent=4)

    except TypeError:
        contents = 'ERROR: The data introduced is not valid'
        if json_format:
            reqError = Error(contents)
            contents = json.dumps(reqError, cls=UserEncoder, indent=4)
    except:
        contents = "An error has been produced"
        if json_format:
            reqError = Error(contents)
            contents = json.dumps(reqError, cls=UserEncoder, indent=4)

    return contents
