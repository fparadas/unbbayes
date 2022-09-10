from unbbayes.unbbayes import UnBBayes

unb = UnBBayes()

net = unb.create_network_from_file("mildew3-2.net")

net = unb.compile_network(net)

unb.print_network(net)


print(" ****** Updating Beliefs ****** ")

net = unb.propagate_evidence(unb.set_evidence(net, [("OQ", "f"), ("OM", "no")]))

unb.print_network(net)