
import http.client
import json



PORT = 8000
SERVER = 'localhost'

# Connect with the server
conn = http.client.HTTPConnection(SERVER, PORT)
headers = {'Content-type': 'text/plain'}

print('MENU')
print('Available options:')
print('1. Name of all the species available in the database. You can introduce a limit.')
print('2. Name of all the chromosomes of a given specie.')
print('3. Length of a given chromosome of a given specie.')
print('4. Sequence of a given human gene.')
print('5. Start and end positions, id, length, and the chromosome to which a given human gene belongs.')
print('6. Length and percentage of all the bases of a given gene.')
print('7. Name of the genes located between two given positions of a given chromosome.')
print('8. Exit.')



while True:
    try:
        option = int(input('--Type one of the available options of the MENU: '))
        if option < 0 or option > 9:
            print('The option requested is not available.')
        else:
            if option == 1:
                while True:
                    limit = input('-Introduce a limit or leave it empty: ')
                    if limit == '':
                        conn.request("GET", "/listSpecies?json=1")
                    else:
                        conn.request("GET", "/listSpecies?limit=" + limit + "&json=1")

                    r1 = conn.getresponse()
                    data1 = r1.read().decode("utf-8")
                    listSpecies = json.loads(data1)
                    if not listSpecies.get("ErrorDescription"):
                        print("result: " + str(listSpecies['Species']))
                        break
                    else:
                        print(listSpecies['ErrorDescription'])

            elif option == 2:
                while True:
                    specie = input('Introduce a specie: ')
                    conn.request('GET', "/karyotype?specie=" + specie + "&json=1")
                    r1 = conn.getresponse()
                    data1 = r1.read().decode("utf-8")
                    Chromosomes = json.loads(data1)
                    if not Chromosomes.get("ErrorDescription"):
                        print("result: " + str(Chromosomes['Chromosomes']))
                        break
                    else:
                        print(Chromosomes['ErrorDescription'])

            elif option == 3:
                while True:
                    specie = input('Introduce a specie: ')
                    chromo = input('Introduce a chromosome available for the specie introduced: ')
                    conn.request("GET", "/chromosomeLength?specie=" + specie + "&chromo=" + chromo + "&json=1")
                    r1 = conn.getresponse()
                    data1 = r1.read().decode("utf-8")
                    length_chromo = json.loads(data1)
                    if not length_chromo.get("ErrorDescription"):
                        print("result: " + str(length_chromo["Length"]))
                        break
                    else:
                        print(length_chromo['ErrorDescription'])

            elif option == 4:
                while True:
                    gene = input('Introduce a human gene: ')
                    conn.request("GET", "/geneSeq?gene=" + gene + "&json=1")
                    r1 = conn.getresponse()
                    data1 = r1.read().decode("utf-8")
                    seq_gene = json.loads(data1)
                    if not seq_gene.get("ErrorDescription"):
                        print("result: " + seq_gene["Sequence"])
                        break
                    else:
                        print(seq_gene['ErrorDescription'])

            elif option == 5:
                while True:
                    gene = input('Introduce a human gene: ')
                    conn.request("GET", "/geneInfo?gene=" + gene + "&json=1")
                    r1 = conn.getresponse()
                    data1 = r1.read().decode("utf-8")
                    gene_data = json.loads(data1)
                    if not gene_data.get("ErrorDescription"):
                        print("Result: " + "Start: " + str(gene_data["Start"]) + " End: " + str(gene_data["End"]) +
                                " Length: " + str(gene_data["Length"]) + " Id: " + gene_data["Id"] +
                                " Chromosome: " + gene_data["Chromosome"])
                        break
                    else:
                        print(gene_data['ErrorDescription'])

            elif option == 6:
                while True:
                    gene = input('Introduce a human gene: ')
                    conn.request("GET", "/geneCal?gene=" + gene + "&json=1")
                    r1 = conn.getresponse()
                    data1 = r1.read().decode("utf-8")
                    calc_gene = json.loads(data1)
                    if not calc_gene.get("ErrorDescription"):
                        print("Result: " + "Number of As: " + str(calc_gene["LengthA"]) +
                                " Number of Cs: " + str(calc_gene["LengthC"]) +
                                " Number of G: " + str(calc_gene["LengthG"]) + " Number of T: " +
                                str(calc_gene["LengthT"]) + " Perc of A: " + str(calc_gene["PercA"]) +
                                " Perc of Cs: " + str(calc_gene["PercC"]) +
                                " perc of G: " + str(calc_gene["PercG"]) + " Perc of T: " + str(calc_gene["PercT"]))
                        break
                    else:
                        print(calc_gene['ErrorDescription'])

            elif option == 7:
                while True:
                    chromo = input('Introduce a human chromosome: ')
                    start = input('Introduce the start position: ')
                    end = input('Introduce the end position: ')
                    conn.request("GET", "/geneList?chromo=" + chromo + "&start=" + start + "&end=" + end + "&json=1")
                    r1 = conn.getresponse()
                    data1 = r1.read().decode("utf-8")
                    gene_names = json.loads(data1)
                    if not gene_names.get("ErrorDescription"):
                        print("Result: " + str(gene_names["Genes"]))
                        break
                    else:
                        print(gene_names['ErrorDescription'])

            elif option == 8:
                break

    except ValueError:
        print('The option introduced is not an integer.')
    except:
        print("An error has been produced")
