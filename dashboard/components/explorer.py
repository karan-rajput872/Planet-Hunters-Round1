"""
Component G: Prediction Explorer
Enterprise Data Management Interface with Live Search, Filter, Sort & Export
"""

import streamlit as st
import pandas as pd
from dashboard.data_loader import load_submission_data, CLASS_METADATA

def render_explorer(theme: str = "light"):
    """Renders the Prediction Explorer table with live search, filters, pagination and safe download."""
    df = load_submission_data().copy()
    total_stars = len(df)
    sub_color = "#94A3B8" if theme == "dark" else "#667085"
    primary_color = "#3B82F6" if theme == "dark" else "#2457D6"

    st.markdown(f"""
    <div class="ph-card ph-card-accent">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
            <div>
                <h2 style="margin: 0 0 4px 0; font-size: 1.35rem;">Prediction Explorer</h2>
                <p style="margin: 0; color: {sub_color}; font-size: 0.88rem;">
                    Examine, search, filter, and inspect individual classifications across all 7,000 test stars.
                </p>
            </div>
            <span class="badge-status badge-telemetry">
                Target Registry: {total_stars:,} Stellar Targets
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filter Controls Bar (4 responsive columns)
    c_search, c_filter, c_sort, c_page = st.columns([1.5, 1.8, 1.3, 1.0])

    with c_search:
        search_id = st.text_input("🔍 Search Star ID", placeholder="e.g. 18042 or 21000", help="Filter by numeric target ID")

    with c_filter:
        class_options = ["All Classes"] + list(CLASS_METADATA.keys())
        selected_class = st.selectbox("Filter Class", options=class_options, index=0)

    with c_sort:
        sort_by = st.selectbox("Sort Order", options=["ID (Ascending)", "ID (Descending)", "Label (A-Z)"], index=0)

    with c_page:
        rows_per_page = st.selectbox("Rows / Page", options=[25, 50, 100], index=0)

    # Apply Filters
    filtered_df = df

    if search_id.strip():
        filtered_df = filtered_df[filtered_df["id"].astype(str).str.contains(search_id.strip())]

    if selected_class != "All Classes":
        filtered_df = filtered_df[filtered_df["label"] == selected_class]

    # Apply Sorting
    if sort_by == "ID (Ascending)":
        filtered_df = filtered_df.sort_values("id", ascending=True)
    elif sort_by == "ID (Descending)":
        filtered_df = filtered_df.sort_values("id", ascending=False)
    elif sort_by == "Label (A-Z)":
        filtered_df = filtered_df.sort_values("label", ascending=True)

    match_count = len(filtered_df)

    # Header bar with filtered match count and Download button
    col_summary, col_dl = st.columns([2.5, 1.5])
    with col_summary:
        st.markdown(f"""
        <div style="padding: 8px 0; font-size: 0.88rem; color: {sub_color};">
            Showing <strong style="color: {primary_color};">{match_count:,}</strong> matching stars out of <strong>{total_stars:,}</strong> test targets
            {"(Filter Active)" if match_count < total_stars else ""}
        </div>
        """, unsafe_allow_html=True)

    with col_dl:
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇ Export Filtered CSV",
            data=csv_data,
            file_name="planet_hunters_filtered_predictions.csv",
            mime="text/csv",
            use_container_width=True,
            help="Exports matching rows to a separate CSV without modifying the original submission candidate."
        )

    # Pagination Logic
    total_pages = max(1, (match_count + rows_per_page - 1) // rows_per_page)

    col_p1, col_p2, col_p3 = st.columns([1, 1.5, 1])
    with col_p2:
        page_num = st.number_input(
            f"Page Navigation (1 to {total_pages})",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1
        )

    start_idx = (page_num - 1) * rows_per_page
    end_idx = min(start_idx + rows_per_page, match_count)
    page_df = filtered_df.iloc[start_idx:end_idx].copy()

    # Add Astrophysical Category display column
    page_df["astrophysical_type"] = page_df["label"].map(lambda x: CLASS_METADATA.get(x, {}).get("scientific_type", "Unknown"))
    page_df["description"] = page_df["label"].map(lambda x: CLASS_METADATA.get(x, {}).get("description", ""))

    # Display clean table
    st.dataframe(
        page_df[["id", "label", "astrophysical_type", "description"]],
        column_config={
            "id": st.column_config.NumberColumn(
                "Star Target ID",
                format="%d",
                width="small"
            ),
            "label": st.column_config.TextColumn(
                "Predicted Label",
                width="medium"
            ),
            "astrophysical_type": st.column_config.TextColumn(
                "Astrophysical Classification",
                width="medium"
            ),
            "description": st.column_config.TextColumn(
                "Phenomenological Description",
                width="large"
            )
        },
        hide_index=True,
        use_container_width=True,
        height=450
    )

    st.markdown(f"""
    <div style="font-size: 0.78rem; color: {sub_color}; text-align: right; margin-top: 6px;">
        Displaying records {start_idx + 1:,}–{end_idx:,} of {match_count:,}
    </div>
    """, unsafe_allow_html=True)
