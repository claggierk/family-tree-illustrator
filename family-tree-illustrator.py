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

def DeduceChildren(people):
    children = {}
    parents = {}
    for outer_person in people:
        is_child = True
        for inner_person in people:
            if people[outer_person].name() == people[inner_person].father or people[outer_person].name() == people[inner_person].mother:
                is_child = False
                parents[outer_person] = people[outer_person]
                break
        if is_child:
            children[outer_person] = people[outer_person]
    return parents, children

def GenerateFamilyTree(people):
    graph = pydot.Dot(graph_name='FamilyTree', graph_type='graph', defaultdist='5')#, ranksep='10', size="7.75,10.25")#, overlap='false')
    graph.set_edge_defaults(color="black", len='1.0', margin='1.0')#, weight="20")#, len='2')

    parents, children = DeduceChildren(people)
    nodes = {}
    edges = []
    print "Absolute children:"
    for child in children:
        print "   ", child
        me_node = pydot.Node(children[child].name(), style="filled", fillcolor=gDEFAULT)
        father_node = pydot.Node(children[child].father, style="filled", fillcolor=gBLUE)
        mother_node = pydot.Node(children[child].mother, style="filled", fillcolor=gPINK)
        nodes[children[child].name()] = pydot.Node(children[child].name(), style="filled", fillcolor=gDEFAULT)
        nodes[children[child].father] = pydot.Node(children[child].father, style="filled", fillcolor=gBLUE)
        nodes[children[child].mother] = pydot.Node(children[child].mother, style="filled", fillcolor=gPINK)
        edges.append(pydot.Edge(nodes[children[child].name()], nodes[children[child].father]))
        edges.append(pydot.Edge(nodes[children[child].name()], nodes[children[child].mother]))
    
    print "Parents:"
    for parent in parents:
        print "   ", parent
        me_node = ""
        if parents[parent].name() in nodes:
            me_node = nodes[parents[parent].name()]
        else:
            print "### ERROR: this node should already exist..."
        if parents[parent].father not in nodes:
            nodes[parents[parent].father] = pydot.Node(parents[parent].father, style="filled", fillcolor=gBLUE)
        if parents[parent].mother not in nodes:
            nodes[parents[parent].mother] = pydot.Node(parents[parent].mother, style="filled", fillcolor=gPINK)
        edges.append(pydot.Edge(me_node, nodes[parents[parent].father]))
        edges.append(pydot.Edge(me_node, nodes[parents[parent].mother]))
    
    for node in nodes:
        graph.add_node(nodes[node])
    for edge in edges:
        graph.add_edge(edge)
    
    graph.write_png("family-tree.png", prog='fdp')
    # prog=circo|dot|neato|fdp|sfdp|twopi

def main():
    python_script = sys.argv[0]
    if len(sys.argv) != 2:
        print "### ERROR: unexpected input arguments"
        return
    input_file = sys.argv[1]
    people = PopulatePeople(input_file)
    GenerateFamilyTree(people)

if __name__ == "__main__":
    main()
