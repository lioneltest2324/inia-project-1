import streamlit as st
import pandas as pd
from universal_component_for_campaign import load_and_process_data,process_usfeed_and_hmfeed_sku_on_ads_data,process_hk_cost_and_value_on_ads_data,\
    process_old_new_sku_2022_and_2023_on_ads_data,merged_spu_to_sku_on_ads_data,merged_imagelink_to_sku_on_ads_data,create_date_filtered_df,\
    output_groupby_df,out_date_range_data,add_groupby_sum_columns_to_list_df,create_dynamic_column_setting,add_custom_proportion_to_df,add_custom_proportion_to_df_x100,\
    create_sensor_gmv_filter_input,create_bulk_sku_input,create_sensor_campaign_filter_input_df,condition_evaluate,merged_saleprice_to_sku_on_ads_data,\
    create_compare_summary_df,format_first_two_rows,format_comparison,colorize_comparison
st.set_page_config(layout="wide")
# ---------------------------------------------------------------------基础数据处理区开始---------------------------------------------------------------------------------------------------
ads_cost_url = 'https://docs.google.com/spreadsheets/d/1Dhq7TCw04r8UFkikGuyhdGy4aHqMXHKGxcTkrcyiVzA/edit?gid=0#gid=0'
ads_conversion_url = 'https://docs.google.com/spreadsheets/d/19avn6L_DlOnDWU4xWuKvCpBZPhg_702e6BguLD5Ec58/edit?gid=1848692976#gid=1848692976'
ads_campaign_daily = load_and_process_data(ads_cost_url,0)
ads_conversion_daily = load_and_process_data(ads_conversion_url,1848692976)
ads_campaign_daily = ads_campaign_daily[['Date','Campaign Name','impression','click','cost']]
ads_campaign_daily  = ads_campaign_daily[~ads_campaign_daily.isnull().all(axis=1)]
unique_conversion_action = ads_conversion_daily['conversion action'].unique()
conversion_action_options = st.multiselect(
    '选择转化操作',
    unique_conversion_action,
    ['Purchase']
)
ads_campaign_daily = output_groupby_df(ads_campaign_daily,['Date'], ['impression','cost','click'], 'sum').reset_index()
ads_conversion_daily = output_groupby_df(ads_conversion_daily,['Date','conversion action'], ['all conversions','all conversion value'], 'sum').reset_index()
combine_campaign_df = pd.merge(ads_conversion_daily,ads_campaign_daily,on=['Date'], how='left')
combine_campaign_df = combine_campaign_df[combine_campaign_df['conversion action'].isin(conversion_action_options)]
ads_daliy_summary_df = output_groupby_df(combine_campaign_df,['Date'], ['impression','cost','click','all conversions','all conversion value'], 'sum').reset_index()
ads_daliy_summary_df= add_custom_proportion_to_df(ads_daliy_summary_df,'all conversion value','cost','ads ROI')
ads_daliy_summary_df= add_custom_proportion_to_df(ads_daliy_summary_df,'cost','click','CPC')
ads_daliy_summary_df = add_custom_proportion_to_df(ads_daliy_summary_df,'click','impression','CTR')
ads_daliy_summary_df = add_custom_proportion_to_df(ads_daliy_summary_df,'all conversions','click','CVR')

st.dataframe(ads_daliy_summary_df,width=2000, height=1000)
