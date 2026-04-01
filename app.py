import streamlit as st
import pubchempy as pcp
import requests

st.set_page_config(page_title="ChemScope", layout="centered")

st.title("ChemScope: Molecule Analysis")
st.write("Search compounds and explore their molecular structure and safety profile.")

compound_name = st.text_input("Enter compound name:")

if st.button("Search"):

    if compound_name.strip() == "":
        st.warning("Please enter a compound name.")

    else:
        try:
            compounds = pcp.get_compounds(compound_name, 'name')

            if not compounds:
                st.error("Compound not found.")

            else:
                compound = compounds[0]
                cid = compound.cid

                st.success("Compound Found!")

                # Basic Info
                st.subheader("Basic Information")

                st.write(f"**IUPAC Name:** {compound.iupac_name}")
                st.write(f"**Formula:** {compound.molecular_formula}")
                st.write(f"**Molecular Weight:** {compound.molecular_weight}")

                # Structure Image
                img_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"

                st.subheader("2D Molecular Structure")
                st.image(img_url, width=300)

                # Interactive 3D Link
                st.subheader("3D Molecular Visualization")

                viewer_url = f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}#section=3D-Conformer"

                st.markdown(
                    f"[🔗 Open Interactive 3D Viewer]({viewer_url})",
                    unsafe_allow_html=True
                )

                # Safety Info
                st.subheader("Safety Information")

                desc_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/description/JSON"
                desc_data = requests.get(desc_url).json()

                try:
                    description = desc_data["InformationList"]["Information"][0]["Description"]
                    st.write(description)

                except:
                    st.write("No detailed description available.")

                st.info("⚠️ Data sourced from PubChem (NCBI). For educational use.")

        except Exception as e:
            st.error("An error occurred while fetching compound data.")
