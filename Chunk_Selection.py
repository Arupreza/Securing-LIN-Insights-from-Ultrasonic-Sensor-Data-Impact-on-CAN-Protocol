import ruptures as rpt
from collections import Counter
from scipy.stats import entropy


# Function for automated chunk selection
def evaluate_chunks_num(data, method="change_point", chunk_size=None, model="l2", n_bkps=None):
    if method not in ["change_point", "fixed_size"]:
        raise ValueError("Invalid method. Choose 'change_point' or 'fixed_size'.")

    chunks = []
    indices = []

    if method == "fixed_size":
        if chunk_size is None:
            raise ValueError("chunk_size must be specified for 'fixed_size' method.")
        for start in range(0, len(data), chunk_size):
            end = min(start + chunk_size, len(data))
            chunks.append(data[start:end])
            indices.append((start, end))
    elif method == "change_point":
        if n_bkps is None:
            raise ValueError("n_bkps must be specified for 'change_point' method.")
        algo = rpt.Binseg(model=model).fit(data)
        change_points = algo.predict(n_bkps=n_bkps)
        start = 0
        for end in change_points:
            chunks.append(data[start:end])
            indices.append((start, end))
            start = end

    return chunks, indices

# Function for chunk evaluation
def evaluate_chunks_cat(data, chunk_size, method="homogeneity"):
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    scores = []

    for chunk in chunks:
        if method == "homogeneity":
            # Homogeneity: Proportion of most common category
            counter = Counter(chunk)
            most_common = counter.most_common(1)[0][1]
            score = most_common / len(chunk)
        elif method == "coverage":
            # Coverage: Unique categories in the chunk
            unique_categories = len(set(chunk))
            score = unique_categories / len(set(data))
        elif method == "entropy":
            # Entropy: Measure of randomness
            counter = Counter(chunk)
            probabilities = [count / len(chunk) for count in counter.values()]
            score = entropy(probabilities, base=2)
        else:
            raise ValueError("Invalid method. Choose 'homogeneity', 'coverage', or 'entropy'.")
        
        scores.append(score)

    return scores
