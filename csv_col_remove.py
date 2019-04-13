import argparse
import csv

def parse_arguments():
    # initialize argumentparser and arguments
    parser = argparse.ArgumentParser(description='Takes a csv file and a tablename and creates an SQL insert statement')
    parser.add_argument('csvFile', type=argparse.FileType('r'), help='The CSV file to be read')

    # parse arguments
    args = parser.parse_args()
    return args

def write_row(file_name, row):
    with open(file_name, 'a', newline='') as csvOut:
        writer = csv.writer(csvOut)
        writer.writerow(row)
    csvOut.close()


def main():
    args = parse_arguments()

    in_file_name = args.csvFile.name
    out_file_name = in_file_name.split(".")[0] + "_striped." + in_file_name.split(".")[1]

    with open(out_file_name, 'w') as csvOut:
        pass
    csvOut.close()

    s = []
    with open(in_file_name, 'r') as csvIn:
        reader = csv.reader(csvIn)
        head = next(reader)

        removed = []
        i, size = 0, len(head)
        print("Decide which columns would you like to remove.")
        while (i+len(removed) < size):
            user_input = input("You removed " + str(len(removed)) + " columns. Would you like to remove " + head[i] + " (y to remove, n to keep or a to rename column, q to end removing): ")
            if user_input == "y":
                removed.append(head.index(head[i]))
                head.remove(head[i])
            elif user_input == "n":
                i += 1
            elif user_input == "a":
                new_name = ""
                while new_name == "":
                    new_name = input("Colum new name: ")
                print("Column {} renamed to {}.".format(head[i], new_name))
                head[i] = new_name
                i += 1
            elif user_input == "q":
                break
        print("Please wait untill program is finished removing.")

        counter = 0
        write_row(out_file_name, head)
        for row in reader:
            for idx in removed:
                row.pop(idx)
            write_row(out_file_name, [l.replace('"', '') for l in row])
            counter += 1
            if (counter % 10000 == 0):
                print("Fast update (still not finished). {} rows changed".format(counter))
    csvIn.close()
    print("Program finished. {} rows changed".format(counter+1))
                

main()
