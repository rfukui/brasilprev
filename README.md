# teste_brasilprev
Escrito em python3
utilização do programa em python
```
$./main.py
```
executa o programa gerando a saida para o terminal
para executar para o simulador, é possivel preencher conforme o exemplo a abaixo quando um valor não é passado, o valor default proposto é executado, nenhum parametro é necessário.
```
./main.py <qtd_simulacao> <qtd_turnos> <qtd_propriedades> <montante_inicial> <valor_minimo_propriedade> <valor_maximo_propriedade> <percentual_aluguel><qtd_ganha_por_volta>
```
Para ajuda, use: 
```
$./main.py --help ou help ou ?
```

# premissas
para a criação das propriedades foi utilizado um gerador de propriedade. O gerador utiliza a seguinte lógica:

 - Todas as propriedades tem o valor variando entre um valor mínimo(definido em 50) e um valor máximo(definodo em 500).
 - Todos os alugueis são baseados em um percentual(25%) do valor do imóvel (no banco imobiliário o valor é de aproximadamente 9%).
 - A ordem das propriedades não alteradas a cada nova jogada.

A ordem dos jogadores é randomizada a cada nova partida.
