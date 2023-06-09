import streamlit as st
import pandas as pd
#import numpy as np
# import math
# import altair as alt
# from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode, JsCode
from streamlit_extras.switch_page_button import switch_page


#@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    # - this is not possible here - needs to change csv header every time
    return df.to_csv().encode('utf-8')


# -----Page Configuration
st.set_page_config(page_title="2D Helmert Transformation", page_icon="🌐", layout="wide")


# style settings, slightly different from other pages which use style.css
st.markdown('''
<style>
.katex-html {
    text-align: left;
    margin-top:-1rem;
}
[data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 170px;
           max-width: 285px;
       }
div[data-testid="stExpander"] div[role="button"] p {
    font-size: 1.5rem;
    font-weight: 700;
}
button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
    font-size: 1.5rem;
    font-weight: 700;
}
.text-center {
  text-align: center;
}
</style>''',
unsafe_allow_html=True
)


# ---- Title and Description
st.markdown('<h1 style="margin-bottom:2rem;margin-top:-5rem;text-align: center">2D Helmert Transformation</h1>',unsafe_allow_html=True,)
#st.markdown('<h1 style="margin-bottom:0rem;margin-top:-4rem;text-align: center">2D Helmert Transformation</h1>',unsafe_allow_html=True,)

col1, col2 = st.columns([2,1],gap="medium")

try:
    number_of_cp_columns = len(st.session_state.common_points_df.columns)
except:
    switch_page("Upload_Coordinates")

if number_of_cp_columns == 6:
    col1.error("Please select common points first", icon="⚠️")
    button_Common_Points= col1.button(
            """**Select Common Points**""",
            key="StartTrafo5",
            help=None,

            on_click=None,
            args=None,
            type="primary",
            disabled=False,
        )
    if button_Common_Points:
        switch_page("Select_Common_Points")
else: #calculate transformed point df and generate output text report
    transformed_points_df=st.session_state.all_points_df[['Name','y_1','x_1','Selected']].copy()
    transformed_points_df["y_new"] = st.session_state.Y0 + st.session_state.b * transformed_points_df["x_1"] + st.session_state.a * transformed_points_df["y_1"]
    transformed_points_df["x_new"] = st.session_state.X0 + st.session_state.a * transformed_points_df["x_1"] - st.session_state.b * transformed_points_df["y_1"]
    transformed_points_df.sort_values(by=['Selected','Name'], inplace=True)

    header_list = st.session_state.source_header_names[:3]
    header_list.append('Selected')

    header_list.append(st.session_state.source_header_names[1] + "_new")
    header_list.append(st.session_state.source_header_names[2] + "_new")
    #header_list_source=st.session_state.source_header_names[:3]
    #header_list_source=header_list[:4]

    #header_list_target=["Name",st.session_state.source_header_names[1]+"_new",st.session_state.source_header_names[2]+"_new"]
    if st.session_state.text_length < len(header_list[0]):
        st.session_state.text_length = len(header_list[0])


    # Formatting Text Output File
    list_lines = []
    list_lines.append("\n")
    list_lines.append((st.session_state.text_length - 4) * " " + "                        2D Helmert Transformation")
    list_lines.append("\n")
    list_lines.append("\n")
    list_lines.append((st.session_state.text_length - 4) * " " + "                              Common Points")
    list_lines.append((st.session_state.text_length - 4) * " " + "                             ---------------")
    list_lines.append("\n")
    list_lines.append((st.session_state.text_length - 4) * " " + "                Source Coordinates        Target Coordinates")
    list_lines.append("   {0:{width}}  {1:>12} {2:>12} {3:>12} {4:>12} {5:>8} {6:>8}"
              .format(header_list[0],
                      header_list[1],header_list[2],
                      header_list[1],header_list[2],
                      "v" + header_list[1],"v" + header_list[2],
                      width=st.session_state.text_length))
    list_lines.append("\n")
    for i in st.session_state.common_points_df[st.session_state.common_points_df.Selected].index:
        list_lines.append("   {0:{width}}  {1:>12.3f} {2:>12.3f} {3:>12.3f} {4:>12.3f} {5:>8.3f} {6:>8.3f}"
              .format(st.session_state.common_points_df.loc[i,"Name"],
                      st.session_state.common_points_df.loc[i,"y_1"],st.session_state.common_points_df.loc[i,"x_1"],
                      st.session_state.common_points_df.loc[i,"y_2"],st.session_state.common_points_df.loc[i,"x_2"],
                      st.session_state.common_points_df.loc[i,"vy"],st.session_state.common_points_df.loc[i,"vx"],
                      width=st.session_state.text_length))
    list_lines.append("\n")
    list_lines.append("   ----" + (st.session_state.text_length - 4) * "-" + "-----------------------------------------------------------------------")
    list_lines.append("   Mean:" + (st.session_state.text_length - 4) * " " + " {0:>12.3f} {1:>12.3f} {2:>12.3f} {3:>12.3f}"
          .format(st.session_state.mean_source_y,st.session_state.mean_source_x,
                  st.session_state.mean_target_y,st.session_state.mean_target_x))
    list_lines.append("   Shift:" + (st.session_state.text_length - 4) * " " + "{0:>12.3f} {1:>12.3f}"
          .format(st.session_state.mean_target_y-st.session_state.mean_source_y,st.session_state.mean_target_x-st.session_state.mean_source_x))
    list_lines.append("\n")
    if st.session_state.stdev is None:
        list_lines.append("   Standard Deviation (m): ---")
    else:
        list_lines.append("   Standard Deviation (m): {:>6.3f}".format(st.session_state.stdev))

    list_lines.append("\n")

    list_lines.append("   Scale: {:0.8f}  Rotation: {}".format(st.session_state.scale,st.session_state.rotation_dms))
    list_lines.append("\n")

    list_lines.append("   Transformation Parameters:  Y0: {:>10.3f}  A: {:>11.8f}".format(st.session_state.Y0,st.session_state.a))
    list_lines.append("                               X0: {:>10.3f}  B: {:>11.8f}".format(st.session_state.X0,st.session_state.b))
    list_lines.append("   ----"+(st.session_state.text_length - 4) * "-" + "-----------------------------------------------------------------------")
    # transformed points
    list_lines.append("\n")
    list_lines.append("\n")
    list_lines.append((st.session_state.text_length - 4) * " " + "                           Transformed Points")
    list_lines.append((st.session_state.text_length - 4) * " " + "                          --------------------")
    list_lines.append("\n")
    list_lines.append((st.session_state.text_length - 4) * " " + "                Source Coordinates        Target Coordinates")
    #list_lines.append("   Name"+(st.session_state.text_length-4)*" "+"        y            x           y_new        x_new")
    list_lines.append("   {0:{width}}  {1:>12} {2:>12} {3:>12} {4:>12}"
              .format(header_list[0],
                      header_list[1],header_list[2],
                      header_list[-2],header_list[-1],
                      width=st.session_state.text_length))
    list_lines.append("\n")
    for i in transformed_points_df[~transformed_points_df.Selected].index:
        list_lines.append("   {0:{width}}  {1:>12.3f} {2:>12.3f} {3:>12.3f} {4:>12.3f}"
              .format(transformed_points_df.loc[i,"Name"],transformed_points_df.loc[i,"y_1"],transformed_points_df.loc[i,"x_1"],
                      transformed_points_df.loc[i,"y_new"],transformed_points_df.loc[i,"x_new"],
                      width=st.session_state.text_length))
    list_lines.append("\n")

    #output_text for file download
    output_text = "\r\n".join(list_lines)

    list_lines2 = [s for s in list_lines if s != "\n"]

    #display text needs to be different because of line breaks
    display_text = "\n".join(list_lines2)


    with col1:
        exp2 = st.expander("Transformation Report:",expanded=True)
        exp2.text("-" + display_text[1:])

        st.download_button(
           label="""**Download Transformation Report**""",
           data=output_text,
           file_name='test.txt',
           mime='text'
        )

    with col2:
        transformed_points_df = transformed_points_df.round(3) # necessary for csv export
        transformed_points_df.columns = header_list

        target_output_format = {}
        target_output_format[header_list[1]]= "{:.3f}"
        target_output_format[header_list[2]]= "{:.3f}"
        target_output_format[header_list[4]]= "{:.3f}"
        target_output_format[header_list[5]]= "{:.3f}"

        st.markdown('<h3 style="margin-bottom:0rem;margin-top:0.3rem">Transformed Points:</h3>',unsafe_allow_html=True)

        radio_cp = st.radio("Select:",("without Common Points","with Common Points" ),label_visibility="collapsed")
        if radio_cp == "without Common Points":
            if len(transformed_points_df[~transformed_points_df.Selected]) < 6:
                st.dataframe(transformed_points_df[~transformed_points_df.Selected].reset_index(drop=True).iloc[:, [0] + [-2] + [-1]].style.format(target_output_format))
            else:
                st.dataframe(transformed_points_df[~transformed_points_df.Selected].reset_index(drop=True).iloc[:, [0] + [-2] + [-1]].style.format(target_output_format), height=235)
            csv = convert_df(transformed_points_df[~transformed_points_df.Selected].set_index(header_list[0]).iloc[:, [-2] + [-1]])
        else:
            if len(transformed_points_df)<6:
                st.dataframe(transformed_points_df.sort_values(by=[header_list[0]]).reset_index(drop=True).iloc[:, [0] + [-2] + [-1]].style.format(target_output_format))
            else:
                st.dataframe(transformed_points_df.sort_values(by=[header_list[0]]).reset_index(drop=True).iloc[:, [0] + [-2] + [-1]].style.format(target_output_format), height=235)
            csv = convert_df(transformed_points_df.sort_values(by=[header_list[0]]).set_index(header_list[0]).iloc[:, [-2] + [-1]])

        st.download_button(
           label="""**Download Transformed Points as csv file**""",
           data=csv,
           file_name='transformed_points.csv',
           mime='text/csv',
        )
