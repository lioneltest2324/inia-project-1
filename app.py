from st_pages import Page, show_pages
import streamlit as st
st.set_page_config(layout="wide")
show_pages(
    [
        Page("get_order_by_sku.py", "根据SKU查当日订单"),
        Page("inia_sep_order_event_track.py", "GA订单用户轨迹(从9月18日开始)"),
        Page("google_daily.py", "谷歌日数据"),
        Page( "google_all_compare_v1.py","谷歌总体自定义日期对比数据(新)"),
        Page("campaign_custom_compare.py","谷歌系列自定义日期对比数据(旧)"),
        Page("google_custom_compare_data.py","谷歌总体自定义日期对比数据(旧)"),
        Page("google-shopping-sku.py","谷歌购物广告产品明细")
    ]
)
