# main.py

import streamlit as st
import os
import json
from datetime import datetime

from input import image_loader
from input.data_loader import load_tabular_file
from input.image_loader import load_image, load_pdf_as_images
from input.data_loader import *
from pipelines.data_pipeline import *
from pipelines.data_query_pipelines import *
from pipelines.data_query_pipelines import *
from pipelines.images_query_pipeline import image_query
from pipelines.graph_pipeline import get_model



#########----------------------Streamlit------------#######
# ======================================================
# CONFIG
# ======================================================
st.set_page_config(page_title="Chart Insight Generator", layout="wide")
st.markdown("""
    <style>
        /* Base button style */
        .stButton button {
            background-color: #66ccff !important;  /* Light blue */
            color: white !important;              /* White text */
        }

        /* Hover */
        .stButton button:hover {
            background-color: #3399ff !important; /* Medium blue on hover */
        }

        /* Active / Clicked */
        .stButton button:active {
            background-color: #005b99 !important; /* Dark blue when clicked */
        }

        /* Sidebar style */
        .stSidebar .sidebar-content {
            background-color: #003366 !important; 
            color: #ffffff !important;
        }
        
        .stTextArea textarea {
            background-color: #e6f7ff !important;
            color: #003366 !important;
        }

        .stDataFrame thead th {
            background-color: #005b99 !important;
            color: white !important;
        }
         /* Increase the title size */
    .css-1d391kg h2 { 
        font-size: 1.4em; 
        font-weight: bold; 
        color: #003366;
    }

    /* Radio buttons text style */
    div[data-baseweb="radio"] label {
        font-size: 16px !important;
        font-weight: bold !important;
        color: #003366 !important;
        padding: 8px 12px;
    }

    /* Selected option background */
    div[data-baseweb="radio"] input:checked + label {
        background-color: #66ccff !important;  /* Light blue */
        color: #003366 !important;             /* Dark text */
        border-radius: 6px;
    }

    /* Hover effect */
    div[data-baseweb="radio"] label:hover {
        background-color: #3399ff !important;  /* Medium blue */
        color: white !important;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

BASE_INPUT_DIR = "input"
CHART_IMAGE_DIR = os.path.join(BASE_INPUT_DIR, "charts", "raw_images")
RAW_DATA_DIR = os.path.join(BASE_INPUT_DIR, "data", "raw_files")
QUERY_LOG_PATH = os.path.join(BASE_INPUT_DIR, "user_queries", "queries.json")

os.makedirs(CHART_IMAGE_DIR, exist_ok=True)
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(os.path.dirname(QUERY_LOG_PATH), exist_ok=True)

# ======================================================
# CACHE WRAPPERS (NO RELOAD ON QUERY SUBMIT)
# ======================================================
@st.cache_data(show_spinner=False)
def cached_load_tabular(uploaded_file):
    return load_tabular_file(uploaded_file)

@st.cache_data(show_spinner=False)
def cached_load_image(uploaded_file):
    return load_image(uploaded_file)

@st.cache_data(show_spinner=False)
def cached_load_pdf(uploaded_file):
    return load_pdf_as_images(uploaded_file)

## Model_load
m1 = get_model()
# ======================================================
# HELPERS
# ======================================================
def save_uploaded_file(uploaded_file, target_dir):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(target_dir, f"{timestamp}_{uploaded_file.name}")
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

def save_query(query_text, mode):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "mode": mode,
        "query": query_text
    }

    if os.path.exists(QUERY_LOG_PATH):
        with open(QUERY_LOG_PATH, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(QUERY_LOG_PATH, "w") as f:
        json.dump(data, f, indent=2)

# ======================================================
# UI
# ======================================================
st.title("Maritime Decision Intelligence System")

mode = st.sidebar.radio(
    "Select Input Type",
    ["Upload Raw Data (CSV/Excel)", "Upload Chart Image / PDF"]
)
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

# Maritime-specific instructions in bold
if mode == "Upload Raw Data (CSV/Excel)":
    st.sidebar.markdown("**⚓ Upload your maritime CSV or Excel data to generate actionable insights for smarter decision-making at sea.**")
elif mode == "Upload Chart Image / PDF":
    st.sidebar.markdown("**⚓ Upload maritime charts or PDFs to extract visual insights for informed navigational or operational decisions.**")
# CLEAR OTHER STATES WHEN SWITCHING MODES
if mode == "Upload Raw Data (CSV/Excel)":
    # remove image-related session state
    for key in ["chart_images", "chart_image_paths", "selected_image_index", "chart_file_name"]:
        if key in st.session_state:
            del st.session_state[key]

# ======================================================
# MODE 1: RAW DATA INPUT
# ======================================================
if mode == "Upload Raw Data (CSV/Excel)":

    st.subheader("📁 Upload CSV or Excel File")

    uploaded_file = st.file_uploader(
        "Upload your data file",
        type=["csv", "xlsx", "xls"],
        key="raw_upload"
    )

    # ---------- UPLOAD (ONCE) ----------
    if uploaded_file:
        if (
        "raw_file_name" not in st.session_state
        or st.session_state["raw_file_name"] != uploaded_file.name
    ):
            # NEW FILE → RESET STATE
            st.session_state.pop("raw_df", None)
            st.session_state.pop("table_name", None)
            st.session_state.pop("raw_data_path", None)
            saved_path = save_uploaded_file(uploaded_file, RAW_DATA_DIR)
            df,file_name = cached_load_tabular(uploaded_file)

            st.session_state["raw_df"] = df
            st.session_state['table_name'] = file_name
            st.session_state["raw_data_path"] = saved_path

            # st.success("File uploaded and saved once")

    # ---------- DISPLAY ----------
    if "raw_df" in st.session_state:
        df = st.session_state["raw_df"]


        st.write("### Preview of Data")
        st.dataframe(df.head())

        st.write("### Basic Info")
        st.write(df.describe(include="all"))

        st.divider()
        st.subheader("🧠 Ask a Question")

        user_query = st.text_area(
            "Enter your analysis question",
            height=120,
            key="raw_query"
        )

    if st.button("Submit Query", key="raw_submit"):
        if not user_query.strip():
            st.warning("Please enter a query")
        else:
            # save query
            save_query(user_query, mode)

            # df,query = df_query(df,user_query)
            # print(df)
            # print(query)
            
            # # ---------- RUN PIPELINE HERE ----------
            # processed_df, schema, summary = run_data_pipeline(
            #     st.session_state["raw_df"],
            #     drop_duplicates=True,
            #     drop_nulls=False,
            #     fill_missing=True,
            # )

            # # store for later use
            # st.session_state["processed_df"] = processed_df
            # st.session_state["schema"] = schema
            # st.session_state["summary"] = summary

            # # TERMINAL OUTPUT ONLY
            # print("\n========== USER QUERY ==========")
            # print(user_query)

            # print("\n========== DATASET SCHEMA ==========")
            # print(schema)

            # print("\n========== DATASET SUMMARY ==========")
            # print(summary)

            st.success("Query submitted and processed")
            sql_result, final_answer,sql_query = m1.graph_sql_pipe(
                                                        dataframe=st.session_state["raw_df"],
                                                        user_query=user_query,
                                                        table_name=st.session_state["table_name"]
                                                    )
            st.subheader("Results")
            st.success(sql_result)
            st.success(sql_query)
            st.success(final_answer)
            
                                                                

# ======================================================
# MODE 2: IMAGE / PDF INPUT
# ======================================================
elif mode == "Upload Chart Image / PDF":

    st.subheader("🖼 Upload Chart Image or PDF")

    uploaded_file = st.file_uploader(
        "Upload chart image or PDF",
        type=["png", "jpg", "jpeg", "pdf"],
        key="chart_upload"
    )

    # ---------- UPLOAD (ONCE) ----------
    if uploaded_file:
    # detect NEW upload
        if (
            "chart_file_name" not in st.session_state
            or st.session_state["chart_file_name"] != uploaded_file.name
        ):
            # ---------- RESET OLD STATE ----------
            st.session_state.pop("chart_images", None)
            st.session_state.pop("chart_image_paths", None)
            st.session_state.pop("selected_image_index", None)

            image_paths = []

            # ---------- LOAD NEW FILE ----------
            if uploaded_file.name.lower().endswith(".pdf"):
                images = cached_load_pdf(uploaded_file)

                for i, img in enumerate(images):
                    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                    path = os.path.join(
                        CHART_IMAGE_DIR,
                        f"{timestamp}_page_{i+1}.png"
                    )
                    img.save(path)
                    image_paths.append(path)

            else:
                img = cached_load_image(uploaded_file)

                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                path = os.path.join(
                    CHART_IMAGE_DIR,
                    f"{timestamp}_{uploaded_file.name}"
                )
                img.save(path)

                images = [img]
                image_paths.append(path)

            # ---------- STORE STATE ----------
            st.session_state["chart_images"] = images
            st.session_state["chart_image_paths"] = image_paths
            st.session_state["chart_file_name"] = uploaded_file.name
            st.session_state["selected_image_index"] = 0

            st.success("New chart uploaded and saved")


# ---------- DISPLAY ----------
if "chart_images" in st.session_state:

    st.subheader("📄 Uploaded Charts")

    # initialize selection
    if "selected_image_index" not in st.session_state:
        st.session_state["selected_image_index"] = 0

    cols = st.columns(3)

    for i, img in enumerate(st.session_state["chart_images"]):
        with cols[i % 3]:
            if st.button(f"Select {i+1}", key=f"select_chart_{i}"):
                st.session_state["selected_image_index"] = i

            st.image(
                img,
                caption=f"Chart {i+1}",
                use_container_width=True
            )

    st.divider()
    st.subheader("🧠 Ask a Question")

    user_query = st.text_area(
        "Enter your analysis question",
        height=120,
        key="chart_query"
    )

    if st.button("Submit Query", key="chart_submit"):
        if not user_query.strip():
            st.warning("Please enter a query")
        else:
            save_query(user_query, mode)
            st.success("Query submitted")

            # ✅ USE SELECTED IMAGE
            idx = st.session_state.get("selected_image_index", 0)
            selected_image = st.session_state["chart_images"][idx]

            image, query = image_query(selected_image, user_query)

            vision_result, final_result = m1.graph_vision_pipe(
                image=image,
                user_query=query
            )

            with st.expander("View Vision Analysis Details"):
                st.write(vision_result)

            st.subheader("Results")
            st.success(final_result)












