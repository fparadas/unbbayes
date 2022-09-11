from unbbayes.unbbayes import Node, UnBBayes

unb = UnBBayes()

nodeList = [
    Node(name="Inf", parents=[], states=["yes", "no"], probs=[0.01, 0.99]),
    Node(name="LW", parents=["Inf"], states=["yes", "no"], probs=[0.05, 0.95, 0.01, 0.99]),
    Node(name="Fe", parents=["Inf"], states=["yes", "no"], probs=[0.01, 0.99, 0.01, 0.99]),
    Node(name="Co", parents=["Inf"], states=["yes", "no"], probs=[0.01, 0.99, 0.01, 0.99]),
    Node(name="SB", parents=["Inf"], states=["yes", "no"], probs=[0.01, 0.99, 0.05, 0.95]),
    Node(name="He", parents=["Inf"], states=["yes", "no"], probs=[0.02, 0.98, 0.01, 0.99]),
    Node(name="ST", parents=["Inf"], states=["yes", "no"], probs=[0.02, 0.98, 0.01, 0.99]),
    Node(name="Na", parents=["Inf"], states=["yes", "no"], probs=[0.02, 0.98, 0.01, 0.99]),
    Node(name="Vo", parents=["Inf"], states=["yes", "no"], probs=[0.02, 0.98, 0.01, 0.99]),
    Node(name="Di", parents=["Inf"], states=["yes", "no"], probs=[0.02, 0.98, 0.01, 0.99]),
    Node(name="CRF", parents=["Inf"], states=["yes", "no"], probs=[0.02, 0.98, 0.01, 0.99]),
    Node(name="IP", parents=["Inf"], states=["yes", "no"], probs=[0.02, 0.98, 0.01, 0.99]),
    Node(name="HF", parents=["Inf"], states=["yes", "no"], probs=[0.02, 0.98, 0.01, 0.99]),
    Node(name="COM", parents=["Inf"], states=["yes", "no"], probs=[0.05, 0.95, 0.01, 0.99]),
]

net = unb.create_network("COVID19.net", nodeList)

net = unb.compile_network(net)

unb.print_network(net)

net = unb.propagate_evidence(unb.set_evidence(net, [
    ("COM", "no"),
    ("Fe", "yes"),
    ("SB", "yes"),
    ("LW", "no"),
    ("Na", "yes"),
    ("Vo", "no")
    ]))

print(" ****** Updating Beliefs ****** ")
unb.print_network(net)