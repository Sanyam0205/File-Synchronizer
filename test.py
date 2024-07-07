import streamlit as st
st.title("Directory Synchronizer")
st.sidebar.write("Go to server to upload a file.")
    # Show the changes that will be synchronized
    
if st.button("Get changes"):
        changes = get_changes(local_dir, remote_dir)
        if changes:
            st.write("The following changes will be synchronized:")
            for change in changes:
                st.write(f"{change[0]} ({change[1]})")
        else:
            st.write("The folders are already synchronized.")
    # Synchronize the folders
if st.button("Synchronize"):
        changes = get_changes(local_dir, remote_dir)
        success = send_changes(changes)
        if success:
            st.write("The folders have been successfully synchronized.")
        else:
            st.write("There was an error synchronizing the folders.")
