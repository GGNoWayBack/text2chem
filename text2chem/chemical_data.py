import os
import json

__filename = os.path.dirname(os.path.realpath(__file__))

pubchem_dictionary = json.loads(open(os.path.join(__filename, "resources/terms_dictionary.json"), encoding="utf8").read())
default_abbreviations = json.loads(open(os.path.join(__filename, "resources/acronyms_dictionary.json"), encoding="utf8").read())
ions_table = json.loads(open(os.path.join(__filename, "resources/ions_dictionary.json"), encoding="utf8").read())

element2name = ions_table.get("elements")
list_of_elements_1 = {el for el in element2name.keys() if len(el) == 1}
list_of_elements_2 = {el for el in element2name.keys() if len(el) == 2}
list_of_elements = list_of_elements_1 | list_of_elements_2
name2element = {v: k for k, v in element2name.items()}

ions = {ion["e_name"] for ion in ions_table.get("anions")}
ions.update({ion["e_name"] for ion in ions_table.get("cations")})

anions = {ion.get("c_name"): {"valency": ion.get("valency"),
                              "e_name": ion.get("e_name"),
                              "n_atoms": ion.get("n_atoms")} for ion in ions_table.get("anions")}

cations = {ion.get("c_name"): {"valency": ion.get("valency"),
                               "e_name": ion.get("e_name"),
                               "n_atoms": ion.get("n_atoms")} for ion in ions_table.get("cations")}
list_of_anions = set(anions.keys())
list_of_cations = set(cations.keys())

species = tuple(sorted([ion.get("e_name")
                        for ion in ions_table.get("anions") if ion.get("e_name") not in ["O2", "S2"]] +
                       [ion.get("e_name") for ion in ions_table.get("cations")] +
                       [e for e in element2name.keys()] +
                       ions_table.get("species") +
                       ions_table["oxyanions"], key=lambda x: len(x), reverse=True))

diatomic_molecules = {"O2", "N2", "H2"}

prefixes2num = {"": 1,
                "mono": 1,
                "di": 2,
                "tri": 3,
                "tetra": 4,
                "pent": 5,
                "penta": 5,
                "hexa": 6,
                "hepta": 7,
                "octa": 8,
                "nano": 9,
                "ennea": 9,
                "nona": 9,
                "deca": 10,
                "undeca": 11,
                "dodeca": 12}

rome2num = {"I": 1,
            "II": 2,
            "III": 3,
            "IV": 4,
            "V": 5,
            "VI": 6,
            "VII": 7,
            "VIII": 8,
            "IX": 9,
            "X": 10}

neg_prefixes = {"an", "de", "non"}

number_to_alphabet_dict = {"specie0_": "A",
                           "specie1_": "B",
                           "specie2_": "C",
                           "specie3_": "Q",
                           "specie4_": "K",
                           "specie5_": "F",
                           "specie6_": "G",
                           "specie7_": "H",
                           "specie8_": "I",
                           "specie9_": "J"}

species_acronyms = {"Ac": "CH3COO",
                    "(ac)": "(CH3COO)",
                    "AC": "CH3COO",
                    "PPh3": "P(C6H5)3",
                    "Ph3P": "P(C6H5)3",
                    "phen": "C12H8N2",
                    "bipy": "(C5H4N)2",
                    "bpy": "(C5H4N)2",
                    "tpy": "C15H11N3",
                    "py": "C5H5N",
                    "bun": "OCH2CH2CH2CH3",
                    "Bun": "OCH2CH2CH2CH3",
                    "Bu": "OCH2CH2CH2CH3"
                    }