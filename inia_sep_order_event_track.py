import streamlit as st
import pandas as pd
from datetime import datetime,timedelta
from universal_component_for_campaign import load_and_process_data,process_usfeed_and_hmfeed_sku_on_ads_data,process_hk_cost_and_value_on_ads_data,\
    process_old_new_sku_2022_and_2023_on_ads_data,merged_spu_to_sku_on_ads_data,merged_imagelink_to_sku_on_ads_data,create_date_filtered_df,\
    output_groupby_df,out_date_range_data,add_groupby_sum_columns_to_list_df,create_dynamic_column_setting,add_custom_proportion_to_df,\
    add_custom_proportion_to_df_x100,format_first_two_rows,format_comparison,colorize_comparison,create_compare_summary_df,\
    create_sensor_gmv_filter_input,create_sensor_campaign_filter_input_df
st.set_page_config(layout="wide")
# ---------------------------------------------------------------------基础数据处理区开始---------------------------------------------------------------------------------------------------
all_url = 'https://docs.google.com/spreadsheets/d/1HWOwov8m3FaFlBrCVOWSCPoTNdctBf2eJYiNLBkHUlE/'
ga4_event_track = load_and_process_data(all_url,0)
order_index = load_and_process_data(all_url,920934221)
order_index = order_index.rename(columns={'订单ID':'出单订单号码'})
ga4_event_track = merged_spu_to_sku_on_ads_data(ga4_event_track,order_index,'出单订单号码', '订单名')
unique_order = ga4_event_track['订单名'].unique()
unique_order  = pd.DataFrame(unique_order).dropna(axis=0)
order_options = st.multiselect(
    '选择shopify订单号',
    unique_order
)
ga4_event_track_filter_order_select_df = ga4_event_track[ga4_event_track['订单名'].isin(order_options)]
user_id = ga4_event_track_filter_order_select_df['用户ID']
ga4_event_track_filter_order_select_df = ga4_event_track[ga4_event_track['用户ID'].isin(user_id)]
ga4_event_track_filter_order_select_df = ga4_event_track_filter_order_select_df.drop(columns=['用户ID','触发事件属性','出单订单号码'])
ga4_event_track_filter_order_select_df = ga4_event_track_filter_order_select_df.sort_values(by="时间",ascending=False)
st.dataframe(ga4_event_track_filter_order_select_df)
