import process as pr

line_relevant_senses = ['cord', 'division', 'formation', 'phone', 'product', 'text']

line_mapping = {103671668: "product",
                106626286: "text",
                107012534: "text",
                107012879: "text",
                104402057: "phone",
                108430203: "formation",
                108430568: "formation",
                105748786: "division",
                103670849: "cord"}

mapping = {"line": {103671668: "product",
                    106626286: "text",
                    107012534: "text",
                    107012879: "text",
                    104402057: "phone",
                    108430203: "formation",
                    108430568: "formation",
                    105748786: "division",
                    103670849: "cord"},
            "hard":{744916: "HARD1",
                    1155354:"HARD2",
                    1150915:"HARD3"},
            "serve":{1095218:"SERVE12",
                    1180351: "SERVE10",
                    568430:  "SERVE2"},
                    1180351: "SERVE6"}

SV_SENSE_MAP = {
    "HARD1": ["difficult.a.01"],    # not easy, requiring great physical or mental
    "HARD2": ["hard.a.02",          # dispassionate
              "difficult.a.01"],
    "HARD3": ["hard.a.03"],         # resisting weight or pressure
    "interest_1": ["interest.n.01"], # readiness to give attention
    "interest_2": ["interest.n.03"], # quality of causing attention to be given to
    "interest_3": ["pastime.n.01"],  # activity, etc. that one gives attention to
    "interest_4": ["sake.n.01"],     # advantage, advancement or favor
    "interest_5": ["interest.n.05"], # a share in a company or business
    "interest_6": ["interest.n.04"], # money paid for the use of money
    "cord": ["line.n.18"],          # something (as a cord or rope) that is long and thin and flexible
    "formation": ["line.n.01","line.n.03"], # a formation of people or things one beside another
    "text": ["line.n.05"],                 # text consisting of a row of words written across a page or computer screen
    "phone": ["telephone_line.n.02"],   # a telephone connection
    "product": ["line.n.22"],       # a particular kind of product or merchandise
    "division": ["line.n.29"],      # a conceptual separation or distinction
    "SERVE12": ["serve.v.02"],       # do duty or hold offices; serve in a specific function
    "SERVE10": ["serve.v.06"], # provide (usually but not necessarily food)
    "SERVE2": ["serve.v.01"],       # serve a purpose, role, or function
    "SERVE6": ["service.v.01"]      # be used by; as of a utility
}


def map_synset_to_sense(target, synset):
    if synset is None:
        return None
    for id in mapping[target].keys():
        if str(id).find(str(synset._offset)) > -1:
            return mapping[target][id]
