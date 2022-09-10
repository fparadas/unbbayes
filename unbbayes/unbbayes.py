from typing import List
from py4j.java_gateway import JavaGateway, is_instance_of
import os
import re

class Network:
    def __init__(self, jNet):
        self.net = jNet
        self.compiled = False

class Node:
    def __init__(self, name: str, parents: List[str], states: List[str], cpt: List[float]):
        self.name = name
        self.parents = parents
        self.states = states
        self.probs = cpt

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class UnBBayes(metaclass=Singleton):

    def __init__(self):

        cwd = os.getcwd()

        unbbayes_path = None
        for filename in os.listdir(os.path.join(cwd, 'unbbayes', 'lib', 'unbbayes')):
            if re.match('unbbayes.*\.jar', filename):
                unbbayes_path = os.path.join(cwd, 'unbbayes', 'lib', 'unbbayes', filename)

        print(unbbayes_path)




        self._gateway = JavaGateway.launch_gateway(classpath=unbbayes_path, die_on_exit=True)
        self._prs = self._gateway.jvm.unbbayes.prs
        self._io = self._gateway.jvm.unbbayes.io

    
    def create_java_node(self, node: Node):
        newNode = self._prs.bn.ProbabilisticNode()

        newNode.setName(node.name)

        for state in node.states:
            newNode.appendState(state)

        aux_cpt = newNode.getProbabilityFunction()
        aux_cpt.addVariable(newNode)

        for i in range(len(node.probs)):
            aux_cpt.addValueAt(i, float(node.probs[i]))
        
        return newNode
    
    def add_node(self, network: Network, node: Node):
        net = network.net
        jNode = self.create_java_node(node)

        for parent in node.parents:
            jParent = net.getNode(parent)
            jNode = net.getNode(node.name)
            net.addEdge(self._prs.Edge(jParent, jNode))

        network.net = net

        return network
    
    def create_network(self, name: str, nodeList: List[Node]):
        net = self._prs.bn.ProbabilisticNetwork(name)

        for node in nodeList:
            jNode = self.create_java_node(node)

            net.addNode(jNode)
        
        for node in nodeList:
            for parent in node.parents:
                jParent = net.getNode(parent)
                jNode = net.getNode(node.name)
                net.addEdge(self._prs.Edge(jParent, jNode))

        return Network(net)
    
    def create_network_from_file(self, path: str):
        file = self._gateway.jvm.java.io.File(path)
        net = self._io.NetIO().load(file)
        return Network(net)

    def save_network(self, path: str, network: Network):
        file = self._gateway.jvm.java.io.File(path)
        self._io.NetIO().save(file, network.net)

    def print_network(self, network: Network):
        net = network.net

        for node in net.getNodes():
            print(node.getName() + ": " + node.getDescription())

            if is_instance_of(self._gateway, node, self._prs.bn.TreeVariable):
                for i in range(node.getStatesSize()):
                    print(node.getStateAt(i) + " : " + str(node.getMarginalAt(i)))
            
                print("----")

    def compile_network(self, network: Network):
        network.compiled = True

        net = network.net

        alg = self._prs.bn.JunctionTreeAlgorithm()
        alg.setNetwork(net)
        alg.run()

        network.net = net

        return network
    
    def set_evidence(self, pyNet: Network, evidences):
        if not pyNet.compiled:
            network = self.compile_network(pyNet)
        else:
            network = pyNet

        net = network.net

        for evidence in evidences:
            findingNode = net.getNode(evidence[0])

            for stateIndex in range(findingNode.getStatesSize()):
                if findingNode.getStateAt(stateIndex) == evidence[1]:
                    findingNode.addFinding(stateIndex)
                    break
        
        return network
    
    def propagate_evidence(self, pyNet: Network):
        if not pyNet.compiled:
            network = self.compile_network(pyNet)
        else:
            network = pyNet
        
        network.net.updateEvidences()

        return network