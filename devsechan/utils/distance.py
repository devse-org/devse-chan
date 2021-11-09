import numpy

def levenshtein(str1: str, str2: str) -> float:
    len1 = len(str1) + 1
    len2 = len(str2) + 1

    matrix = numpy.zeros((len1, len2))
    for i in range(len1):
        matrix[i][0] = i

    for j in range(len2):
        matrix[0][j] = j

    for i in range(1, len1):
        for j in range(1, len2):
            if (str1[i - 1] == str2[j - 1]):
                matrix[i][j] == matrix[i - 1][j - 1]
            else:
                matrix[i][j] = min(
                    matrix[i-1, j], matrix[i-1, j-1], matrix[i, j-1]) + 1
    return matrix[len1-1,len2-1]