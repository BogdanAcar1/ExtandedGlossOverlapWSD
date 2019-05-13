
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

mapping = {"line": line_mapping}

def map_synset_to_sense(target, synset):
    if synset is None:
        return None
    for id in mapping[target].keys():
        if str(id).find(str(synset._offset)) > -1:
            return mapping[target][id]
