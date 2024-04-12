
if __name__ == '__main__':
    s = 100 # support

    # Read browsing.txt
    with open('browsing.txt') as f:
        transactions = f.readlines()

    # A Priori Algorithm
    # Pass 1: Count the frequency of each item
    ## Items that appear in at least s transactions are frequent
    # Keep only frequent items
    items = {}
    for transaction in transactions:
        for item in transaction.split():
            if item in items:
                items[item] += 1
            else:
                items[item] = 1
    frequent_items = {item: freq for item, freq in items.items() if freq >= s}

    print(len(frequent_items))

    # Pass 2: Read baskets again and keep track of the count of only those pairs where both elements are frequent (from Pass 1)
    item_pairs = {}

    for transaction in transactions:
        basket = transaction.split()
        basket = [item for item in basket if item in frequent_items]
        basket.sort()
        for i in range(len(basket)): # i is the index of the first item
            for j in range(i+1, len(basket)): # j is the index of the second item
                if (basket[j] != basket[i]):
                    #print(basket[i], basket[j])
                    pair = (basket[i], basket[j])
                    if pair in item_pairs:
                        item_pairs[pair] += 1
                    else:
                        item_pairs[pair] = 1
    frequent_item_pairs = {pair: freq for pair, freq in item_pairs.items() if freq >= s}

    print(len(frequent_item_pairs))
    # Top 5 pairs by frequency
    print({pair: freq for pair, freq in sorted(frequent_item_pairs.items(), key=lambda item: item[1], reverse=True)[:5]})

    # Compute confidence scores
    # Conf(X -> Y) = freq(X, Y) / freq(X)
    # Conf(Y -> X) = freq(X, Y) / freq(Y) 
    # Confidence score for each pair of items in frequent_item_pairs
    confidence_scores = {}
    for pair, freq in frequent_item_pairs.items():
        confidence_scores[pair] = freq / frequent_items[pair[0]] # Get the confidence score for X -> Y
        confidence_scores[(pair[1], pair[0])] = freq / frequent_items[pair[1]] # Get the confidence score for Y -> X

    # Sort high to low, show top 5
    print({pair: score for pair, score in sorted(confidence_scores.items(), key=lambda item: item[1], reverse=True)[:5]})

    # Pass 3: Read the baskets again and keep track of the frequency of each triple of items (where all three are frequent)
    item_triples = {}
    for transaction in transactions:
        basket = transaction.split()
        basket = [item for item in basket if item in frequent_items]
        basket.sort()
        for i in range(len(basket)): # i is the index of the first item
            for j in range(i+1, len(basket)): # j is the index of the second item
                for k in range(j+1, len(basket)): # k is the index of the third item
                    if (basket[j] != basket[i]) and (basket[k] != basket[i]) and (basket[k] != basket[j]):
                        triple = (basket[i], basket[j], basket[k])
                        if triple in item_triples:
                            item_triples[triple] += 1
                        else:
                            item_triples[triple] = 1
    frequent_item_triples = {triple: freq for triple, freq in item_triples.items() if freq >= s}

    print({pair: freq for pair, freq in sorted(frequent_item_triples.items(), key=lambda item: item[1], reverse=True)[:5]})

    # Compute confidence scores
    # Conf(X, Y -> Z) = freq(X, Y, Z) / freq(X, Y)
    # Conf(X, Z -> Y) = freq(X, Y, Z) / freq(X, Z)
    # Confidence score for each pair of items in frequent_item_pairs
    confidence_scores = {}
    for triple, freq in frequent_item_triples.items():
        confidence_scores[triple] = freq / frequent_item_pairs[triple[:2]] # Get the confidence score for X, Y -> Z
        confidence_scores[(triple[0], triple[2], triple[1])] = freq / frequent_item_pairs[(triple[0], triple[2])] # Get the confidence score for X, Z -> Y
        confidence_scores[(triple[1], triple[2], triple[0])] = freq / frequent_item_pairs[(triple[1], triple[2])] # Get the confidence score for Y, Z -> X

    # Sort high to low, show top 5
    sorted_confidence_triples = {pair: score for pair, score in sorted(confidence_scores.items(), key=lambda item: item[1], reverse=True)[:5]}

    # Sort by lexicographic order
    print({pair: score for pair, score in sorted(sorted_confidence_triples.items(), key=lambda item: item[0])})