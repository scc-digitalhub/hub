# Julia Container Function

This function runs a Julia script in a container using the julia:latest image. It installs the AWS, AWS S3, and HTTP packages into a shared Julia environment, then configures AWS credentials using either web identity or the default credential chain. It supports a custom S3 endpoint through AWS_ENDPOINT_URL. The job uses S3_BUCKET and PROJECT_NAME to create an S3 path for julia.txt, writes it, reads the file back, and logs the result.


## Features

- **Run Julia on DigitalHub**: Execute Julia scripts as container jobs on the DH platform
- **Julia container runtime**: Use the `julia:latest` image for an isolated job environment
- **AWS and S3 support**: Use Julia's AWS packages to access S3-compatible storage
- **Flexible AWS credentials**: Authenticate with web identity or the default credential chain
- **Custom S3 endpoints**: Connect to an alternate S3 service with `AWS_ENDPOINT_URL`
- **Project-based object paths**: Use `S3_BUCKET` and `PROJECT_NAME` to form the path for `julia.txt`
- **S3 read/write workflow**: Write `julia.txt`, read it back, and log the result


## Definition

The Julia job can use the following script to write `julia.txt` to the project-specific S3 path, read it back, and log the contents:

```julia
using AWSS3

bucket = ENV["S3_BUCKET"]
project = ENV["PROJECT_NAME"]
key = "$project/julia.txt"
message = "Hello from Julia!"

AWSS3.s3_put(bucket, key, message)
contents = AWSS3.s3_get(bucket, key)
println("Read from s3://$bucket/$key: $(String(contents))")
```

## Usage

Set up a DigitalHub project and run the registered Julia job:

```python
import digitalhub as dh

project = dh.get_or_create_project("<YOUR_PROJECT_NAME>")
function = project.get_function("julia-container-job")

run = function.run(
    action="job",
    run_as_user="1000",
    args=["/shared/hello-julia.jl"],
    wait=True,
)
```

Notes: For detailed usage, check the notebook.