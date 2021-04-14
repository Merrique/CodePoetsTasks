import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def GraphComparison(observed,expected):
    '''
    Generates image with a column chart comparing observed and expected frequency distribution of leading digit

            Parameters:
                    observed (list): list with the frequency distribution of leading digit in uploaded data 
                    expected (list): list with expected frequency distribution of leading digit

            Returns:
                    Figure results.png in media folder
    '''
    labels = ['1', '2', '3', '4', '5','6','7','8','9']

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, observed, width, label='Observed')
    rects2 = ax.bar(x + width/2, expected, width, label='Expected')

    ax.set_ylabel('Procent')
    ax.set_title('First number distribution')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()

    plt.savefig('./mysite/media/results.png')


def ChiSquareTest(observed,expected):
    '''
    Caclulates chi square parameter

            Parameters:
                    observed (list): list with the frequency distribution of leading digit in uploaded data 
                    expected (list): list with expected frequency distribution of leading digit

            Returns:
                    procentFirstNumberList (list): Frequency distribution of leading digit in the uploaded data. 
                                                   The order of the elements corresponds directly to frequency distribution of 1, 2, 3, 4, 5, 6, 7, 8, 9
    '''

    chi = 0.
    for i in range(len(observed)):
        chi = chi + ((observed[i]-expected[i])**2)/expected[i]
    
    return(chi)
    

def GetFirstNumbers(uploaded_file,columntitle):
    '''
    Returns list with the frequency distribution of leading digit in uploaded data 

            Parameters:
                    uploaded_file (file): file uploaded by app user
                    columtitle (str): title of the colum with the data to analyze 

            Returns:
                    procentFirstNumberList (list): Frequency distribution of leading digit in the uploaded data. 
                                                   The order of the elements corresponds directly to frequency distribution of 1, 2, 3, 4, 5, 6, 7, 8, 9
    '''

    firstNumberList = [0]*9
    procentFirstNumberList = []
    firstline = uploaded_file.readline()
    firstline = firstline.decode('utf-8')
    columns = firstline.split('\t')

    if columntitle in columns:
        columnNumber = columns.index(columntitle)
        lines = uploaded_file.readlines()
        sum = 0
        for line in lines:
            sum = sum + 1
            words = line.split(b'\t')
            columnData = words[columnNumber].decode('utf-8')
            columnDataNoSigns = columnData.replace('-','')
            columnDataNoSigns = columnDataNoSigns.replace('+','')
            columnDataNoSigns = columnDataNoSigns.replace('.','')

            if not columnDataNoSigns.isnumeric():
                return(None)
            else:
                columnData = format(float(columnData),'+E')
                firstNumber = int(columnData[1])
        
            firstNumberList[firstNumber-1] = firstNumberList[firstNumber-1]+1
        
        for element in firstNumberList:
            procentFirstNumberList.append(element/sum *100)

        
        return(procentFirstNumberList)
    else:
        return(None)


def BenfordAnalysis(uploaded_file,columntitle):
    '''
    Returns information of the agreement of experimental data with theoretical values based on chi sqaure test analysis

            Parameters:
                    uploaded_file (file): file uploaded by app user
                    columtitle (str): title of the colum with the data to analyze 

            Returns:
                    (str): Information if uploaded data matches Benford's Law
    '''
    
    counterFirstNumber = GetFirstNumbers(uploaded_file,columntitle)

    if counterFirstNumber is not None:
        expectedFirstNumber = [30.1,17.6,12.5,9.7,7.9,6.7,5.8,5.1,4.6]

        GraphComparison(counterFirstNumber,expectedFirstNumber)
        chisquare = ChiSquareTest(counterFirstNumber,expectedFirstNumber)
        
        if chisquare < 15.5: #value from chisquare distribution with n=8 alpha=0.05
            return('The observed data matches the expected data distrubtion')
        else:
            return('The observed data DOES NOT match the expected data distrubtion')
    else:
        return(None)

