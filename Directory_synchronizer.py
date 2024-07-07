import streamlit as st
import os

local_dir = "local_dir"
remote_dir = "remote_dir"

def show_files(local_dir):
    # Show the files in the local directory
    st.write("Files in the local directory:")
    local_files = os.listdir(local_dir)
    if len(local_files) == 0:
        st.write("No files in the local directory.")
    else:
        for file in local_files:
            st.write(file)

def show_remote_file(remote_dir):
    # Show the files in the remote directory
    st.write("")
    st.write("Files in the remote directory:")
    remote_files = os.listdir(remote_dir)
    if len(remote_files) == 0:
        st.write("No files in the remote directory.")
    else:
        for file in remote_files:
            st.write(file)

def get_changes(local_dir, remote_dir):
    """
    Compares the local directory to the remote directory and returns a list
    of changes that need to be synchronized.
    Args:
    local_dir (str): The path to the local directory.
    remote_dir (str): The path to the remote directory.
    Returns:
    A list of tuples, where each tuple represents a change that needs to
    be synchronized. The first element of the tuple is the path to the
    changed file or directory, and the second element is a string
    indicating the type of change (added, modified, or deleted).
    """
    changes = []
    # Get the list of files in the local directory
    local_files = set(os.listdir(local_dir))
    # Get the list of files in the remote directory
    remote_files = set(os.listdir(remote_dir))
    # Check for added files
    for file in local_files - remote_files:
        changes.append((os.path.join(local_dir, file), 'added'))
    # Check for deleted files
    for file in remote_files - local_files:
        changes.append((os.path.join(remote_dir, file), 'deleted'))
    # Check for modified files
    for file in local_files & remote_files:
        local_path = os.path.join(local_dir, file)
        remote_path = os.path.join(remote_dir, file)
        if os.path.isfile(local_path) and os.path.isfile(remote_path):
            local_mtime = os.path.getmtime(local_path)
            remote_mtime = os.path.getmtime(remote_path)
            if local_mtime > remote_mtime:
                changes.append((local_path, 'modified'))
        elif os.path.isdir(local_path) and os.path.isdir(remote_path):
            sub_changes = get_changes(local_path, remote_path)
            changes.extend(sub_changes)
    return changes

def send_changes(changes):
    """
    Saves a list of changes to a file on the local machine.
    Args:
    changes (list): A list of tuples, where each tuple represents a change
    that needs to be synchronized. The first element of the tuple is
    the path to the changed file or directory, and the second element
    is a string indicating the type of change (added, modified, or
    deleted).
    Returns:
    True if the changes were successfully saved, False otherwise.
    """
    for change in changes:
        path, change_type = change
        if change_type == 'added' or change_type == 'modified':
            try:
                with open(path, 'rb') as f:
                    data = f.read()
                with open(os.path.join(remote_dir, os.path.basename(path)), 'wb') as f:
                    f.write(data)
            except:
                return False
        elif change_type == 'deleted':
            try:
                os.remove(os.path.join(remote_dir, os.path.basename(path)))
            except:
                return False
    return True

# Define the Streamlit app
def run_app():
    st.title("Directory Synchronizer")
    st.sidebar.write("Go to server to upload a file.")
    # Show the changes that will be synchronized
    
    # if st.button("Get changes"):
    changes = get_changes(local_dir, remote_dir)
    if changes:
            st.write("The following changes will be synchronized:")
            for change in changes:
                st.write(f"{change[0]} ({change[1]})")
    else:
            st.write("The folders are already synchronized.")
    # Synchronize the folders
    # if st.button("Synchronize"):
    changes = get_changes(local_dir, remote_dir)
    success = send_changes(changes)
    if success:
            st.write("The folders have been successfully synchronized.")
    else:
            st.write("There was an error synchronizing the folders.")
    show_remote_file(remote_dir)

if __name__ == "__main__":
    run_app()