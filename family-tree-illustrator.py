import sys

class Person:
    def __init__(self, name):
        if len(name) == 2:
            self.first_name = name[0]
            self.maiden_name = ""
            self.last_name = name[1]
        elif len(name) == 3:
            self.first_name = name[0]
            self.maiden_name = name[1]
            self.last_name = name[2]

    def __str__(self):
        if self.maiden_name == "":
            return "%s %s" % (self.first_name, self.last_name)
        return "%s %s %s" % (self.first_name, self.maiden_name, self.last_name)
    def __repr__(self):
        if self.maiden_name == "":
            return "%s %s" % (self.first_name, self.last_name)
        return "%s %s %s" % (self.first_name, self.maiden_name, self.last_name)

def main():
    python_script = sys.argv[0]
    input_file = sys.argv[1]
    file_handle = open(input_file, 'r')
    for input_line in file_handle:
        input_line = input_line.strip()
        if input_line == "":
            continue
        person = Person(input_line.split())
        print person
    file_handle.close()

if __name__ == "__main__":
    main()
