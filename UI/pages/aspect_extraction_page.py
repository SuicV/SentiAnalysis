import streamlit as st
import pandas as pd
import spacy
from Aspects.ExplicitAspectExtractor import ExplicitAspectExtractor
from Aspects.CoRefAspectIdentGrouping import CoRefAspectIdentGrouping
from Aspects.ImplicitAspectExtractor import ImplicitAspectExtractor
import plotly.express as px


def aspects_extraction_page():
    # configuration form
    st.markdown('**configuration**')
    with st.form("config_aspect_extraction"):
        col1, col2 = st.columns(2)
        with col1:    
            dataset = st.file_uploader("upload cleaned dataset", type = ['csv'])

        with col2:
            aspects_number = st.number_input("number of aspects", min_value=1, max_value=100, value=50)

        submited = st.form_submit_button("Extract")
 
    # when the user clicks on the submition button
    if submited and dataset is not None:
        df = pd.read_csv(dataset, encoding="utf-8")
        df = df[df['cleaned_review'].notna()]
        st.write(df)
        nlp = spacy.load("en_core_web_sm")

        with st.expander("Explicit Aspect Extraction"):
            with st.spinner('Wait! extracting explicit aspects in progress'):
                explicit_aspects_extractor = ExplicitAspectExtractor(df["cleaned_review"], nlp)
                extracted_aspects = explicit_aspects_extractor.start(aspects_number)
                st.session_state["explicit_aspects"] = extracted_aspects
                aspects_df = pd.DataFrame(extracted_aspects, columns=["aspects", "frequency"])
            st.write(aspects_df.shape)
            aspects_plot = px.bar(aspects_df, x="aspects", y="frequency")
            st.plotly_chart(aspects_plot)

        with st.expander("Co-reference aspects identification and grouping"):
            with st.spinner('Wait! Co-reference aspects identification and grouping in progress'):
                coref_aspects_ident_group = CoRefAspectIdentGrouping(df, dict(extracted_aspects), nlp)
                if "co_ref_word2vec_model" in st.session_state:
                    coref_aspects_ident_group.model_wv = st.session_state.get("co_ref_word2vec_model")
                # TODO: save word2vec as pickle file to avoid using session
                coref_groups = coref_aspects_ident_group.get_co_reference_aspects_groups(0.980)
                if "co_ref_word2vec_model" not in st.session_state:
                    st.session_state["co_ref_word2vec_model"] = coref_aspects_ident_group.model_wv
                st.session_state["co_ref_aspects"] = coref_groups
                st.write(coref_groups)

        with st.expander("Implicit aspects extraction"):
            with st.spinner('Wait! extracting implicit aspects in progress'):
                co_occurence_matrix = coref_aspects_ident_group.get_co_occurrence_matrix()
                implicit_aspect_extractor = ImplicitAspectExtractor(df["cleaned_review"], co_occurence_matrix, nlp)
                df_implicit_aspects, implicit_aspects_summary = implicit_aspect_extractor.extract_implicit_aspects()
                st.write(df_implicit_aspects)
                
                st.session_state['implicit_aspect_summary'] = implicit_aspects_summary.groupby(["aspect", "sentiment"]).size().reset_index(name="count").sort_values("count", ascending=False)
