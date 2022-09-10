from py4j.java_gateway import JavaGateway, is_instance_of
import os
import re


cwd = os.getcwd()

unbbayes_path = None
for filename in os.listdir(os.path.join(cwd, 'lib', 'unbbayes')):
    if re.match('unbbayes.*\.jar', filename):
        unbbayes_path = os.path.join(cwd, 'lib', 'unbbayes', filename)

print(unbbayes_path)




gateway = JavaGateway.launch_gateway(classpath=unbbayes_path, die_on_exit=True)
prs = gateway.jvm.unbbayes.prs
io = gateway.jvm.unbbayes.io

asiaFile = gateway.jvm.java.io.File("asia.net")

net = io.NetIO().load(asiaFile)

newNode = prs.bn.ProbabilisticNode()

newNode.setName("K")
newNode.setDescription("A test node")
newNode.appendState("yes")
newNode.appendState("no")

aux_cpt = newNode.getProbabilityFunction()

aux_cpt.addVariable(newNode)
net.addNode(newNode)

asiaNode = net.getNode("A")
net.addEdge(prs.Edge(asiaNode, newNode))

aux_cpt.addValueAt(0, 0.99)
aux_cpt.addValueAt(1, 0.01)
aux_cpt.addValueAt(2, 0.1)
aux_cpt.addValueAt(3, 0.9)

#Compiling the network
alg = prs.bn.JunctionTreeAlgorithm()

alg.setNetwork(net)
alg.run()

#print nodes initial probabilities
for node in net.getNodes():
    print(node.getDescription())

    for i in range(node.getStatesSize()):
        print(node.getStateAt(i) + " : " + str(node.getMarginalAt(i)))


findingNode = net.getNode("A")
findingNode.addFinding(0)
likelihood = gateway.new_array(gateway.jvm.float, newNode.getStatesSize())

likelihood[0] = 1.0
likelihood[1] = 0.8

newNode.addLikeliHood(likelihood)

net.updateEvidences()

print(" **** Updated **** ")
for node in net.getNodes():
    print(node.getDescription())

    for i in range(node.getStatesSize()):
        print(node.getStateAt(i) + " : " + str(node.getMarginalAt(i)))

