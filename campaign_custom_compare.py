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
ads_campaign_daily = ads_campaign_daily[['Date','Campaign Name','impression','click','cost','Campaign Type']]
ads_campaign_daily  = ads_campaign_daily[~ads_campaign_daily.isnull().all(axis=1)]
unique_conversion_action = ads_conversion_daily['conversion action'].unique()
conversion_action_options = st.multiselect(
    '选择转化操作',
    unique_conversion_action,
    ['Purchase']
)
unique_campaign = ads_campaign_daily['Campaign Name'].unique()
unique_campaign_options = st.multiselect(
    '选择广告系列',
    unique_campaign
)
with st.sidebar:
    selected_range = out_date_range_data(ads_campaign_daily, 'Date', "对比数据日期范围")
    compare_selected_range = out_date_range_data(ads_campaign_daily, 'Date', "自选日期范围")

ads_campaign_daily['Date'] = pd.to_datetime(ads_campaign_daily['Date'])
ads_conversion_daily['Date'] = pd.to_datetime(ads_conversion_daily['Date'])

ads_cost_daily_filtered_date_range_df = create_date_filtered_df(ads_campaign_daily, 'Date', selected_range)
compare_ads_cost_daily_filtered_date_range_df = create_date_filtered_df(ads_campaign_daily, 'Date', compare_selected_range)
select_ads_cost_daily_filtered_date_range_df = ads_cost_daily_filtered_date_range_df[ads_cost_daily_filtered_date_range_df['Campaign Name'].isin(unique_campaign_options)]
select_compare_ads_cost_daily_filtered_date_range_df = compare_ads_cost_daily_filtered_date_range_df[compare_ads_cost_daily_filtered_date_range_df['Campaign Name'].isin(unique_campaign_options)]
ads_campaign_sum_daily = output_groupby_df(select_ads_cost_daily_filtered_date_range_df,['Date'], ['impression','cost','click'], 'sum').reset_index()
compare_ads_campaign_sum_daily = output_groupby_df(select_compare_ads_cost_daily_filtered_date_range_df,['Date'], ['impression','cost','click'], 'sum').reset_index()


ads_conversion_daily_filtered_date_range_df = create_date_filtered_df(ads_conversion_daily, 'Date', selected_range)
compare_ads_conversion_daily_filtered_date_range_df = create_date_filtered_df(ads_conversion_daily, 'Date', compare_selected_range)
select_ads_conversion_daily_filtered_date_range_df = ads_conversion_daily_filtered_date_range_df[ads_conversion_daily_filtered_date_range_df['Campaign Name'].isin(unique_campaign_options)]
select_compare_ads_conversion_daily_filtered_date_range_df = compare_ads_conversion_daily_filtered_date_range_df[compare_ads_conversion_daily_filtered_date_range_df['Campaign Name'].isin(unique_campaign_options)]
ads_conversion_sum_daily = output_groupby_df(select_ads_conversion_daily_filtered_date_range_df,['Date','conversion action'], ['all conversions','all conversion value'], 'sum').reset_index()
compare_ads_conversion_sum_daily = output_groupby_df(select_compare_ads_conversion_daily_filtered_date_range_df,['Date','conversion action'], ['all conversions','all conversion value'], 'sum').reset_index()

ads_conversion_sum_daily = ads_conversion_sum_daily[ads_conversion_sum_daily['conversion action'].isin(conversion_action_options)]
compare_ads_conversion_sum_daily = compare_ads_conversion_sum_daily[compare_ads_conversion_sum_daily['conversion action'].isin(conversion_action_options)]


combine_campaign_df = pd.merge(ads_campaign_sum_daily,ads_conversion_sum_daily,on=['Date'], how='left')
compare_combine_campaign_df = pd.merge(compare_ads_campaign_sum_daily,compare_ads_conversion_sum_daily,on=['Date'], how='left')

ads_daily_sum_df = pd.DataFrame(columns=['impression','click','cost','all conversions','all conversion value'], data=[[0, 0, 0,0,0]])
ads_daily_sum_df['日期范围'] = pd.to_datetime(selected_range[0]).strftime('%Y-%m-%d')+"至"+pd.to_datetime(selected_range[1]).strftime('%Y-%m-%d')
ads_daily_sum_df['impression'] = combine_campaign_df['impression'].sum()
ads_daily_sum_df['click'] = combine_campaign_df['click'].sum()
ads_daily_sum_df['cost'] = combine_campaign_df['cost'].sum()
ads_daily_sum_df['all conversions'] = combine_campaign_df['all conversions'].sum()
ads_daily_sum_df['all conversion value'] = combine_campaign_df['all conversion value'].sum()
ads_daily_sum_df = ads_daily_sum_df[['日期范围','impression','click','cost','all conversions','all conversion value']]
ads_daily_sum_df= add_custom_proportion_to_df(ads_daily_sum_df,'all conversion value','cost','ads ROI')
ads_daily_sum_df= add_custom_proportion_to_df(ads_daily_sum_df,'cost','click','CPC')
ads_daily_sum_df = add_custom_proportion_to_df_x100(ads_daily_sum_df,'click','impression','CTR')
ads_daily_sum_df = add_custom_proportion_to_df_x100(ads_daily_sum_df,'all conversions','click','CVR')
ads_daily_sum_df = add_custom_proportion_to_df(ads_daily_sum_df,'cost','all conversions','CPA')
ads_daily_sum_df = add_custom_proportion_to_df(ads_daily_sum_df,'all conversion value','all conversions','AOV')


compare_ads_daily_sum_df = pd.DataFrame(columns=['impression','click','cost','all conversions','all conversion value'], data=[[0, 0, 0,0,0]])
compare_ads_daily_sum_df['日期范围'] = pd.to_datetime(compare_selected_range[0]).strftime('%Y-%m-%d')+"至"+pd.to_datetime(compare_selected_range[1]).strftime('%Y-%m-%d')
compare_ads_daily_sum_df['impression'] = compare_combine_campaign_df['impression'].sum()
compare_ads_daily_sum_df['click'] = compare_combine_campaign_df['click'].sum()
compare_ads_daily_sum_df['cost'] = compare_combine_campaign_df['cost'].sum()
compare_ads_daily_sum_df['all conversions'] = compare_combine_campaign_df['all conversions'].sum()
compare_ads_daily_sum_df['all conversion value'] = compare_combine_campaign_df['all conversion value'].sum()
compare_ads_daily_sum_df = compare_ads_daily_sum_df[['日期范围','impression','click','cost','all conversions','all conversion value']]
compare_ads_daily_sum_df= add_custom_proportion_to_df(compare_ads_daily_sum_df,'all conversion value','cost','ads ROI')
compare_ads_daily_sum_df= add_custom_proportion_to_df(compare_ads_daily_sum_df,'cost','click','CPC')
compare_ads_daily_sum_df = add_custom_proportion_to_df_x100(compare_ads_daily_sum_df,'click','impression','CTR')
compare_ads_daily_sum_df = add_custom_proportion_to_df_x100(compare_ads_daily_sum_df,'all conversions','click','CVR')
compare_ads_daily_sum_df = add_custom_proportion_to_df(compare_ads_daily_sum_df,'cost','all conversions','CPA')
compare_ads_daily_sum_df = add_custom_proportion_to_df(compare_ads_daily_sum_df,'all conversion value','all conversions','AOV')


all_combine_df = create_compare_summary_df(ads_daily_sum_df, compare_ads_daily_sum_df,['日期范围','impression','click','cost','all conversions','all conversion value','ads ROI','CPC','CTR','CVR','CPA','AOV'])
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
all_combine_df = all_combine_df.apply(format_comparison, axis=1)
st.dataframe(all_combine_df,width=2000, height=200,column_config=column_config)
