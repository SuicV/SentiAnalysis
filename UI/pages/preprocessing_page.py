import streamlit as st
from UI.froms.preprocessing.preprocessing_form import preprocessing_form
import pandas as pd
import spacy
from Preprocessors.ReviewPreprocessor import ReviewPreprocessor


def preprocessing_page():
    # Upload dataset
    dataset, submit_button = preprocessing_form()
    if submit_button:
        df = pd.read_csv(dataset, encoding="utf-8")
        st.write(df)
        nlp = spacy.load("en_core_web_sm")
        preprocessor = ReviewPreprocessor(df["review"], nlp, ["riad", "dar", "rif"], 0.4)
        # Text Preprocessing
        st.subheader('Text Preprocessing')
        with st.spinner('Wait! text preporocessing in progress'):
            with st.expander('Expand for details'):
                # remove useless features
                st.subheader('Remove useless features')
                df["cleaned_review"] = preprocessor.remove_tags()
                st.table(df[['review', 'cleaned_review']].head(2))

                # transform reviews to lowercase form
                st.subheader('Transformation to lowercase')
                df["cleaned_review"] = preprocessor.lowercase_transformation()
                st.table(df[['review', 'cleaned_review']].head(2))

                # spelling correction
                st.subheader('Spelling correction')
                df["cleaned_review"] = preprocessor.spelling_correction()
                st.table(df[['review', 'cleaned_review']].head(2))

                # remove objective sentences
                st.subheader('remove objective sentences')
                df["cleaned_review"] = preprocessor.remove_objective_sentences()

                #drop empty cleaned_reviews
                df = df[df["cleaned_review"].notna() | (df["cleaned_review"] != "")]

                st.table(df[['review', 'cleaned_review']].head(2))

        # Download csv file
        csv = df.to_csv(index=False).encode('utf-8')
        filename = dataset.name.replace('.csv', '_clean.csv')
        st.download_button("Download the clean data", csv,filename, "text/csv",key='download-csv')
        st.stop()
