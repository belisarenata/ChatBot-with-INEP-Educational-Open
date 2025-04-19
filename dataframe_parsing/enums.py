from enum import Enum


class Indicator(Enum):
    IRD = "Regularidade do Corpo Docente"
    DSU = "Percentual de Docentes com Curso Superior"
    HAD = "Média de Horas-aula diária"
    IED = "Esforço Docente"
    ATU = "Média de Alunos por Turma"
    INSE = "Nível Socioeconômico (Inse)"
    TDI = "Taxas de Distorção Idade-série"
    TNR = "Taxas de Não-resposta (TNR)"
    REND = "Taxas de Rendimento"
    ICG = "Complexidade de Gestão da Escola"
    AFD = "Adequação da Formação Docente"


class EducationLevel(Enum):
    INF = "Educacao Infantil"
    EF = "Ensino Fundamental"
    EM = "Ensino Medio"
    EP = "Educacao Profissional"
    EJA = "Educacao de Jovens e Adultos"
    EE = "Educacao Especial"


class EducationSubLevel(Enum):
    TOTAL = "Total"
    AI = "Anos_Iniciais"
    AF = "Anos_Finais"
    A1 = "1_Ano"
    A2 = "2_Ano"
    A3 = "3_Ano"
    A4 = "4_Ano"
    A5 = "5_Ano"
    A6 = "6_Ano"
    A7 = "7_Ano"
    A8 = "8_Ano"
    A9 = "9 Ano"
    CRECHE = "Creche"
    PRE = "Pre-Escola"
    NS = "Nao-Seriado"
    S1 = "1_serie"
    S2 = "2_serie"
    S3 = "3_serie"
    S4 = "4_serie"


class FKs(Enum):
    SCHOOL_CODE = "Código da Escola"
    YEAR = "Ano"
