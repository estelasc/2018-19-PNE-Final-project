# This is the server for the final proyect.
import http.server
import socketserver
import json
from Ensembl_functions import get_karyotype
from Ensembl_functions import get_name
from Ensembl_functions import get_len_chromo
from Ensembl_functions import get_sequence
from Ensembl_functions import get_gene_info
from Seq import Seq
from Ensembl_functions import get_name_genes
from json_classes import UserEncoder
from Ensembl_functions import get_limit_name
from json_classes import Error
from json_classes import Gene_Calculations

# Define the Server's port: 8000
PORT = 8000

# For preventing the error "post already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Advanced level
        json_format = False
        if '?json=1' in self.path or '&json=1' in self.path:
            json_format = True  # Results in format json.
            self.path = self.path.replace('?json=1', '').replace('&json=1', '')  # We eliminate it in order to
            # work always in the same way, but having into account the format

        URLError = False
        contents = ''
        # Message to send back to the client
        if self.path == '/':  # Main page. In this page you will find all the forms
            f = open('form.html', 'r')
            contents = f.read()
            f.close()

        # We start the basic level
        elif self.path == '/listSpecies':  # It returns all the species available in the database
            contents = get_name(json_format)

        elif self.path.startswith('/listSpecies'):  # It returns the number 'limit' of species
            pos = self.path.find('?limit=')  # Find the position of ?limit= in the URL
            if pos == -1 and not json_format:  # If the position is -1 means that ?limit= is not in the URL and
                # since json_format=False, the user wants the results in html format
                URLError = True
            elif pos == -1 and json_format:  # If the position is -1 means that ?limit= is not in the URL and
                # since json_format=True, the user wants the results in json format
                reqError = Error("An error has been produced.")
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
            else:
                txt_limit = self.path[pos+7:]  # Get the limit integer introduced by the user.
                # I add up 7 units to the position because pos returns the position of the first letter (in this case ?)
                # And 7 is the number of characters that ?limit= has.
                contents = get_limit_name(txt_limit, json_format)

        elif self.path.startswith('/karyotype'):  # It returns the name of the chromosomes of a given specie
            # Si no están disponibles los cromosomas de una especie.
            # Quitar la coma del final. MT
            pos = self.path.find('?specie=')  # Find the position of ?specie= in the URL
            if pos == -1 and not json_format:  # If the position is -1 means that ?specie= is not in the URL and
                # since json_format=False the user wants the results in html format
                URLError = True
            elif pos == -1 and json_format:  # If the position is -1 means that ?specie= is not in the URL and
                # since json_format=True the user wants the results in json format
                reqError = Error("An error has been produced.")
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
            else:
                txt_specie = self.path[pos+8:]  # Get the specie introduced by the user
                # I add up 8 units to the position because pos returns the position of the first letter (in this case ?)
                # And 8 is the number of characters that ?specie= has.
                contents = get_karyotype(txt_specie, json_format)

        elif self.path.startswith('/chromosomeLength'):  # It returns the length of a given chromosome
            # Punto al final
            pos_specie = self.path.find('?specie=')  # Find the position of ?specie= in the URL
            pos_chromo = self.path.find('&chromo=')  # Find the position of &chromo= in the URL
            if pos_specie == -1 or pos_chromo == -1 and not json_format:  # If the position is -1 means that ?specie=
                # or &chromo= is not in the URL and since json_format=False the user wants the results in html format
                URLError = True
            elif pos_specie == -1 or pos_chromo == -1 and json_format:   # If the position is -1 means that ?specie=
                # or &chromo= is not in the URL and since json_format=True the user wants the results in json format
                reqError = Error("An error has been produced.")
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
            else:
                specie = self.path[pos_specie+8:pos_chromo]  # Get the specie introduced by the user
                # I add up 8 units to the position because pos_specie returns the position of the first letter
                # (in this case ?) and 8 is the number of characters that ?specie= has.
                chromo = self.path[pos_chromo+8:]  # Get the chromo introduced by the user
                # I add up 8 units to the position because pos_chromo returns the position of the first letter
                # (in this case &) and 8 is the number of characters that &chromo= has.
                contents = get_len_chromo(specie, chromo, json_format)

        # We start with the medium level
        elif self.path.startswith('/geneSeq'):  # It returns the sequence of a given human gene
            # Secuencia en más de una línea
            pos_gene = self.path.find('?gene=')  # Find the position of ?gene= in the URL
            if pos_gene == -1 and not json_format:  # If the position is -1 means that ?gene= is not in the URL and
                # since json_format=False the user wants the results in html format
                URLError = True
            elif pos_gene == -1 and json_format:  # If the position is -1 means that ?gene= is not in the URL and
                # since json_format=True the user wants the results in json format
                reqError = Error("An error has been produced.")
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
            else:
                gene = self.path[pos_gene+6:]  # Get the gene introduced by the user
                # I add up 6 units to the position because pos_gene returns the position of the first letter
                # (in this case ?) and 6 is the number of characters that ?gene= has.
                contents = get_sequence(gene, json_format)

        elif self.path.startswith('/geneInfo'):  # It returns start, end, id, length and chromosome
            # of a given human gene
            pos_gene = self.path.find('?gene=')  # Find the position of ?gene= in the URL
            if pos_gene == -1 and not json_format:  # If the position is -1 means that ?gene= is not in the URL and
                # since json_format=False the user wants the results in html format
                URLError = True
            elif pos_gene == -1 and json_format:  # If the position is -1 means that ?gene= is not in the URL and
                # since json_format=True the user wants the results in json format
                reqError = Error("An error has been produced.")
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
            else:
                gene = self.path[pos_gene+6:]  # Get the gene introduced by the user
                # I add up 6 units to the position because pos_gene returns the position of the first letter
                # (in this case ?) and 6 is the number of characters that ?gene= has.
                contents = get_gene_info(gene, json_format)

        elif self.path.startswith('/geneCalc'):  # It calculates the length and percentage of all the bases
            # of a given human gene
            pos_gene = self.path.find('?gene=')  # Find the position of ?gene= in the URL
            if pos_gene == -1 and not json_format:  # If the position is -1 means that ?gene= is not in the URL and
                # since json_format=False the user wants the results in html format
                URLError = True
            elif pos_gene == -1 and json_format:  # If the position is -1 means that ?gene= is not in the URL and
                # since json_format=True the user wants the results in json format
                reqError = Error("An error has been produced.")
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
            else:
                gene = self.path[pos_gene+6:]  # Get the gene introduced by the user
                Sequence = Seq(get_sequence(gene, False))  # Use the class Seq we create in the first practice
                totA = Sequence.count('A')  # Number of As
                totC = Sequence.count('C')  # Number of Cs
                totG = Sequence.count('G')  # Number of Gs
                totT = Sequence.count('T')  # Number of Ts
                percA = Sequence.perc('A')  # percentage of As
                percC = Sequence.perc('C')  # percentage of Cs
                percG = Sequence.perc('G')  # percentage of Gs
                percT = Sequence.perc('T')  # percentage of Ts
                contents = "The total length of As is {}, the total length of Cs is {}, the total length of Gs is {}," \
                           " the total length of Ts is {}, the percentage of As is {}%, " \
                           "the percentage of Cs is {}%, the percentage of Gs is {}%, " \
                           "and the percentage of Ts is {}%".format(totA, totC, totG, totT, percA, percC, percG, percT)
                if json_format:
                    gene_calcs = Gene_Calculations(totA, totC, totG, totT, percA, percC, percG, percT)
                    contents = json.dumps(gene_calcs, cls=UserEncoder, indent=4)


        elif self.path.startswith('/geneList'):  # It returns the list of all the genes between a given start
            # and a given end position of a given human chromosome
            pos_chromo = self.path.find('?chromo=')  # Find the position of ?chromo= in the URL
            pos_start = self.path.find('&start=')  # Find the position of &start= in the URL
            pos_end = self.path.find('&end=')  # Find the position of &end= in the URL
            if pos_chromo == -1 or pos_start == -1 or pos_end == -1 and not json_format:  # If the position is -1 means
                # that ?chromo= or &start= or &end= is not in the URL
                # and since json_format=False the user wants the results in html format
                URLError = True
            elif pos_chromo == -1 or pos_start == -1 or pos_end == -1 and json_format:  # If the position is -1 means
                # that ?chromo= or &start= or &end= is not in the URL
                # and since json_format=True the user wants the results in json format
                reqError = Error("An error has been produced.")
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
            else:
                chromo = self.path[pos_chromo+8:pos_start]  # Get the Chromosome introduced by the user
                # I add up 8 units to the position because pos_chromo returns the position of the first letter
                # (in this case ?) and 8 is the number of characters that ?chromo= has.
                start = self.path[pos_start+7:pos_end]  # Get the start position introduced by the user
                # I add up 7 units to the position because pos_start returns the position of the first letter
                # (in this case &) and 7 is the number of characters that ?start= has.
                end = self.path[pos_end+5:]  # Get the end position introduced by the user
                # I add up 5 units to the position because pos_end returns the position of the first letter
                # (in this case &) and 5 is the number of characters that ?end= has.
                contents = get_name_genes(chromo, start, end, json_format)

        else:  # Endpoint not valid
            URLError = True

        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        if not json_format:
            # Define the content-type header:
            self.send_header('Content-Type', 'text/html')
            if URLError:
                f = open('error.html', 'r')  # Endpoint not valid
                contents = f.read()
                f.close()
            elif self.path != '/':
                f = open('result.html', 'r')  # Endpoint valid
                contents = f.read().replace("####", contents)
                f.close()

        else:
            # Define the content-type header:
            self.send_header('Content-Type', 'application/json')

        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()

print("")
print("Server Stopped")
