# Gerador de provas em Latex (LatexExamGenerator)
O gerador de provas é uma ferramenta para auxiliar a geração de provas customizadas e individuais por aluno.
O prof. tem em suas mãos uma ferramenta capaz de receber um conjunto de questões pré-definidas e transformá-las em avaliações individuais facilitando o processo de geração de edição e prepararação para impressão.
### Funcionalidades:
 - Gerador de provas automatizados
 - Provas individuais por alunos
 - Gabarito individualizado por prova
 - Gerar o embaralhamento aleatório do gabarito por questão
 - Gerar o embaralhamento aleatório das questões por prova

# Como funciona?
O programa funciona utilizando um **template/modelo** do documento, uma das vantagens da linguagem de edição de texto Latex.
O processo:
 - Gerar uma folha de rosto
 - Definir quantas questões a prova irá conter
 - Inserir as questões na estrutura de diretórios
 - Incluir um arquivo com o nome dos alunos
 - Executar o programa main.py no diretório do **template**
 
# Resultado 
Como resultado obteremos um novo diretório criado junto com a estrutura do **template** chamado build. Isso garante que antes do produto final a ser realizado o prof. tenha oportunidade de conferir o gabarito, número de provas.
Pode-se observar que cada prova gerada, contém a estrutura número_nome_do_aluno, o que facilita a identificação e a estrutura gerada pelo programa principal main.py. 
Cada vez que o programa main.py for executado a pasta build será inteiramente refeita e cada uma das provas criadas terá uma nova estrutura.

# A estrutura
template/exam.tex (Folha de rosto da prova)
template/alunos.txt (Alunos participantes)
template/Makefile (Ferramenta de ajuda na compilação do exam.text)
template/question.X/ (Cada questão da prova)

# Como gerar o diretório build?
Para gerar o diretório build basta executar o comando:
```sh
cd template
python2 ../main.py
```

Ou seja, executar o programa main.py dentro do diretório template.
Depois de executar o programa o diretório build vai conter todas as provas prontas para serem geradas individualmente.

# Script.sh
Dentro do diretório build é possível encontrar o arquivo script.sh que é responsável por gerar as provas no formato PDF e também incluir cada uma das provas para um formato ZIP, chamado provas.zip . O arquivo provas.zip já está no melhor formato para ser compartilhado, ou transportado até a impressora.

# Como corrigir as provas?
Todas as provas são diferentes, mas para cada prova existe um arquivo chamado assinatura, que representa o gabarito para cada prova.
Exemplo de uso para correção de prova:

[![N|Solid](https://raw.githubusercontent.com/marc-queiroz/LatexExamGenerator/master/assinatura.png)](Exemplo)

# Conclusão
Com a geração de provas personalizadas utilizando Latex procura-se diminuir a fricção em termos de edição, melhorias incrementais, adição de biblioteca de questões, tudo isso aliado a facilidade de gerar novas provas.
No dia a dia também é possível salvar cada uma das provas e criar um repositório para cada uma de suas provas, sem o risco de perder qualquer informação.
