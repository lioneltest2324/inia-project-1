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
ads_cost_url = 'https://docs.google.com/spreadsheets/d/19avn6L_DlOnDWU4xWuKvCpBZPhg_702e6BguLD5Ec58/edit?gid=0'
ads_campaign_daily = load_and_process_data(ads_cost_url,1392279435)
ads_conversion_daily = load_and_process_data(ads_cost_url,0)
ads_campaign_daily = output_groupby_df(ads_campaign_daily,['Date','SKU'], ['impression','click','cost'], 'sum').reset_index()
ads_conversion_daily = output_groupby_df(ads_conversion_daily,['Date','SKU','conversion action'], ['conversions','conversion value','all conversions','all conversion value'], 'sum').reset_index()
# combine_ads_df = pd.merge(ads_conversion_daily,ads_campaign_daily,on=['Date','SKU'], how='left')
with st.sidebar:
    selected_range = out_date_range_data(ads_campaign_daily, 'Date', "自选日期范围")
    ads_campaign_daily['Date'] = pd.to_datetime(ads_campaign_daily['Date'])
    ads_conversion_daily['Date'] = pd.to_datetime(ads_conversion_daily['Date'])
    
    ads_campaign_cost_daily_range_df = create_date_filtered_df(ads_campaign_daily, 'Date', selected_range)
    ads_campaign_conversion_daily_range_df = create_date_filtered_df(ads_conversion_daily, 'Date', selected_range)
unique_conversion_action = ads_conversion_daily['conversion action'].unique()
conversion_action_options = st.multiselect(
    '选择转化操作',
    unique_conversion_action,
    ['Purchase']
)
ads_campaign_conversion_daily_range_df = ads_campaign_conversion_daily_range_df[ads_campaign_conversion_daily_range_df['conversion action'].isin(conversion_action_options)]
ads_campaign_conversion_sum_df = output_groupby_df(ads_campaign_conversion_daily_range_df,['SKU'], ['all conversions','all conversion value'], 'sum').reset_index()
ads_campaign_cost_sum_df = output_groupby_df(ads_campaign_cost_daily_range_df,['SKU'], ['impression','click','cost'], 'sum').reset_index()
sumary_daily = pd.merge(ads_campaign_cost_sum_df,ads_campaign_conversion_sum_df,on=['SKU'], how='left')

sumary_daily= add_custom_proportion_to_df(sumary_daily,'all conversion value','cost','ads ROI')
sumary_daily= add_custom_proportion_to_df(sumary_daily,'cost','click','CPC')
sumary_daily = add_custom_proportion_to_df(sumary_daily,'click','impression','CTR')
sumary_daily = add_custom_proportion_to_df(sumary_daily,'all conversions','click','CVR')
sumary_daily = add_custom_proportion_to_df(sumary_daily,'cost','all conversions','CPA')

column_config = {}
column_config['CTR'] = st.column_config.NumberColumn(
    format='%.2f%%',  # 显示为百分比
    min_value=0,
    max_value=1,
            )
column_config['CVR'] = st.column_config.NumberColumn(
    format='%.2f%%',  # 显示为百分比
    min_value=0,
    max_value=1,
            )

st.dataframe(sumary_daily,width=2000, height=400,column_config=column_config)
