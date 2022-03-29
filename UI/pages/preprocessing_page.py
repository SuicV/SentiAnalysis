import streamlit as st
import pandas as pd
import spacy
from Preprocessors.ReviewPreprocessor import ReviewPreprocessor

def preprocessing_page():
    # Upload dataset
    st.subheader('Upload Dataset')
    dataset = st.file_uploader("", type = ['csv'])
    if dataset is not None:
        df = pd.read_csv(dataset, encoding="utf-8")
        st.write(df)
        nlp = spacy.load("en_core_web_sm")
        preprocessor = ReviewPreprocessor(df["review"], nlp, ["riad", "dar", "rif"], 0.6)
        # Text Preprocessing
        st.subheader('Text Preprocessing')
        with st.spinner('Wait! text preporocessing in progress'):
            with st.expander('Expand for details'):
                # remove duplicate rows
                st.subheader('Remove useless features')
                df["cleaned_review"] = preprocessor.remove_tags()
                st.table(df[['review', 'cleaned_review']].head(2))

                st.subheader('Spelling correction')
                df["cleaned_review"] = preprocessor.spelling_correction()
                st.table(df[['review', 'cleaned_review']].head(2))

                st.subheader('remove objective sentences')
                df["cleaned_review"] = preprocessor.remove_objective_sentences()
                st.table(df[['review', 'cleaned_review']].head(2))

        # Download csv file
        csv = df.to_csv(index=False).encode('utf-8')
        filename = dataset.name.replace('.csv', '_clean.csv')        
        st.download_button("Download the clean data", csv,filename, "text/csv",key='download-csv')
        st.stop()