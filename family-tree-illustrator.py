import sys
import pydot

gBLUE = "#6599FF"
gPINK = "#FF69B4"
gGRAY = "#D3D3D3"
gDEFAULT = "#FFFFFF"

class Person:
    def __init__(self, person_info):
        names = person_info.split("|")
        
        name = names[0].split()
        father = names[1].split()
        mother = names[2].split()

        self.first_name = name[0]
        if len(name) == 2:
            self.maiden_name = ""
            self.last_name = name[1]
        elif len(name) == 3:
            self.maiden_name = name[1]
            self.last_name = name[2]

        self.father = " ".join(father)
        self.mother = " ".join(mother)

    def name(self):
        if self.maiden_name == "":
            return "%s %s" % (self.first_name, self.last_name)
        return "%s %s %s" % (self.first_name, self.maiden_name, self.last_name)

    def __str__(self):
        return self.name()
    def __repr__(self):
        return self.name()

def PopulatePeople(input_file):
    people = {}
    file_handle = open(input_file, 'r')
    
    current_last_name = ""
    for input_line in file_handle:
        input_line = input_line.strip()
        if input_line == "":
            continue
        person = Person(input_line)
        people[person.name()] = person
    file_handle.close()
    return people

def DisplayPeople(people):
    for person in people:
        print person

def DisplayFamilies(families):
    for family_name, family_members in families.iteritems():
        print "Family: ", family_name
        for family_member in family_members:
            print "  ", family_member
        print ""

def GenerateFamilyTree(people):
    graph = pydot.Dot(graph_type='digraph')
    nodes = {}
    for person in people:
        person_node = pydot.Node(people[person].name(), style="filled", fillcolor=gDEFAULT)
        father_node = pydot.Node(people[person].father, style="filled", fillcolor=gBLUE)
        mother_node = pydot.Node(people[person].mother, style="filled", fillcolor=gPINK)
        graph.add_node(person_node)
        graph.add_node(father_node)
        graph.add_node(mother_node)

        graph.add_edge(pydot.Edge(person_node, father_node, label="", labelfontcolor="#009933", fontsize="10.0", color="blue"))
        graph.add_edge(pydot.Edge(person_node, mother_node, label="", labelfontcolor="#009933", fontsize="10.0", color="blue"))

    graph.write_png("family-tree.png")

def main():
    python_script = sys.argv[0]
    if len(sys.argv) != 2:
        print "### ERROR: unexpected input arguments"
        return
    input_file = sys.argv[1]
    people = PopulatePeople(input_file)
    DisplayPeople(people)
    GenerateFamilyTree(people)

if __name__ == "__main__":
    main()
