import argparse
import csv

def parse_arguments():
    parser = argparse.ArgumentParser(description='Takes a csv file and splits it in multiple smaller tables')
    parser.add_argument('csvFile', type=argparse.FileType('r'), help='The CSV file to be read')
    parser.add_argument('-n', dest='table_count', help='Number of tables to be created', required=True)

    args = parser.parse_args()
    return args

def createFile(file_name, header):
    with open(file_name, 'w') as csvOut:
        writer = csv.writer(csvOut)
        writer.writerow(header)
    csvOut.close()

def writeRow(file_name, row):
    with open(file_name, 'a', newline='') as csvOut:
        writer = csv.writer(csvOut)
        writer.writerow(row)
    csvOut.close()


def main():
    args = parse_arguments()

    in_file_name = args.csvFile.name
    table_count = int(args.table_count)
    files = [str(in_file_name.split(".")[0] + "_split" + str(i+1) + "." + in_file_name.split(".")[1]) for i in range(table_count)]

    with open(in_file_name, 'r') as csvIn:
        reader = csv.reader(csvIn)
        head = next(reader)
        if (table_count > len(head)):
            return
        s = []
        idxs = [i+1 for i in range(len(head))]

        print("Select where will columns be placed. Each column can be placed in multiple tables.\n")
        [print (str(i+1) + ". " + head[i]) for i in range(len(head))]
        print()
        for i in range(table_count):
            user_input = input("Type columns to separate (separated only by space): ").split(" ")
            user_input = [int(int(t)-1) for t in user_input]
            user_input = list(set(user_input))

            validate = sum(int(elem <= len(head) and elem >= 0) for elem in user_input)
            if (validate !=  len(user_input)):
                print("Wrong input! Please try again.")
                i -= 1
            else:
                s.append(user_input)
                idxs = [t for t in idxs if t not in user_input]

        for i in range(table_count):
            print(str(i+1) + ". table contains: " + ", ".join([head[t] for t in s[i]]))

        counter = 0
        for i in range(table_count):
            createFile(files[i], [head[j] for j in s[i]])

        for row in reader:
            for i in range(table_count):
                out = [row[j] for j in s[i]]
                writeRow(files[i], out)
    csvIn.close()
                

if __name__ == "__main__":
    main()
