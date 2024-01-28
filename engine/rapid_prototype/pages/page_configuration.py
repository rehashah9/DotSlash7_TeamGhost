import streamlit as st
from streamlit_image_select import image_select
import time

def main():
    st.title("Add Connect Credentials")

    images=[
        "https://thumbs.dreamstime.com/b/demo-demo-icon-139882881.jpg",
        "https://www.logo.wine/a/logo/Amazon_Web_Services/Amazon_Web_Services-Logo.wine.svg",
        "https://www.logo.wine/a/logo/Microsoft_Azure/Microsoft_Azure-Logo.wine.svg",
        "https://www.logo.wine/a/logo/Google_Cloud_Platform/Google_Cloud_Platform-Logo.wine.svg",
        # "https://www.logo.wine/a/logo/DigitalOcean/DigitalOcean-Logo.wine.svg"
        ]


    img = image_select(
    label="Select Cloud Provider",
    images=images,
    captions=["Demo Test","Amazon Web Service (AWS)", "Microsoft Azure (Azure)", "Google Cloud Platform (GCP)"],
    use_container_width=False
    )

    cloud_profile_name = st.text_input("Create Profile:" , placeholder="Anything you want to name your new Connection")
    # Input box for user to enter text


    st.markdown("---")

    alpha = ""

    if img == images[0]:
        alpha="Demo"
        st.write("Cloud Connection: Demo Test")

    elif img == images[1]:
        alpha="AWS"
        st.write("Cloud Connection: Amazon Web Service (AWS)")
    elif img == images[2]:
        alpha="Azure"
        st.write("Cloud Connection: Microsoft Azure (Azure)")
    elif img == images[3]:
        alpha="GCP"
        st.write("Cloud Connection: Google Cloud Platform (GCP)")

    if alpha == "Demo":
        pass

    elif alpha == "AWS":
        cloud_access_key_id = st.text_input("Access Key ID:" , placeholder="Enter your Access Key ID")
        cloud_secret_access_key = st.text_input("Secret Access Key:" , placeholder="Enter your Secret Access Key")
        cloud_region = st.text_input("Region:" , placeholder="Enter your Region")

        ## Info on how to get the Access Key ID and Secret Access Key
        with st.expander("How to get the Access Key ID and Secret Access Key?"):
            st.info("""
            1. Login to your AWS account.
            2. Click on your username and select **My Security Credentials**.
            3. Click on **Create access key**.
            4. Click on **Show** to view the **Secret access key**.
            5. Copy the **Access key ID** and **Secret access key**.
            
            """)

    elif alpha == "Azure":
        cloud_subscription_id = st.text_input("Subscription ID:" , placeholder="Enter your Subscription ID", disabled=True)
        cloud_client_id = st.text_input("Client ID:" , placeholder="Enter your Client ID", disabled=True)
        cloud_client_secret = st.text_input("Client Secret:" , placeholder="Enter your Client Secret", disabled=True)
        cloud_tenant_id = st.text_input("Tenant ID:" , placeholder="Enter your Tenant ID", disabled=True)
        st.info("We are currently working on the Intergration with Azure. 🚧")

    elif alpha == "GCP":
        cloud_project_id = st.text_input("Project ID:" , placeholder="Enter your Project ID", disabled=True)
        cloud_client_id = st.text_input("Client ID:" , placeholder="Enter your Client ID", disabled=True)
        cloud_client_secret = st.text_input("Client Secret:" , placeholder="Enter your Client Secret", disabled=True)
        cloud_tenant_id = st.text_input("Tenant ID:" , placeholder="Enter your Tenant ID", disabled=True)
        st.info("We are currently working on the Intergration with GCP. 🚧")
    

    
    # Button to submit the input
    if st.button("Let's Go! 🚀"):
        # Action to perform when the button is clicked
        # Show popup with the loading
        with st.spinner("Loading..."):
            # Wait 3 seconds to simulate a delay
            # Make other input boxes disappear
            st.empty()
            time.sleep(3)

if __name__ == "__main__":
    main()