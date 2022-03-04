from Preprocessors.ReviewPeprocessor import ReviewPreprocessor
import pandas as pd
import re

reviews = pd.Series(["the foood was soo delecious, and spiecy, i think it was madee by #simon_gg. the staff's is greade.",
                     "the enviroment was crazyii"])
preprocessor = ReviewPreprocessor(reviews)
print(preprocessor.start())