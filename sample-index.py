def create_index_entry_for(filename):
    position = 0
    index_entry = {}
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            for token in line.split():
                if token not in index_entry:
                    index_entry[token] = []
                index_entry[token].append(position)
                position = position + 1
    return index_entry