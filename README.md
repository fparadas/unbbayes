# UnBBAyes Python API

Esse projeto implementa uma API em Python para o framework UnBBayes.

O UnBBayes é um framework em Java desenvolvido na UnB que permite modelar e manipular modelos gráficos probabilísticos. O intuito da API em Python é disponibilizar como um pacote de Programação Probabilística para a linguagem.

Autor: Felipe Gomes Paradas
Matricula: 17/0009840

---

## Como rodar os exemplos

Para conseguir rodar o projeto, é necessário, além de uma instalação do SDK Java 8, Python3 e do pip3, instalar as depêndencias do projeto, ou seja, o pacote Py4J. Para isso, basta acessar o terminal da raiz do projeto e rodar o seguinte comando:

```sh
pip3 install requirements.txt
```

Após garantir que a instalação do pacote Py4J foi realizada, basta executar um dos exemplos disponíveis com o comando python3 da raíz do projeto.

```python
python3 <exemplo>
```

---
## Dependências do projeto

Para a execução do projeto, foram utilizados dois principais pacotes. O primeiro, UnBBayes possui a API em Java que será consumida para a disponibilização dos algoritmos e o segundo, o Py4J, que permite realizar chamadas na JVM dentro do código Python.

### UnBBayes

O UnBBayes é um framework para modelos probabilísticos em inteligência artificial desenvolvido dentro da UnB que disponibiliza tanto uma interface gráfica, quanto um sistema de plugins e até mesmo uma interface de programação de aplicativos (API) Java para integração com outros programas desenvolvidos.

#### Modelo de classes

Em sua API, temos acesso as seguintes classes:

![Modelo de classes do UnBBayes](assets/unbbayes.jpg)


- Graph: interface para grafos construídos sob um conjunto de nós e arestas.

- Network: implementação concreta de uma rede genérica. Se uma rede é composta por nós probabilísticos, usar ProbabilisticNetork (uma extensão de Network) seria útil.

- Edge: é a classe que representa uma aresta entre dois nós.Ao modelar a relação como uma classe separada se torna possível usar atributos, permitindo tratamento diferente por outras classes.

- INode: INode: interface para representar um nó genérico.

- ProbabilisticNode: representa um nó probabilístico.

- UtilityNode: um nó de utilidade para Diagramas de Influência (IDs).

- UtilityTable: representa a função de utilidade para IDs (que é representado como uma tabela no UnBBayes)

- DecisionNode: um nó de decisão para IDs.

- IProbabilityFunction: uma interface para objetos que especificam a distribuição de probabilidade de um nó.

- PotentialTable: classe abstrata que representa IProbabilityFunciton em formato de tabela.

- ProbabilisticTabel: tabelas de probabilidade condicional para BNs.

#### Métodos disponíveis

A API do framework UnBBayes disponibiliza diversos métodos para modelos probabilísticos gráficos e é possível dividi-los em duas principais categorias:

- PRS: nesse pacote encontram-se os métodos referentes a computação de modelos probabilísticos gráficos.

- IO: nessa categoria estão os métodos referentes a leitura e escrita de arquivos externos

### Py4J

Py4J é uma ferramente que possibilita que programas em Python sendo executados no interpretador Python acessem, de forma dinâmica, objetos Java em uma Máquina Virtual Java. A ferramenta também permite o acesso inverso, programas Java fazerem chamadas para objetos Python, mas o foco será na primeira funcionalidade.

A bibliotéca não executa o código Python na JVM, o que Py4J usa são conexões em "sockets" para comunicar a JVM com o interpretador Python e, para isso, é necessário implementar uma porta de entrada em Java chamando a bibliotéca e expondo o programa para o interpretador Python.

Esse pacote será utilizado para permitir o consumo da API do UnBBayes em Java dentro do Python. 

---

## Funções desponibilizadas na API Python

A API em Python tem três principais responsabilidades. A primeira é encapsular as interações com a JVM de forma com que o usuário não precise saber quais conexões e chamadas estão sendo feitas, além de garantir que será mantido apenas um processo da JVM rodando e esse processo será terminado ao final do script Python.

Para essa cumprir com essa responsabilidade, é criado uma classe seguindo o padrão de desenho `singleton`, o que consegue garantir apenas uma instância JVM sendo executada por programa Python. Além disso, algumas funções disponibilizadas pelo próprio Py4J cuidam do desligamento do processo ao final.

```python
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
```

Sua segunda responsabilidade é disponibilizar classes objetos para que os usuários consigam representar os nós e suas redes com maior facilidade. São implementadas duas classes simples para isso, Node e Network.

```python
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
```


E, por fim, sua terceira responsabilidade é fornecer funções para o programador realizar as computações dos modelos sem precisar se importar com a implementação. As seguintes funções são disponibilizadas:


- create_java_node
    ```python
    def create_java_node(self, node: Node)
    ```

    Aceita um nó Python como entrada, cria seu equivalente na JVM e retorna essa referência.

- add_node
    ```python
    def add_node(self, network: Network, node: Node)
    ```

    Aceita como entrada um nó e uma rede, adiciona o nó a esta rede e a retorna.


- create_network
    ```python
    def create_network(self, name: str, nodeList: List[Node])
    ```

    Aceita como entrada o nome da rede e uma lista de nós, cria uma rede baseada baseada na lista de nós e a retorna.

- create_network_from_file
    ```python
    def create_network_from_file(self, path: str)
    ```

    Aceita como entrada o caminho para um arquivo `.net`, cria uma rede a partir dele e a retorna.

- save_network
    ```python
    def save_network(self, path: str, network: Network)
    ```

    Aceita como entrada o caminho onde a rede será salva e a rede em si. Salva a rede no formato `.net` no caminho especificado.

- print_network
    ```python
    def print_network(self, network: Network)
    ```

    Imprime no terminal a rede passada como entrada.

- compile_network
    ```python
    def compile_network(self, network: Network)
    ```

    Compila a rede passada como entrada.

- set_evidence
    ```python
    def set_evidence(self, pyNet: Network, evidences)
    ```

    A partir das novas evidências passadas como entrada, atualiza as probabilidades presentes na rede passada como entrada.

- propagate_evidence
    ```python
    def propagate_evidence(self, pyNet: Network)
    ```

    Propaga as evidências que foram atualizadas na rede passada como entrada.

---

## Modelos exemplos

---

## Referências


[1] [UnBBayes](http://unbbayes.sourceforge.net/)

[2] [Py4J](https://www.py4j.org/)