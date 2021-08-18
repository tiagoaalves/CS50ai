import csv
import itertools
import sys

PROBS = {
    # Unconditional probabilities for having gene
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        # Probability of trait given two copies of gene
        2: {True: 0.65, False: 0.35},
        # Probability of trait given one copy of gene
        1: {True: 0.56, False: 0.44},
        # Probability of trait given no gene
        0: {True: 0.01, False: 0.99},
    },
    # Mutation probability
    "mutation": 0.01,
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (
                people[person]["trait"] is not None
                and people[person]["trait"] != (person in have_trait)
            )
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (
                    True
                    if row["trait"] == "1"
                    else False
                    if row["trait"] == "0"
                    else None
                ),
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s)
        for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    result = 1
    for person in people:

        # if the person has parents in the dataset
        if people[person]["mother"] != None:

            # find the number of genes of the persons mother
            if people[person]["mother"] in one_gene:
                mother = 1
            elif people[person]["mother"] in two_genes:
                mother = 2
            else:
                mother = 0

            # find the numer of genes of the persons father
            if people[person]["father"] in one_gene:
                father = 1
            elif people[person]["father"] in two_genes:
                father = 2
            else:
                father = 0

            # find the number of genes of the person
            if person in one_gene:

                # find if its supposed to calculate the probability of having the trait
                if person in have_trait:

                    # calculate the probability
                    result *= oneGeneParents(True, mother, father)

                else:
                    result *= oneGeneParents(False, mother, father)

            if person in two_genes:

                if person in have_trait:
                    result *= twoGenesParents(True, mother, father)
                else:
                    result *= twoGenesParents(False, mother, father)

            if person not in one_gene and person not in two_genes:

                if person in have_trait:
                    result *= zeroGenesParents(True, mother, father)
                else:
                    result *= zeroGenesParents(False, mother, father)

        # if the person doesnt have parents in the dataset
        else:

            # find the number of genes of the person
            if person in one_gene:

                # find if its supposed to calculate the probability of having the trait
                if person in have_trait:
                    result *= oneGene(True)
                else:
                    result *= oneGene(False)

            if person in two_genes:

                if person in have_trait:
                    result *= twoGenes(True)
                else:
                    result *= twoGenes(False)

            if person not in one_gene and person not in two_genes:

                if person in have_trait:
                    result *= zeroGenes(True)
                else:
                    result *= zeroGenes(False)
        # print(result)
    return result


# People with no parents

# find the probabilty of having zero genes and trait/not trait
def zeroGenes(trait):
    if trait:
        return PROBS["gene"][0] * PROBS["trait"][0][True]
    return PROBS["gene"][0] * PROBS["trait"][0][False]


# find the probabilty of having one gene and trait/not trait
def oneGene(trait):
    if trait:
        return PROBS["gene"][1] * PROBS["trait"][1][True]
    return PROBS["gene"][1] * PROBS["trait"][1][False]


# find the probabilty of having two genes and trait/not trait
def twoGenes(trait):
    if trait:
        return PROBS["gene"][2] * PROBS["trait"][2][True]
    return PROBS["gene"][2] * PROBS["trait"][2][False]


# People with parents

# find the probabilty of having zero genes and trait/not trait
def zeroGenesParents(trait, mother, father):
    result = 1

    if mother == 0:
        result *= 1 - PROBS["mutation"]

    elif mother == 1:
        result *= 0.5 * (1 - PROBS["mutation"]) + (0.5 * PROBS["mutation"])

    elif mother == 2:
        result *= PROBS["mutation"]

    if father == 0:
        result *= 1 - PROBS["mutation"]

    elif father == 1:
        result *= 0.5 * (1 - PROBS["mutation"]) + (0.5 * PROBS["mutation"])

    elif father == 2:
        result *= PROBS["mutation"]

    if trait:
        result *= PROBS["trait"][0][True]
    else:
        result *= PROBS["trait"][0][False]

    return result


# find the probabilty of having one gene and trait/not trait
def oneGeneParents(trait, mother, father):
    mothernotFather = 1
    fatherNotMother = 1

    if mother == 0:
        mothernotFather *= PROBS["mutation"]
        fatherNotMother *= 1 - PROBS["mutation"]

    elif mother == 1:
        mothernotFather *= 0.5 * (1 - PROBS["mutation"]) + (0.5 * PROBS["mutation"])
        fatherNotMother *= 0.5 * (1 - PROBS["mutation"]) + (0.5 * PROBS["mutation"])

    elif mother == 2:
        mothernotFather *= 1 - PROBS["mutation"]
        fatherNotMother *= PROBS["mutation"]

    if father == 0:
        mothernotFather *= 1 - PROBS["mutation"]
        fatherNotMother *= PROBS["mutation"]

    elif father == 1:
        mothernotFather *= 0.5 * (1 - PROBS["mutation"]) + (0.5 * PROBS["mutation"])
        fatherNotMother *= 0.5 * (1 - PROBS["mutation"]) + (0.5 * PROBS["mutation"])

    elif father == 2:
        mothernotFather *= PROBS["mutation"]
        fatherNotMother *= 1 - PROBS["mutation"]

    else:
        "error in fathers number of genes"

    result = mothernotFather + fatherNotMother

    if trait:
        result *= PROBS["trait"][1][True]
    else:
        result *= PROBS["trait"][1][False]

    return result


# find the probabilty of having two genes and trait/not trait
def twoGenesParents(trait, mother, father):
    result = 1

    if mother == 0:
        result *= PROBS["mutation"]

    elif mother == 1:
        result *= 0.5 * (1 - PROBS["mutation"]) + (0.5 * PROBS["mutation"])

    elif mother == 2:
        result *= 1 - PROBS["mutation"]

    else:
        "error in mothers number of genes"

    if father == 0:
        result *= PROBS["mutation"]

    elif father == 1:
        result *= 0.5 * (1 - PROBS["mutation"]) + (0.5 * PROBS["mutation"])

    elif father == 2:
        result *= 1 - PROBS["mutation"]

    else:
        "error in fathers number of genes"

    if trait:
        result *= PROBS["trait"][2][True]
    else:
        result *= PROBS["trait"][2][False]

    return result


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # raise NotImplementedError

    for person in probabilities:
        # print(p)

        # add p to trait
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p

        # add p to gene
        if person in one_gene:
            probabilities[person]["gene"][1] += p

        elif person in two_genes:
            probabilities[person]["gene"][2] += p

        else:
            probabilities[person]["gene"][0] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:

        # normalize gene distribution

        total = (
            probabilities[person]["gene"][0]
            + probabilities[person]["gene"][1]
            + probabilities[person]["gene"][2]
        )

        probabilities[person]["gene"][0] = probabilities[person]["gene"][0] / total

        probabilities[person]["gene"][1] = probabilities[person]["gene"][1] / total

        probabilities[person]["gene"][2] = probabilities[person]["gene"][2] / total

        # normalize trait distribution

        total = (
            probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        )

        probabilities[person]["trait"][True] = (
            probabilities[person]["trait"][True] / total
        )

        probabilities[person]["trait"][False] = (
            probabilities[person]["trait"][False] / total
        )


if __name__ == "__main__":
    main()
