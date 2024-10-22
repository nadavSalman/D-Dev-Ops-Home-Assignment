docker run --rm \
  -e MONGO_SOURCE_URI="" \
  -e MONGO_DEST_URI="" \
  your-image-name:latest \
  bash -c "mongomirror --source \"$MONGO_SOURCE_URI\" --destination \"$MONGO_DEST_URI\" && python3 /app/your_python_script.py"
