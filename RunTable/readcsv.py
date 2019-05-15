import os
import csv

included_cols = [0,3,4]

with open('Run_config.txt', 'w') as f:

        with open("RunTableGrid.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                content = list(row[i] for i in included_cols)

                RunNumber = content[0]
                Config = content[1]
                Digitizer = content[2]

                if ("KeySightScope" in Digitizer and "," not in Config):
                            f.write("%s\t" % RunNumber)
                            f.write("%s\n" % Config)
