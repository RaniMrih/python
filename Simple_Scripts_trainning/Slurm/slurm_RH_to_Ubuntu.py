import os
import shutil

# Source and destination directories
src_dir = "/etc/slurm"
dst_dir = "/etc/slurm-llnl"

# Check if the source directory exists
if os.path.exists(src_dir):
    pass
    # Copy the SLURM files to the destination directory
#     for filename in os.listdir(src_dir):
#         src_file = os.path.join(src_dir, filename)
#         dst_file = os.path.join(dst_dir, filename)
#         shutil.copy2(src_file, dst_file)
#     print("SLURM files successfully copied from", src_dir, "to", dst_dir)
# else:
#     print("Source directory", src_dir, "does not exist.")
