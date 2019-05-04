# Client for the advanced level of the final project
import http.client
import json


PORT = 8000
SERVER = 'localhost'

# Connect with the server
conn = http.client.HTTPConnection(SERVER, PORT)

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
        option = int(input('\n--Type one of the available options of the MENU: '))
        if option < 0 or option > 9:
            print('The option requested is not available.')  # The option is an integer, but not a valid one
        else:
            if option == 1:  # Option 1 selected
                while True:
                    limit = input('-Introduce a limit or leave it empty: ')  # Asking for the limit
                    if limit == '':
                        conn.request("GET", "/listSpecies?json=1")  # Connecting with server.py
                        # All species available in the database
                    else:
                        conn.request("GET", "/listSpecies?limit=" + limit + "&json=1")  # Connecting with server.py

                    r1 = conn.getresponse()
                    data1 = r1.read().decode("utf-8")  # Decode the data
                    listSpecies = json.loads(data1)  # Get the data
                    if not listSpecies.get("ErrorDescription"):
                        print("RESULT:\n" + ', '.join(listSpecies['Species']) + '.')  # All went well
                        break
                    else:
                        print(listSpecies['ErrorDescription'])  # An error has been produced

            elif option == 2:  # Option 2 was selected
                while True:
                    specie = input('-Introduce a specie: ')  # Asking for a specie
                    conn.request('GET', "/karyotype?specie=" + specie + "&json=1")  # Connecting with server.py
                    r1 = conn.getresponse()
                    data1 = r1.read().decode("utf-8")  # Decode the data
                    Chromosomes = json.loads(data1)  # Get the data
                    if not Chromosomes.get("ErrorDescription"):
                        print("RESULT:\n" + ', '.join(Chromosomes['Chromosomes']) + '.')  # All went well
                        break
                    else:
                        print(Chromosomes['ErrorDescription'])  # An error has been produced

            elif option == 3:
                while True:
                    specie = input('-Introduce a specie: ')  # Asking for a specie
                    # Asking for a chromo
                    chromo = input('-Introduce a chromosome available for the specie introduced: ')
                    # Connecting with server.py
                    conn.request("GET", "/chromosomeLength?specie=" + specie + "&chromo=" + chromo + "&json=1")
                    r1 = conn.getresponse()
                    data1 = r1.read().decode("utf-8")  # Decode the data
                    length_chromo = json.loads(data1)  # Get the data
                    if not length_chromo.get("ErrorDescription"):
                        print("RESULT:\n" + str(length_chromo["Length"]))  # All went well
                        break
                    else:
                        print(length_chromo['ErrorDescription'])  # An error has been produced

            elif option == 4:  # Option 4 selected
                while True:
                    gene = input('-Introduce a human gene: ')  # Asking for a gene
                    conn.request("GET", "/geneSeq?gene=" + gene + "&json=1")  # Connecting with server.py
                    r1 = conn.getresponse()
                    data1 = r1.read().decode("utf-8")  # Decode the data
                    seq_gene = json.loads(data1)  # Get the data
                    if not seq_gene.get("ErrorDescription"):
                        print("RESULT:\n" + seq_gene["Sequence"])  # All went well
                        break
                    else:
                        print(seq_gene['ErrorDescription'])  # An error has been produced

            elif option == 5:  # Option 5 selected
                while True:
                    gene = input('-Introduce a human gene: ')  # Asking for a gene
                    conn.request("GET", "/geneInfo?gene=" + gene + "&json=1")  # Connecting with server.py
                    r1 = conn.getresponse()
                    data1 = r1.read().decode("utf-8")  # Decode the data
                    gene_data = json.loads(data1)  # Get the data
                    if not gene_data.get("ErrorDescription"):
                        print("Start: " + str(gene_data["Start"]) + "\nEnd: " + str(gene_data["End"]) +
                                "\nLength: " + str(gene_data["Length"]) + "\nId: " + gene_data["Id"] +
                                "\nChromosome: " + gene_data["Chromosome"])  # All went well
                        break
                    else:
                        print(gene_data['ErrorDescription'])  # An error has been produced

            elif option == 6:  # Option 6 selected
                while True:
                    gene = input('-Introduce a human gene: ')  # Asking for a gene
                    conn.request("GET", "/geneCalc?gene=" + gene + "&json=1")  # Connecting with server.py
                    r1 = conn.getresponse()
                    data1 = r1.read().decode("utf-8")  # Decode the data
                    calc_gene = json.loads(data1)  # Get the data
                    if not calc_gene.get("ErrorDescription"):
                        # All went well
                        print("Number of As: " + str(calc_gene["LengthA"]) +
                                "\nNumber of Cs: " + str(calc_gene["LengthC"]) +
                                "\nNumber of G: " + str(calc_gene["LengthG"]) + "\nNumber of T: " +
                                str(calc_gene["LengthT"]) + "\nPerc of A: " + str(calc_gene["PercA"]) +
                                "\nPerc of Cs: " + str(calc_gene["PercC"]) +
                                "\nperc of G: " + str(calc_gene["PercG"]) + "\nPerc of T: " + str(calc_gene["PercT"]))
                        break
                    else:
                        print(calc_gene['ErrorDescription'])  # An error has been produced

            elif option == 7:  # Option 7 selected
                while True:
                    chromo = input('-Introduce a human chromosome: ')  # Asking for a chromo
                    start = input('-Introduce the start position: ')  # Asking for a start position
                    end = input('-Introduce the end position: ')  # Asking for an end position
                    # Connecting with server.py
                    conn.request("GET", "/geneList?chromo=" + chromo + "&start=" + start + "&end=" + end + "&json=1")
                    r1 = conn.getresponse()
                    data1 = r1.read().decode("utf-8")  # Decode the data
                    gene_names = json.loads(data1)  # Get the data
                    if not gene_names.get("ErrorDescription"):
                        print("RESULT:\n" + ', '.join(gene_names["Genes"]))  # All went well
                        break
                    else:
                        print(gene_names['ErrorDescription'])  # An error has been produced

            elif option == 8:  # Option 8 selected
                break  # Bye-bye

    except KeyboardInterrupt:
        print('\n\nClient stopped by the user')
        break
    except ValueError:
        print('The option introduced is not an integer.')
    except http.client.HTTPException:
        print("An error with the connection with the server has been produced")
    except:
        print("An error has been produced")
