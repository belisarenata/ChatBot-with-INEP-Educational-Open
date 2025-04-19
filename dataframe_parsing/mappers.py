from enums import EducationLevel, EducationSubLevel, Indicator

REGISTRATION_FIELDS = {
    "Região": "region",
    "UF": "state",
    "Código do Município": "city_code",
    "Nome do Município": "city_name",
    "Nome da Escola": "school_name",
    "Localização": "location",
    "Dependência Administrativa": "administrative_dependency", #??
}

EXTENDED_SUB_CLASSES_ELEMENTARY_EDUCATION = [
    EducationSubLevel.TOTAL,
    EducationSubLevel.AI,
    EducationSubLevel.AF,
    EducationSubLevel.A1,
    EducationSubLevel.A2,
    EducationSubLevel.A3,
    EducationSubLevel.A4,
    EducationSubLevel.A5,
    EducationSubLevel.A6,
    EducationSubLevel.A7,
    EducationSubLevel.A8,
    EducationSubLevel.A9,
]

SUB_CLASSES_ELEMENTARY_EDUCATION = [
    EducationSubLevel.TOTAL,
    EducationSubLevel.AI,
    EducationSubLevel.AF,
]

SUB_CLASSES_PRE_SCHOOL_EDUCATION = [
    EducationSubLevel.TOTAL,
    EducationSubLevel.CRECHE,
    EducationSubLevel.PRE,
]

SUB_CLASSES_HIGH_SCHOOL = [
    EducationSubLevel.TOTAL,
    EducationSubLevel.S1,
    EducationSubLevel.S2,
    EducationSubLevel.S3,
    EducationSubLevel.S4,
]

EXTENDED_SUB_CLASSES_HIGH_SCHOOL = SUB_CLASSES_HIGH_SCHOOL + [EducationSubLevel.NS]

INDICATOR_DICTS = {
    Indicator.IRD: {"media"},
    Indicator.DSU: {
        "percentual": {
            EducationLevel.INF: SUB_CLASSES_PRE_SCHOOL_EDUCATION,
            EducationLevel.EF: SUB_CLASSES_ELEMENTARY_EDUCATION,
            EducationLevel.EM: [],
            EducationLevel.EP: [],
            EducationLevel.EJA: [],
            EducationLevel.EE: [],
        }
    },
    Indicator.HAD: {
        "media": {
            EducationLevel.INF: SUB_CLASSES_PRE_SCHOOL_EDUCATION,
            EducationLevel.EF: EXTENDED_SUB_CLASSES_ELEMENTARY_EDUCATION,
            EducationLevel.EM: EXTENDED_SUB_CLASSES_HIGH_SCHOOL,
        }
    },
    Indicator.IED: {
        "indice": {
            EducationLevel.EF: SUB_CLASSES_ELEMENTARY_EDUCATION,
            EducationLevel.EM: [],
        }
    },
    Indicator.ATU: {
        "media": {
            EducationLevel.INF: SUB_CLASSES_PRE_SCHOOL_EDUCATION,
            EducationLevel.EF: EXTENDED_SUB_CLASSES_ELEMENTARY_EDUCATION
            + ["Turmas Multietapa, Multi ou Correção de Fluxo"],
            EducationLevel.EM: EXTENDED_SUB_CLASSES_HIGH_SCHOOL,
        }
    },
    Indicator.INSE: {
        "QTD_ALUNOS_INSE",
        "INSE_VALOR_ABSOLUTO",
        "INSE_CLASSIFICACAO",
    },
    Indicator.TDI: {
        "taxa": {
            EducationLevel.EF: [],
            EducationLevel.EM: SUB_CLASSES_HIGH_SCHOOL,
        }
    },
    Indicator.TNR: {
        "taxa": {
            EducationLevel.EF: EXTENDED_SUB_CLASSES_ELEMENTARY_EDUCATION,
            EducationLevel.EM: EXTENDED_SUB_CLASSES_HIGH_SCHOOL,
        }
    },
    Indicator.REND: {
        "aprovação": {
            EducationLevel.EF: EXTENDED_SUB_CLASSES_ELEMENTARY_EDUCATION,
            EducationLevel.EM: EXTENDED_SUB_CLASSES_HIGH_SCHOOL,
        },
        "reprovação": {
            EducationLevel.EF: EXTENDED_SUB_CLASSES_ELEMENTARY_EDUCATION,
            EducationLevel.EM: EXTENDED_SUB_CLASSES_HIGH_SCHOOL,
        },
        "abandono": {
            EducationLevel.EF: EXTENDED_SUB_CLASSES_ELEMENTARY_EDUCATION,
            EducationLevel.EM: EXTENDED_SUB_CLASSES_HIGH_SCHOOL,
        },
    },
    Indicator.ICG: {"nivel"},
    Indicator.AFD: {
        "nivel": {
            EducationLevel.EF: SUB_CLASSES_ELEMENTARY_EDUCATION,
            EducationLevel.EM: [],
            EducationLevel.EJA: [EducationLevel.EF, EducationLevel.EM],
        }
    },
}

NO_CATEGORICAL_INDICATORS = {Indicator.IED.value: 6, Indicator.AFD.value: 5}

SINGLE_VALUE_INDICATOR = [Indicator.ICG.value, Indicator.IRD.value]

