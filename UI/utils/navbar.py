import hydralit_components as hc


def navbar():
	menu_data = [
		{'id': 'Reviews Scraping', 'label': '🕸 Reviews Scraping'},
		{'id': 'Reviews Preprocessing', 'label': '⚙Reviews Preprocessing'},
		#{'id': 'Aspects Extraction', 'label': '⚗Aspects Extraction'},
		{'id':'Sentiments Classification', 'label':'😃☹Sentiments Classification'},
	]

	over_them = {'txc_inacive': '#FFFFFF'}
	menu_id = hc.nav_bar(menu_definition=menu_data,
	                     override_theme=over_them,
	                     home_name='Home',
	                     first_select=0,
	                     hide_streamlit_markers=False,  # will show the st hamburger as well as the navbar now!
	                     sticky_nav=True,  # at the top or not
	                     sticky_mode='pinned')  # jumpy or not-jumpy, but sticky or pinned

	return menu_id
