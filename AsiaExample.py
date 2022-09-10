from unbbayes.unbbayes import Node, UnBBayes

unb = UnBBayes()
unb2 = UnBBayes()

nodeList = [
    Node(name="asia", parents=[], states=["yes", "no"], cpt=[0.01, 0.99]),
    Node(name="tub", parents=["asia"], states=["yes", "no"], cpt=[0.05, 0.95, 0.01, 0.99]),
    Node(name="smoke", parents=[], states=["yes", "no"], cpt=[0.5,0.5]),
    Node(name="lung", parents=["smoke"], states=["yes", "no"], cpt=[0.1, 0.9, 0.01, 0.99]),
    Node(name="bronc", parents=["smoke"], states=["yes", "no"], cpt=[0.6, 0.4, 0.3, 0.7]),
    Node(name="either", parents=["lung", "tub"], states=["yes", "no"], cpt=[1,0,1,0,1,0,0,1]),
    Node(name="xray", parents=["either"], states=["yes", "no"], cpt=[0.98, 0.02, 0.05, 0.95]),
    Node(name="dysp", parents=["bronc", "either"], states=["yes", "no"], cpt=[0.9, 0.1, 0.7, 0.3, 0.8, 0.2, 0.1, 0.9]),
]

net = unb.createNetwork("Asia.net", nodeList)

net = unb.compileNetwork(net)

unb.print_network(net)

net = unb.propagateEvidence(unb.setEvidence(net, [("dysp", "yes"), ("smoke", "no")]))

print(" ****** Updating Beliefs ****** ")
unb.print_network(net)