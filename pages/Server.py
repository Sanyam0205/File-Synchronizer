import os
import streamlit as st

def show_files(local_dir):
    # Show the files in the local directory
    st.write("Files in the local directory:")
    local_files = os.listdir(local_dir)
    if len(local_files) == 0:
        st.write("No files in the local directory.")
    else:
        for custom_file in local_files:
            st.write(custom_file)
    return local_files

def delete_file(local_dir, filename):
    file_path = os.path.join(local_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        st.success(f"File '{filename}' deleted.")
    else:
        st.warning(f"File '{filename}' not found.")

# Define a callback function to handle file uploads
def handle_file_upload(local_dir,file):
    if file is not None:
        # Save the uploaded file to the local directory
        file_path = os.path.join(local_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())
        # Display a success message
        st.success(f"File '{file.name}' uploaded")

# Define the user interface and behavior of the app
def main():
    st.title("Directory Synchronizer")
    # Set the local and remote directories
    local_dir = st.text_input("Enter the local directory path:", "D:/projects/file_sync/local_dir")
    remote_dir = st.text_input("Enter the remote directory path:", "D:/projects/file_sync/remote_dir")
    # Check that the directories exist and are writable
    if not os.path.isdir(local_dir):
        st.error("The local directory does not exist.")
        return
    if not os.access(local_dir, os.W_OK):
        st.error("The local directory is not writable.")
        return
    if not os.path.isdir(remote_dir):
        st.error("The remote directory does not exist.")
        return
    if not os.access(remote_dir, os.W_OK):
        st.error("The remote directory is not writable.")
        return
    # Add a file uploader to the app
    st.write("Upload a file to synchronize with the remote directory.")
    uploaded_file = st.file_uploader("Choose a file", type=None)
    st.write("")
    st.write("")
    # Call the file upload callback function when a file is uploaded
    if st.button("Upload"):
        handle_file_upload(local_dir,uploaded_file)
        show_files(local_dir)
    # Display a list of available files
    available_files = os.listdir(local_dir)
    selected_files = st.multiselect("Select files to delete:", available_files)
    # Display a button to delete the selected files
    if st.button("Delete files"):
        for filename in selected_files:
            delete_file(local_dir,filename)

# Run the app
if __name__ == "__main__":
    main()