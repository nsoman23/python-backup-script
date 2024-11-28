# Backup and Upload Script

This Python script automates the process of creating backups for directories or files, compressing them into tar archives, and securely uploading the archives to a remote server using SFTP. It verifies data integrity using MD5 hash values to ensure the backup's consistency.

---

## Features

- **Automatic Backup**: Compresses directories or files into `.tar.gz` archives.
- **SFTP Upload**: Transfers the archives securely to a remote server.
- **Data Integrity Verification**: Ensures that the backup file's MD5 hash matches on both the local and remote servers.
- **Error Handling**: Automatically removes corrupted backups from the remote server if hash values do not match.

---

## Prerequisites

- Python 3.x
- Libraries:
  - `pysftp`
  - `paramiko` (dependency for `pysftp`)
- SSH key-based authentication enabled for the remote server.

Install the required libraries using:
```bash
pip install pysftp 
```
---

## Configuration

Edit the following variables in the script before running:

- `sourceDir`: The local directory containing the files/directories to back up.
- `remote_host`: The IP address or hostname of the remote server.
- `remote_user`: The SSH username for the remote server.
- `remote_port`: The SSH port (default is 22).
- `remote_key`: The path to the private SSH key file.
- `remote_dir`: The directory on the remote server where backups will be stored.

---

## How It Works

1. Backup Generation:

- The script iterates over the contents of `sourceDir`.
 - Each file or directory is compressed into a `.tar.gz` archive with a timestamped name.
2. Uploading Backups:

- The archive is uploaded to the remote server using SFTP.
3. Hash Verification:

- The script calculates the MD5 hash of the local archive before uploading.
- After uploading, it retrieves the remote file's MD5 hash and compares it to the local hash.
4. Error Handling:

-  If the hash values do not match, the uploaded file is removed from the remote server.

---

## Running the Script

After configuring the script, run it with:

```Bash
python3 backup_script.py
```

---

## Example Output

```Bash
hash values of source and destination files matched
Hash value before upload: d41d8cd98f00b204e9800998ecf8427e
Hash value after upload: d41d8cd98f00b204e9800998ecf8427e
upload completed: /tmp/sample-12-11-2024-10:15:30.tar.gz --> /backups/sample-12-11-2024-10:15:30.tar.gz
```

**If the hashes do not match:**

```Bash
hash value of the files /tmp/sample-12-11-2024-10:15:30.tar.gz and /backups/sample-12-11-2024-10:15:30.tar.gz don't match so removing the file from the remote server
remote backup file /backups/sample-12-11-2024-10:15:30.tar.gz removed.
```

---

## Important Notes

1. **Permission Settings:** Ensure the user running the script has sufficient permissions to read the source directory and upload files to the remote server.

---

## Customization

- Modify the timestamp format in the `genArchiveName` function to suit your naming convention.
- Extend the script to handle additional backup options, such as file exclusion.

---

## Troubleshooting

- **Host Key Verification Errors**: Ensure the host key for the remote server is present in `~/.ssh/known_hosts`. Add it using:

```Bash
ssh-keyscan -p <port> <remote_host> >> ~/.ssh/known_hosts
```

- **Connection Issues**: Verify the remote server credentials, SSH key, and port settings.

- **Dependency Errors**: Ensure all required Python libraries are installed and compatible with your Python version.