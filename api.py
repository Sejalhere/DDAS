from fastapi import FastAPI, UploadFile, File

app = FastAPI()


@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    # Read file content
    file_content = await file.read()

    # Check if file is a duplicate
    duplicate_check = check_duplicate(file_content)

    if duplicate_check["is_duplicate"]:
        return {"status": "duplicate", "file_metadata": duplicate_check['file_metadata']}

    # Store file metadata if not duplicate
    file_metadata = store_file_metadata(
        file_content,
        file_path=f"/path/to/{file.filename}",
        server="Server1",
        dataset_name="Dataset_A"
    )
    return {"status": "success", "metadata": file_metadata}
