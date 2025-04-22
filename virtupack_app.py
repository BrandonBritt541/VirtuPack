
import streamlit as st
import plotly.graph_objects as go
import json

st.set_page_config(page_title="VirtuPack", layout="wide")
st.title("📦 VirtuPack – Virtual Packaging Simulator")

tab = st.sidebar.radio("Navigation", ["Product", "Box", "Material", "Testing", "3D Preview", "Export"])

for key, default in {
    "product_name": "Chair Arm",
    "product_length": 100,
    "product_width": 80,
    "product_height": 50,
    "fragility": 50,
    "materials_used": ["Plastic"],
    "box_type": "FEFCO 0201",
    "box_length": 300,
    "box_width": 200,
    "box_height": 150,
    "wall_thickness": 3.0,
    "material_type": "PaperWrap",
    "gsm": 80,
    "air_count": 5,
    "foam_fill": 15,
    "corr_flute": "C",
    "drop_test": 94,
    "vibration_test": 82,
    "compression_test": 90,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

if tab == "Product":
    st.subheader("🧱 Product Setup")
    st.session_state["product_name"] = st.text_input("Product Name", st.session_state["product_name"])
    st.session_state["product_length"] = st.slider("Length (mm)", 10, 500, st.session_state["product_length"])
    st.session_state["product_width"] = st.slider("Width (mm)", 10, 500, st.session_state["product_width"])
    st.session_state["product_height"] = st.slider("Height (mm)", 10, 500, st.session_state["product_height"])
    st.session_state["fragility"] = st.slider("Fragility Score", 0, 100, st.session_state["fragility"])
    st.session_state["materials_used"] = st.multiselect(
        "Materials Used", ["Glass", "Wood", "Plastic", "Metal", "Foam", "Electronics"],
        default=st.session_state["materials_used"]
    )

elif tab == "Box":
    st.subheader("📦 Box Setup")
    st.session_state["box_type"] = st.selectbox("Box Type", ["FEFCO 0201", "FEFCO 0300", "FEFCO 0427", "Custom"],
                                                index=["FEFCO 0201", "FEFCO 0300", "FEFCO 0427", "Custom"].index(st.session_state["box_type"]))
    st.session_state["box_length"] = st.slider("Box Length (mm)", 100, 1000, st.session_state["box_length"])
    st.session_state["box_width"] = st.slider("Box Width (mm)", 100, 1000, st.session_state["box_width"])
    st.session_state["box_height"] = st.slider("Box Height (mm)", 100, 1000, st.session_state["box_height"])
    st.session_state["wall_thickness"] = st.slider("Wall Thickness (mm)", 1.0, 10.0, st.session_state["wall_thickness"])

elif tab == "Material":
    st.subheader("📦 Material Config")
    st.session_state["material_type"] = st.selectbox("Material Type", ["PaperWrap", "AirPillow", "FoamInPlace", "CorrugateInsert"],
                                                     index=["PaperWrap", "AirPillow", "FoamInPlace", "CorrugateInsert"].index(st.session_state["material_type"]))
    if st.session_state["material_type"] == "PaperWrap":
        st.session_state["gsm"] = st.slider("Paper GSM", 20, 200, st.session_state["gsm"])
    elif st.session_state["material_type"] == "AirPillow":
        st.session_state["air_count"] = st.slider("Air Pillows Count", 1, 20, st.session_state["air_count"])
    elif st.session_state["material_type"] == "FoamInPlace":
        st.session_state["foam_fill"] = st.slider("Foam Fill %", 0, 100, st.session_state["foam_fill"])
    elif st.session_state["material_type"] == "CorrugateInsert":
        st.session_state["corr_flute"] = st.selectbox("Flute Type", ["B", "C", "E"], index=["B", "C", "E"].index(st.session_state["corr_flute"]))

elif tab == "Testing":
    st.subheader("🧪 ISTA Test Simulation")
    st.session_state["drop_test"] = st.slider("Drop Test (%)", 0, 100, st.session_state["drop_test"])
    st.session_state["vibration_test"] = st.slider("Vibration Test (%)", 0, 100, st.session_state["vibration_test"])
    st.session_state["compression_test"] = st.slider("Compression Test (%)", 0, 100, st.session_state["compression_test"])

elif tab == "3D Preview":
    st.subheader("📊 3D Visualization")
    fig = go.Figure()
    bl, bw, bh = st.session_state["box_length"], st.session_state["box_width"], st.session_state["box_height"]
    pl, pw, ph = st.session_state["product_length"], st.session_state["product_width"], st.session_state["product_height"]
    fig.add_trace(go.Mesh3d(
        x=[0, bl, bl, 0, 0, bl, bl, 0],
        y=[0, 0, bw, bw, 0, 0, bw, bw],
        z=[0, 0, 0, 0, bh, bh, bh, bh],
        color='lightgray', opacity=0.2, name='Box'
    ))
    fig.add_trace(go.Mesh3d(
        x=[50, 50+pl, 50+pl, 50, 50, 50+pl, 50+pl, 50],
        y=[50, 50, 50+pw, 50+pw, 50, 50, 50+pw, 50+pw],
        z=[10, 10, 10, 10, 10+ph, 10+ph, 10+ph, 10+ph],
        color='red', opacity=0.7, name='Product'
    ))
    fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
    st.plotly_chart(fig, use_container_width=True)

elif tab == "Export":
    st.subheader("📤 Export Configuration")
    summary = {
        "product": {
            "name": st.session_state["product_name"],
            "dimensions_mm": [st.session_state["product_length"], st.session_state["product_width"], st.session_state["product_height"]],
            "fragility": st.session_state["fragility"],
            "materials": st.session_state["materials_used"]
        },
        "box": {
            "type": st.session_state["box_type"],
            "dimensions_mm": [st.session_state["box_length"], st.session_state["box_width"], st.session_state["box_height"]],
            "wall_thickness_mm": st.session_state["wall_thickness"]
        },
        "packaging": {
            "type": st.session_state["material_type"],
            "paper_gsm": st.session_state["gsm"],
            "air_pillows": st.session_state["air_count"],
            "foam_fill_pct": st.session_state["foam_fill"],
            "flute": st.session_state["corr_flute"]
        },
        "tests": {
            "drop": st.session_state["drop_test"],
            "vibration": st.session_state["vibration_test"],
            "compression": st.session_state["compression_test"],
            "confidence_score": round((st.session_state["drop_test"] + st.session_state["vibration_test"] + st.session_state["compression_test"]) / 3, 2)
        }
    }
    st.json(summary)
    st.download_button("Download JSON", data=json.dumps(summary, indent=2), file_name="virtupack_simulation.json", mime="application/json")
