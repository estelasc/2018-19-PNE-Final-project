# This is the server for the final practice.
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
            json_format = True
            self.path = self.path.replace('?json=1', '').replace('&json=1', '')

        URLError = False
        contents = ''
        # Message to send back to the client
        if self.path == '/':
            f = open('form.html', 'r')
            contents = f.read()
            f.close()

        elif self.path == '/listSpecies':
            contents = get_name(json_format)

        elif self.path.startswith('/listSpecies'):
            pos = self.path.find('?limit=')
            if pos == -1 and not json_format:
                URLError = True
            elif pos == -1 and json_format:
                reqError = Error("An error has been produced.")
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
            else:
                txt_limit = self.path[pos+7:]  # Get the limit integer introduced by the user
                contents = get_limit_name(txt_limit, json_format)

        elif self.path.startswith('/karyotype'):  # Si no están disponibles los cromosomas de una especie.
            # Quitar la coma del final. MT
            pos = self.path.find('?specie=')
            if pos == -1 and not json_format:
                URLError = True
            elif pos == -1 and json_format:
                reqError = Error("texto")
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
            else:
                txt_specie = self.path[pos+8:]  # Get the specie introduced by the user
                contents = get_karyotype(txt_specie, json_format)

        elif self.path.startswith('/chromosomeLength'):
            pos_specie = self.path.find('?specie=')
            pos_chromo = self.path.find('&chromo=')
            if pos_specie == -1 or pos_chromo == -1 and not json_format:
                URLError = True
            elif pos_specie == -1 or pos_chromo == -1 and json_format:
                reqError = Error("texto")
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
            else:
                specie = self.path[pos_specie+8:pos_chromo]  # Get the specie introduced by the user
                chromo = self.path[pos_chromo+8:]  # Get the chromo introduced by the user
                contents = get_len_chromo(specie, chromo, json_format)

        # We start with the medium level
        elif self.path.startswith('/geneSeq'):  # Secuencia en más de una línea
            pos_gene = self.path.find('?gene=')
            if pos_gene == -1 and not json_format:
                URLError = True
            elif pos_gene == -1 and json_format:
                reqError = Error("texto")
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
            else:
                gene = self.path[pos_gene+6:]  # Get the gene introduced by the user
                contents = get_sequence(gene, json_format)

        elif self.path.startswith('/geneInfo'):
            pos_gene = self.path.find('?gene=')
            if pos_gene == -1 and not json_format:
                URLError = True
            elif pos_gene == -1 and json_format:
                reqError = Error("texto")
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
            else:
                gene = self.path[pos_gene+6:]  # Get the gene introduced by the user
                contents = get_gene_info(gene, json_format)

        elif self.path.startswith('/geneCal'):
            pos_gene = self.path.find('?gene=')
            if pos_gene == -1 and not json_format:
                URLError = True
            elif pos_gene == -1 and json_format:
                reqError = Error("texto")
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
            else:
                gene = self.path[pos_gene+6:]  # Get the gene introduced by the user
                Sequence = Seq(get_sequence(gene, False))
                totA = Sequence.count('A')
                totC = Sequence.count('C')
                totG = Sequence.count('G')
                totT = Sequence.count('T')
                percA = Sequence.perc('A')
                percC = Sequence.perc('C')
                percG = Sequence.perc('G')
                percT = Sequence.perc('T')
                contents = "The total length of As is {}, the total length of Cs is {}, the total length of Gs is {}," \
                           " the total length of Ts is {}, the percentage of As is {}%, " \
                           "the percentage of Cs is {}%, the percentage of Gs is {}%, " \
                           "and the percentage of Ts is {}%".format(totA, totC, totG, totT, percA, percC, percG, percT)
                if json_format:
                    gene_calcs = Gene_Calculations(totA, totC, totG, totT, percA, percC, percG, percT)
                    contents = json.dumps(gene_calcs, cls=UserEncoder, indent=4)


        elif self.path.startswith('/geneList'):
            pos_chromo = self.path.find('?chromo=')
            pos_start = self.path.find('&start=')
            pos_end = self.path.find('&end=')
            if pos_chromo == -1 or pos_start == -1 or pos_end == -1 and not json_format:
                URLError = True
            elif pos_chromo == -1 or pos_start == -1 or pos_end == -1 and json_format:
                reqError = Error("texto")
                contents = json.dumps(reqError, cls=UserEncoder, indent=4)
            else:
                chromo = self.path[pos_chromo+8:pos_start]  # Get the Chromosome introduced by the user
                start = self.path[pos_start+7:pos_end]  # Get the start position introduced by the user
                end = self.path[pos_end+5:]  # Get the end position introduced by the user
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
                f = open('result.html', 'r')  # Endpoint not valid
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
