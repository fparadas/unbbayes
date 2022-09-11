from unbbayes.unbbayes import UnBBayes

unb = UnBBayes()

net = unb.create_network_from_file("examples/asia.net")

net = unb.compile_network(net)

unb.print_network(net)


print(" ****** Updating Beliefs ****** ")

net = unb.propagate_evidence(unb.set_evidence(net, [("D", "yes"), ("S", "no")]))

unb.print_network(net)