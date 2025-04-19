EDUCATIONAL_DATA_CONTEXT = """
As tabelas informadas são o resultado de todas as pesquisas educacionais conduzidas pelo governo brasileiro sobre a educação básica, abrangendo os anos de 2013 a 2023. Os dados incluem informações sobre escolas municipais, estaduais e particulares.

As pesquisas realizadas possuem os seguintes nomes (equivalentes aos nomes das tabelas, com espaços substituídos por "_"):
- Adequação da Formação Docente
- Complexidade de Gestão da Escola
- Esforço Docente
- Média de Alunos por Turma
- Média de Horas-aula Diária
- Percentual de Docentes com Curso Superior
- Regularidade do Corpo Docente
- Taxas de Distorção Idade-Série
- Taxas de Não-resposta (TNR)
- Taxa de Rendimento

Além disso, há uma tabela chamada "registration", que contém os dados cadastrais das escolas. Os campos dessa tabela incluem:
- Código da Escola (SCHOOL_CODE)
- Região do País (region)
- Estado da Federação (state)
- Código da Cidade (city_code)
- Nome da Cidade (city_name)
- Localização (location), indicando se a escola está em zona rural ou urbana
- Dependência Administrativa (administrative_dependency), indicando se a escola é Municipal, Estadual ou Privada
- Ano de criação da escola (YEAR) 
Lembre-se que todos os campos que estão nessa tabela não estão presentes nas outras tabelas, com exceção de school_code
O campo `year` na tabela `registration` indica o ano em que a escola foi criada eincluída na pesquisa educacional pela primeira vez.  
Após a inclusão, a escola permanece registrada nos anos seguintes. O total de escolas de um determinado ano deve considerar todas as escolas criadas anteriormeente.


A chave primária da tabela registration é o campo SCHOOL_CODE, que também é usado como chave estrangeira em todas as demais tabelas.

### Etapas educacionais no Brasil

O sistema educacional brasileiro é dividido nas seguintes etapas e classes:
- Educação Infantil: Creche, Pré-escola
- Ensino Fundamental:
  - Anos Iniciais: 1º ao 5º ano
  - Anos Finais: 6º ao 9º ano
- Ensino Médio: 1ª a 4ª série
- Educação de Jovens e Adultos (EJA): Pode incluir todas as classes do Ensino Fundamental e Ensino Médio
- Educação Profissional
- Educação Especial

### Pesquisas categóricas

As tabelas "Adequação da Formação Docente" e "Esforço Docente" contêm dados categóricos, onde a soma de todas as categorias é sempre 100% para uma mesma combinação de [código da escola, ano, etapa, classe].

#### Adequação da Formação Docente
Classifica os docentes de acordo com sua formação acadêmica:
1. Docentes com licenciatura na mesma disciplina que lecionam ou bacharelado com complementação pedagógica concluída.
2. Docentes com bacharelado na disciplina correspondente, sem licenciatura ou complementação pedagógica.
3. Docentes com licenciatura em área diferente da que leciona ou bacharelado nas disciplinas da base curricular comum com complementação pedagógica em área diferente.
4. Docentes com outra formação superior não incluída nas categorias anteriores.
5. Docentes sem curso superior completo.

#### Esforço Docente
Classifica os docentes com base no número de alunos e carga horária:
- Nível 1: Até 25 alunos, atuando em um único turno, escola e etapa.
- Nível 2: Entre 25 e 150 alunos, atuando em um único turno, escola e etapa.
- Nível 3: Entre 25 e 300 alunos, atuando em um ou dois turnos, em uma única escola e etapa.
- Nível 4: Entre 50 e 400 alunos, atuando em dois turnos, em uma ou duas escolas e duas etapas.
- Nível 5: Mais de 300 alunos, atuando nos três turnos, em duas ou três escolas e em duas ou três etapas.
- Nível 6: Mais de 400 alunos.

### Pesquisas sobre características das escolas

As tabelas "Complexidade de Gestão da Escola" e "Regularidade do Corpo Docente" não são segmentadas por turma ou série, sendo indexadas apenas por [código da escola, ano]. Elas representam características específicas da escola como um todo.

#### Complexidade de Gestão da Escola
Cada escola é classificada em um dos seis níveis a seguir:
- Nível 1: Pequeno porte (até 50 matrículas), operando em um turno e etapa, oferecendo apenas Educação Infantil ou Anos Iniciais.
- Nível 2: Porte entre 50 e 300 matrículas, operando em dois turnos, oferecendo até duas etapas.
- Nível 3: Porte entre 50 e 500 matrículas, operando em dois turnos, oferecendo duas ou três etapas, com Anos Finais como etapa mais elevada.
- Nível 4: Porte entre 150 e 1000 matrículas, operando em dois ou três turnos, oferecendo duas ou três etapas, com Ensino Médio, Educação Profissional ou EJA como etapa mais elevada.
- Nível 5: Porte entre 150 e 1000 matrículas, operando em três turnos, oferecendo duas ou três etapas, com EJA como etapa mais elevada.
- Nível 6: Porte superior a 500 matrículas, operando em três turnos, oferecendo quatro ou mais etapas, com EJA como etapa mais elevada.

### Pesquisas sobre taxas educacionais

A tabela "Taxas de Rendimento" fornece três indicadores para cada [código da escola, ano, etapa, classe]:
- Taxa de Aprovação
- Taxa de Reprovação
- Taxa de Abandono

A soma dessas três taxas é sempre 100%.
"""
