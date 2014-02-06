Eric Gan (andrewID: ericgan)
Language Modeling for 11-411: Natural Language Processing

Runtime: 10 + [numberOfTrainingFiles] * 15 seconds

    Example: If training 4 files, runtime is ~70 seconds.

Usage: python hw03.py [lambda0] [lambda1] [lambda2] [lambda3] [testFile] [trainingFile(s)]

Example:

    python hw03.py 0.25 0.25 0.25 0.25 train/sports.txt train/games.txt
    python hw03.py 0.25 0.30 0.20 0.25 train/health.txt train/sports.txt train/games.txt train/news.txt train/shopping.txt

    The first command will train games.txt and test sports.txt at the given 
        lambda values.
    The second command will train sports.txt, games.txt, news.txt, and
        shopping.txt, and will test health.txt at the given lambda values.

Notes: 

    +As you run the script, stdout will output progress and sometimes 
        information about the different models if VERBOSE is set to True. See
        note on flags below for more information.
    +The code will halt after the Training part is completed. Press Enter to 
        enter to the testing portion. If you only intended to train your model
        and gather information from it, you may exit by hitting Ctrl+C. Then 
        the lambda values and the test file arguments will be irrelevant. (This 
        feature was used to complete subtask1.txt)
    +There are two flags on the top of the file that you can toggle: 
         -VERBOSE: Turn this on if you want to see the top hits for each n-gram
                   DO NOT turn this flag on if you are using more than 1 file!
         -INCLUDEPUNCTUATION: Turn this flag to False if you do not want to 
                   include punctuation in your vocabulary. 
         -MAX_NUMBER_TO_PRINT: This number caps the number of lines the program
                   will print for the top n-gram hits. Increase this number to 
                   show more information. This field is only relevant if VERBOSE
                   is set to True.
    +Lambda values must sum to 1.0, and will raise an error if it doesn't.

Collaborators: I have collaborated with Rachel Kobayashi (received help from her
and (somewhat) gave help to her), and Aaron Anderson (received conceptual help 
from him).
