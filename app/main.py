# imports
import streamlit as st
import datetime
import util_funcs

con = None

# page info
st.set_page_config(
    layout='centered',
    page_title='Sofia Air',
    page_icon=':cloud:'
)


def form_callback():
    st.session_state.reload = not st.session_state.reload


def main():
    st.session_state.lang = 'en'

    content = util_funcs.load_content()

    st.session_state['df'] = util_funcs.read_data()
    st.session_state['min_max_date'] = util_funcs.min_max_date(st.session_state['df'])

    # get selector data
    stations = st.session_state['df']['station_name'].unique()

    if 'station_selector' not in st.session_state:
        util_funcs.map(st.session_state['df'], stations, None)
        st.session_state.reload = False
    else:
        st.session_state.update({
            'df':
            util_funcs.show_by_time(
                util_funcs.show_by_location(
                    st.session_state['df'],
                    st.session_state['station_selector']
                ),
                st.session_state['min_max_date'][0],
                st.session_state['min_max_date'][1]
            )
        })
        util_funcs.map(st.session_state['df'], stations, None)

    format = 'DD.MM.YYYY'
    start_date = datetime.datetime.fromisoformat(
        st.session_state['min_max_date'][0]).date()
    end_date = datetime.datetime.fromisoformat(
        st.session_state['min_max_date'][1]).date()
    max_days = end_date - start_date

    with st.form(key='map_properties'):
        st.multiselect(
            content['ams_selector'][st.session_state.lang],
            options=stations,
            default=stations,
            key='station_selector'
        )

        slider = st.slider(
            'Select date',
            min_value=start_date,
            value=(start_date, end_date),
            max_value=end_date,
            format=format
        )

        submit_button = st.form_submit_button(
            label='Get information',
            on_click=form_callback
        )


if __name__ == "__main__":
    main()
