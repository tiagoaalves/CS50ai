import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    evidence = []
    labels = []

    with open("shopping.csv", newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        for row in spamreader:

            splitted = row[0].split(",")

            if splitted[0] == "Administrative":
                continue

            floats = {1, 3, 5, 6, 7, 8, 9}
            ints = {0, 2, 4, 11, 12, 13, 14}
            setter = []
            for i in range(18):
                if i in floats:
                    setter.append(float(splitted[i]))
                elif i in ints:
                    setter.append(int(splitted[i]))
                elif i == 10:
                    if splitted[i] == "Jan":
                        setter.append(0)
                    if splitted[i] == "Feb":
                        setter.append(1)
                    if splitted[i] == "Mar":
                        setter.append(2)
                    if splitted[i] == "Apr":
                        setter.append(3)
                    if splitted[i] == "May":
                        setter.append(4)
                    if splitted[i] == "June":
                        setter.append(5)
                    if splitted[i] == "Jul":
                        setter.append(6)
                    if splitted[i] == "Aug":
                        setter.append(7)
                    if splitted[i] == "Sep":
                        setter.append(8)
                    if splitted[i] == "Oct":
                        setter.append(9)
                    if splitted[i] == "Nov":
                        setter.append(10)
                    if splitted[i] == "Dec":
                        setter.append(11)
                elif i == 15:
                    if splitted[i] == "Returning_Visitor":
                        setter.append(1)
                    else:
                        setter.append(0)
                elif i == 16:
                    if splitted[i] == "TRUE":
                        setter.append(1)
                    else:
                        setter.append(0)
                elif i == 17:
                    if splitted[i] == "TRUE":
                        labels.append([1])
                    else:
                        labels.append([0])
            evidence.append(setter)

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

        
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    positive = 0.0
    positiveTotal = 0.0
    negative = 0.0
    negativeTotal = 0.0

    for i in range(len(labels)):

        if labels[i][0] == 1:

            if labels[i] == predictions[i]:
                positive += 1.0
                positiveTotal += 1.0

            else:
                positiveTotal += 1.0

        else:
            if labels[i] == predictions[i]:
                negative += 1.0
                negativeTotal += 1.0

            else:
                negativeTotal += 1.0

    sensitivity = positive / positiveTotal
    specificty = negative / negativeTotal

    return (sensitivity, specificty)


if __name__ == "__main__":
    main()
