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

def month_2_int(month):
    if month == "Jan":
        return 0
    elif month == "Feb":
        return 1
    elif month == "Mar":
        return 2
    elif month == "Apr":
        return 3
    elif month == "May":
        return 4
    elif month == "June":
        return 5
    elif month == "Jul":
        return 6
    elif month == "Aug":
        return 7
    elif month == "Sep":
        return 8
    elif month == "Oct":
        return 9
    elif month == "Nov":
        return 10
    elif month == "Dec":
        return 11
    else:
        return -1
    
def visitor_type_2_int(visitor_type):
    if visitor_type == "Returning_Visitor":
        return 1
    elif visitor_type == "New_Visitor":
        return 0
    else:
        return -1

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
    # read the csv file
    evidence=[]
    labels=[]
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['Month'] = month_2_int(row['Month'])
            row['VisitorType'] = visitor_type_2_int(row['VisitorType'])
            row['Weekend'] = 1 if row['Weekend'] == "TRUE" else 0
            row['Revenue'] = 1 if row['Revenue'] == "TRUE" else 0
            # set correct types
            row['Administrative'] = int(row['Administrative'])
            row['Informational'] = int(row['Informational'])
            row['ProductRelated'] = int(row['ProductRelated'])
            row['OperatingSystems'] = int(row['OperatingSystems'])
            row['Browser'] = int(row['Browser'])
            row['Region'] = int(row['Region'])
            row['TrafficType'] = int(row['TrafficType'])
            row['Month'] = int(row['Month'])
            row['VisitorType'] = int(row['VisitorType'])
            row['Weekend'] = int(row['Weekend'])
            # floats
            row['Administrative_Duration'] = float(row['Administrative_Duration'])
            row['Informational_Duration'] = float(row['Informational_Duration'])
            row['ProductRelated_Duration'] = float(row['ProductRelated_Duration'])
            row['BounceRates'] = float(row['BounceRates'])
            row['ExitRates'] = float(row['ExitRates'])
            row['PageValues'] = float(row['PageValues'])
            row['SpecialDay'] = float(row['SpecialDay'])
            
            # add to evidence
            row_evidence = [
                row['Administrative'],
                row['Administrative_Duration'],
                row['Informational'],
                row['Informational_Duration'],
                row['ProductRelated'],
                row['ProductRelated_Duration'],
                row['BounceRates'],
                row['ExitRates'],
                row['PageValues'],
                row['SpecialDay'],
                row['Month'],
                row['OperatingSystems'],
                row['Browser'],
                row['Region'],
                row['TrafficType'],
                row['VisitorType'],
                row['Weekend']
            ]
            evidence.append(row_evidence)

            # add to labels
            labels.append(row['Revenue'])
    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # make model
    model = KNeighborsClassifier(n_neighbors=1)
    # train model
    model.fit(evidence, labels)
    # return model
    return model



def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for label, prediction in zip(labels, predictions):
        if label == 1 and prediction == 1:
            tp += 1
        elif label == 0 and prediction == 0:
            tn += 1
        elif label == 0 and prediction == 1:
            fp += 1
        elif label == 1 and prediction == 0:
            fn += 1
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    return (sensitivity, specificity)



if __name__ == "__main__":
    main()
