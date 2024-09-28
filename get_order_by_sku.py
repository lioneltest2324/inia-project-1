import streamlit as st
import pandas as pd
from universal_component_for_campaign import load_and_process_data,process_usfeed_and_hmfeed_sku_on_ads_data,process_hk_cost_and_value_on_ads_data,\
    process_old_new_sku_2022_and_2023_on_ads_data,merged_spu_to_sku_on_ads_data,merged_imagelink_to_sku_on_ads_data,create_date_filtered_df,\
    output_groupby_df,out_date_range_data,add_groupby_sum_columns_to_list_df,create_dynamic_column_setting,add_custom_proportion_to_df,add_custom_proportion_to_df_x100,\
    create_sensor_gmv_filter_input,create_bulk_sku_input,create_sensor_campaign_filter_input_df,condition_evaluate,merged_saleprice_to_sku_on_ads_data,\
    create_compare_summary_df,format_first_two_rows,format_comparison,colorize_comparison
st.set_page_config(layout="wide")
# ---------------------------------------------------------------------基础数据处理区开始---------------------------------------------------------------------------------------------------
sku_url = 'https://docs.google.com/spreadsheets/d/10VvttII97JrNQ02mRE1oq8pOqdcGOx6k1QnFJ_1TJng/edit?gid=1906999968#gid=1906999968'
sku_daily = load_and_process_data(sku_url,1906999968)


sku_daily = sku_daily[['订单名','订单创建时间','产品标题','销售数量','产品落地页链接','产品价格']]
sku_daily  = sku_daily[~sku_daily.isnull().all(axis=1)]
sku_daily.loc[sku_daily['产品标题'].str.contains('FOND', na=False), '产品匹配'] = 'FOND'
sku_daily.loc[sku_daily['产品标题'].str.contains('GLOW', na=False), '产品匹配'] = 'GLOW'
sku_daily.loc[sku_daily['产品标题'].str.contains('HAUTE Pro', na=False), '产品匹配'] = 'HAUTE Pro'
sku_daily.loc[sku_daily['产品标题'].str.contains('FLARE', na=False), '产品匹配'] = 'FLARE'

sku_daily.loc[(sku_daily['产品标题'].str.contains('HAUTE', na=False)) & (~sku_daily['产品标题'].str.contains('HAUTE Pro', na=False)), '产品匹配'] = 'HAUTE'
sku_daily['订单创建时间'] = pd.to_datetime(sku_daily['订单创建时间'])
sku_daily['订单创建时间'] = sku_daily['订单创建时间'].dt.strftime('%Y-%m-%d')
unique_sku = sku_daily['产品匹配'].unique()
sku_options = st.multiselect(
    '选择产品',
    unique_sku
)
with st.sidebar:
    selected_range = out_date_range_data(sku_daily, '订单创建时间', "日期范围")

sku_daily['订单创建时间'] = pd.to_datetime(sku_daily['订单创建时间'])
sku_daily_filtered_date_range_df = create_date_filtered_df(sku_daily, '订单创建时间', selected_range)
selected_campaign_date_range_df = sku_daily_filtered_date_range_df[sku_daily_filtered_date_range_df['产品匹配'].isin(sku_options)]
selected_campaign_date_range_df = selected_campaign_date_range_df[['订单名','产品匹配','销售数量','产品价格']]
st.dataframe(selected_campaign_date_range_df,width=2000, height=800)
