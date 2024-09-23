from st_pages import Page, show_pages
import streamlit as st
st.set_page_config(layout="wide")
show_pages(
    [
        Page("inia_sep_order_event_track.py", "GA订单用户轨迹"),
        Page("google_daily.py", "谷歌日数据")
    ]
)
