# Text Extraction Service

This project implements a text extraction service using Apache Tika and Python. It provides a REST API endpoint that accepts POST requests containing file artifacts and extracts text content from them.

The service consists of two main components:

- **Tika Container**: Apache Tika service for document text extraction
- **Python Function**: Handler that orchestrates the extraction workflow, downloads artifacts, sends them to Tika, and logs the extracted output


## Definition

### Extract 

The `extract` function is a Python-based handler that processes document artifacts through Apache Tika for text extraction.

```python
import requests

def extract_text(tika_url, artifact, project):
    print(f"Downloading artifact {artifact.name}...")
    fp = artifact.as_file()
    if not (tika_url)[:4] == "http": 
        tika_url = "http://"+tika_url
    print(f"Sending {fp} to {tika_url}...")    
    response = requests.put(tika_url+"/tika",headers={"Accept":"text/html"}, data=open(fp,'rb').read())
    if response.status_code == 200:
        print("Extracted text with success")
        res = "/tmp/output.html"
        with open(res, "w") as tf:
            tf.write(response.text)
        project.log_artifact(kind="artifact", name=artifact.name+"_output.html", source=res)
        return res
    else:
        print(f"Received error: {response.status_code}")
        raise Exception("Error")
```

**Parameters**:

- `tika_url`: URL endpoint of the Tika service
- `artifact`: The document file to be processed
- `project`: Project context for logging results

**Workflow**:

1. Downloads the artifact file
2. Ensures proper HTTP URL formatting for Tika endpoint
3. Sends the file to Tika via PUT request with `Accept: text/html` header
4. On success (HTTP 200), writes extracted text to `/tmp/output.html`
5. Logs the output artifact back to the project
6. Raises exception on extraction failure


### Tika

The Tika service is a containerized Apache Tika instance that provides document text extraction capabilities via REST API.

**Container Image**: `apache/tika:latest`

**Port**: `9998`

**Endpoint**: `PUT /tika/form`

**Request Headers**:

- `Accept: text/html`: Specifies HTML output format

**Response**: Extracted text content from the document

**Supported Formats**: PDF, DOCX, XLSX, PPTX, images with OCR, and other common document types


## Usage

To use the text extraction service, follow these steps:

1. **Initialize the project and deploy Tika service**:

```python
import digitalhub as dh
proj = dh.get_or_create_project("tika")
tika_function = proj.get_function("tika")
tika_run = tika_function.run("serve", service_ports=[{"port": 9998, "target_port": 9998}], wait=True)
TIKA_URL = tika_run.status.to_dict()["service"]["url"]
```

2. **Log a document artifact**:

```python
artifact = proj.log_artifact("document.pdf", kind="artifact", source="path/to/document.pdf")
```

3. **Run the extraction function**:

```python
extract_function = proj.get_function("extract")
extract_run = extract_function.run("job", inputs={"artifact": artifact.key}, parameters={"tika_url": TIKA_URL}, wait=True)
```

4. **Retrieve the extracted output**:

```python
output_artifact = proj.get_artifact("document.pdf_output.html")
output_artifact.download()
with open('./artifact/output.html', 'r') as f:
        print(f.read())
```
