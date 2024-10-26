docker run --rm \
  -e MONGO_SOURCE_URI="" \
  -e MONGO_DEST_URI="" \
  your-image-name:latest \
  bash -c "./dump-restore.sh && python3 main.py"
