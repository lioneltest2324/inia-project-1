import streamlit as st
import pandas as pd
from universal_component_for_campaign import load_and_process_data,process_usfeed_and_hmfeed_sku_on_ads_data,process_hk_cost_and_value_on_ads_data,\
    process_old_new_sku_2022_and_2023_on_ads_data,merged_spu_to_sku_on_ads_data,merged_imagelink_to_sku_on_ads_data,create_date_filtered_df,\
    output_groupby_df,out_date_range_data,add_groupby_sum_columns_to_list_df,create_dynamic_column_setting,add_custom_proportion_to_df,add_custom_proportion_to_df_x100,\
    create_sensor_gmv_filter_input,create_bulk_sku_input,create_sensor_campaign_filter_input_df,condition_evaluate,merged_saleprice_to_sku_on_ads_data,\
    create_compare_summary_df,format_first_two_rows,format_comparison,colorize_comparison
st.set_page_config(layout="wide")
# ---------------------------------------------------------------------基础数据处理区开始---------------------------------------------------------------------------------------------------
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
column_config['buy CVR'] = st.column_config.NumberColumn(
    format='%.2f%%',  # 显示为百分比
    min_value=0,
    max_value=1,
            )
column_config['atc CVR'] = st.column_config.NumberColumn(
    format='%.2f%%',  # 显示为百分比
    min_value=0,
    max_value=1,
            )


ads_cost_url = 'https://docs.google.com/spreadsheets/d/1Dhq7TCw04r8UFkikGuyhdGy4aHqMXHKGxcTkrcyiVzA/edit?gid=0#gid=0'
ads_conversion_url = 'https://docs.google.com/spreadsheets/d/19avn6L_DlOnDWU4xWuKvCpBZPhg_702e6BguLD5Ec58/edit?gid=1848692976#gid=1848692976'
ads_campaign_daily = load_and_process_data(ads_cost_url,0)
ads_conversion_daily = load_and_process_data(ads_conversion_url,1848692976)
ads_campaign_daily = ads_campaign_daily[['Date','Campaign Name','impression','click','cost']]
ads_campaign_daily  = ads_campaign_daily[~ads_campaign_daily.isnull().all(axis=1)]
unique_conversion_action = ads_conversion_daily['conversion action'].unique()

ads_campaign_daily = output_groupby_df(ads_campaign_daily,['Date'], ['impression','cost','click'], 'sum').reset_index()
ads_conversion_daily = output_groupby_df(ads_conversion_daily,['Date','conversion action'], ['all conversions','all conversion value'], 'sum').reset_index()
combine_campaign_df = pd.merge(ads_conversion_daily,ads_campaign_daily,on=['Date'], how='left')


before_combine_df = pd.merge(ads_campaign_daily,ads_conversion_daily,on=['Date'], how='left')
buy_combine_df = before_combine_df[before_combine_df['conversion action'].isin(["Purchase"])]
atc_combine_df = before_combine_df[before_combine_df['conversion action'].isin(["Add to cart"])]
atc_combine_df = atc_combine_df.drop(columns=['impression','cost','click','conversion action'])
buy_combine_df['buy conversions'] = buy_combine_df['all conversions']
buy_combine_df['buy value'] = buy_combine_df['all conversion value']
buy_combine_df = buy_combine_df.drop(columns=['all conversions','all conversion value','conversion action'])
all_combine_action_df = pd.merge(buy_combine_df,atc_combine_df,on=['Date'], how='left')
all_combine_action_df = all_combine_action_df.drop(columns=['all conversion value'])
all_combine_action_df['atc conversions'] = all_combine_action_df['all conversions']
all_combine_action_df = all_combine_action_df.drop(columns=['all conversions'])
all_combine_action_df= add_custom_proportion_to_df(all_combine_action_df,'buy value','cost','ads ROI')
all_combine_action_df= add_custom_proportion_to_df(all_combine_action_df,'cost','click','CPC')
all_combine_action_df= add_custom_proportion_to_df_x100(all_combine_action_df,'click','impression','CTR')
all_combine_action_df = add_custom_proportion_to_df_x100(all_combine_action_df,'buy conversions','click','buy CVR')
all_combine_action_df = add_custom_proportion_to_df_x100(all_combine_action_df,'atc conversions','click','atc CVR')
all_combine_action_df = add_custom_proportion_to_df(all_combine_action_df,'cost','buy conversions','buy CPA')
all_combine_action_df = add_custom_proportion_to_df(all_combine_action_df,'cost','atc conversions','atc CPA')
st.dataframe(all_combine_action_df,width=1800, height=600,column_config=column_config)

conversion_action_options = st.multiselect(
    '选择转化操作',
    unique_conversion_action,
    ['Purchase']
)
combine_campaign_df = combine_campaign_df[combine_campaign_df['conversion action'].isin(conversion_action_options)]
ads_daliy_summary_df = output_groupby_df(combine_campaign_df,['Date'], ['impression','cost','click','all conversions','all conversion value'], 'sum').reset_index()
ads_daliy_summary_df= add_custom_proportion_to_df(ads_daliy_summary_df,'all conversion value','cost','ads ROI')
ads_daliy_summary_df= add_custom_proportion_to_df(ads_daliy_summary_df,'cost','click','CPC')
ads_daliy_summary_df = add_custom_proportion_to_df_x100(ads_daliy_summary_df,'click','impression','CTR')
ads_daliy_summary_df = add_custom_proportion_to_df_x100(ads_daliy_summary_df,'all conversions','click','CVR')
ads_daliy_summary_df = add_custom_proportion_to_df(ads_daliy_summary_df,'cost','all conversions','CPA')

st.dataframe(ads_daliy_summary_df,width=1800, height=800,column_config=column_config)
