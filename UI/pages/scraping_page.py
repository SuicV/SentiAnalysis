from os import link
import streamlit as st
from Scrappers.BookingAgoda_Scrapper import BookingAgoda_Scrapper

from UI.froms.scraping.scrap_by_search_form import scrap_by_search_form
from UI.froms.scraping.scrap_by_link_form import scrap_by_link_form

from Scrappers.AgodaScrapper import AgodaScrapper
from Scrappers.TripAdvisorScrapper import TripAdvisorScrapper

import pandas as pd

from time import gmtime

def scrap_reviews_by_link (params):
    print(params)
    """
    function to apply the process of getting reviews by a defined hotel url

    :param tripadvisor_url
    :param agoda_url
    :param num_pages number of reviews pages to scrap

    :return reviews, file_name
    """
    reviews = pd.DataFrame(columns=["listing_name", "listing_score", "username", "review_score", "review_title", "review"])
    reviews_temp = None
    file_name = "reviews_"
    progress = st.progress(0)
    scrappers = []
    if params["tripadvisor_url"] != "":
        scrappers.append(TripAdvisorScrapper)
        file_name += "TripAdvisor_"
    elif params["agoda_url"] != "":
        if params["booking_option"]:
            scrappers.append(BookingAgoda_Scrapper)
            file_name += "Booking_"
        elif params["agoda_option"]:
            scrappers.append(AgodaScrapper)
            file_name += "Agoda_"

    progress.progress(5)

    for step, scraper in enumerate(scrappers):
        scraper = scraper()

        link = params["tripadvisor_url"] if isinstance(scraper, TripAdvisorScrapper) else params["agoda_url"]
        
        reviews_temp = pd.DataFrame(scraper.get_reviews(link, int(params["num_pages"])))
        reviews = pd.concat([reviews, reviews_temp], axis=0, ignore_index=True)
        scraper.scrapper.quit()
        progress.progress(int((step+1)*100/len(scrappers)))
    
    del reviews_temp
    return (reviews, file_name)

def scrap_reviews_by_search(search_tag, otas, num_pages, hotels_count):
    """
    function to apply the process of getting reviews by search tag

    :param search_tag search tag to be used by scrapers class
    :param otas online travel agencies
    :param num_pages number of reviews pages to scrap for each hotel page
    :param hotels_count number of hotels to scrap reviews from

    :return reviews, file_name
    """
    reviews = pd.DataFrame(columns = ["listing_name", "listing_score", "username", "review_score", "review_title", "review"])
    reviews_temp = None
    file_name = "reviews_"
    progress = st.progress(5)
    scrappers = []
    for ota in otas:
        if ota == "TripAdvisor":
            scrappers.append(TripAdvisorScrapper)
            file_name += "TripAdvisor_"
        elif ota == "Agoda":
            scrappers.append(AgodaScrapper)
            file_name += "Agoda_"
        elif ota == "Booking":
            scrappers.append(BookingAgoda_Scrapper)
            file_name += "Booking_"

    agoda_links = None
    for step, scrapper in enumerate(scrappers):
        scraper = scrapper()
        if isinstance(scrapper, (BookingAgoda_Scrapper, AgodaScrapper)):
            if agoda_links is None:
                links = scraper.get_hotels(search_tag)
            else:
                links = agoda_links
        else:
            links = scraper.get_hotels(search_tag)
        if links == False:
            continue
        max_url = len(links) if hotels_count > len(links) else hotels_count
        for i in range(max_url):
            reviews_temp = pd.DataFrame(scraper.get_reviews(links[i]["link"], num_pages))
            reviews = pd.concat([reviews, reviews_temp], ignore_index=True)
        
        scraper.scrapper.quit()
        
        progress.progress(int((step+1)*100/len(scrappers)))
    
    return reviews, file_name

def scraping_page():
    # scrap reviews by search tag form
    data_search_form, search_form_submition_button = scrap_by_search_form()
    
    # apply scrap reviews by search
    if search_form_submition_button :
        reviews, file_name = scrap_reviews_by_search(data_search_form["search_tag"], data_search_form["otas_values"], data_search_form["search_num_pages"], data_search_form["urls_count"])
        # show scraped reviews
        st.dataframe(reviews)
        # save scraped reviews as csv file
        csv = reviews.to_csv(index=False).encode('utf-8')
        current_time = gmtime()
        # YYYY_MM_DD_hh_mm_ss.csv
        file_name += f"{current_time[0]}_{current_time[1]}_{current_time[2]}_{current_time[3]}_{current_time[4]}_{current_time[5]}.csv"
        st.download_button("Download reviews as csv file", csv,file_name, "text/csv",key='download-csv')
        st.stop()
    
    # scrap reviews by link form
    data_link_form, link_form_submition_button = scrap_by_link_form()
    
    # apply scraping reviews by link
    if link_form_submition_button:
        reviews, file_name = scrap_reviews_by_link(data_link_form)
        
        # show scraped reviews
        st.dataframe(reviews)
        # save scraped reviews as csv file
        csv = reviews.to_csv(index=False).encode('utf-8')
        current_time = gmtime()
        # YYYY_MM_DD_hh_mm_ss.csv
        file_name += f"{current_time[0]}_{current_time[1]}_{current_time[2]}_{current_time[3]}_{current_time[4]}_{current_time[5]}.csv"
        st.download_button("Download reviews as csv file", csv,file_name, "text/csv",key='download-csv')
        st.stop()
    pass