import streamlit as st
from Classifiers.NLPSentimentClassifier import NLPSentimentClassifier
import spacy
import pandas as pd
import plotly.express as px


def sentiment_classification_page():
	if "explicit_aspects" in st.session_state and "implicit_aspect_summary" in st.session_state:
		dataset_file = None
		with st.form("config_sentiment_classification"):
			dataset_file = st.file_uploader("Upload cleaned dataset", type = ["csv"])
			submited = st.form_submit_button("Classify")

		if submited and dataset_file is not None:
			nlp = spacy.load("en_core_web_sm")
			df = pd.read_csv(dataset_file, encoding="utf-8")
			df = df[df['cleaned_review'].notna()]
			st.write(df)
			
			nlp_classifier = NLPSentimentClassifier(df["cleaned_review"], list(dict(st.session_state["explicit_aspects"]).keys()), nlp)
			
			classification_result = nlp_classifier.start()
			classification_result = pd.concat([classification_result, st.session_state['implicit_aspect_summary']], ignore_index=True)
			
			grouped_classification_result = classification_result.groupby(["aspect", "sentiment"]).size().reset_index(name="count").sort_values("count", ascending=False)
			sentiment_plot = px.bar(grouped_classification_result, x="aspect", y="count", color="sentiment", width=1000, height=500)

			aggregated_result = grouped_classification_result.groupby(["sentiment"]).sum("count").reset_index()
			pi_plot = px.pie(aggregated_result, names="sentiment", values="count")

			st.plotly_chart(sentiment_plot, use_container_width=True)
			st.plotly_chart(pi_plot)

	else:
		st.warning("You can not apply sentiment classification process without extracting aspects")
	pass