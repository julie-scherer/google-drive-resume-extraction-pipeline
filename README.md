# Project Overview

This project combines a data extraction (ETL) process (**`extract.py`**) and a templated Python script that uses the OpenAI GPT-4 model (**`generate.py`**) to generate responses based on system prompts and user input.

## Getting Started

### Prerequisites

Before starting, make sure you have the Google Cloud CLI installed. You can find installation instructions [here](https://cloud.google.com/sdk/docs/install). Additionally, follow the instructions [here](https://cloud.google.com/docs/authentication/api-keys?&_ga=2.51103338.-2121777189.1703621503#python) to set up authentication with the Google Cloud API.

### References

Access the App in the Google Cloud Console at [this link](https://console.cloud.google.com/).

### Installation

1. Navigate to the root of the V4 Scholarship App Review folder:

    ```bash
    cd apps/v4-scholarship-app-reviews
    ```

2. Create a new **`credentials.json`** file, copy the **`GOOGLE_APP_CREDENTIALS`** config variable from Heroku, and save the credentials in the newly created file.

   Copy and paste the variable from the Heroku UI or use the Heroku CLI command to get the value and save it as **`credentials.json`**:

     ```bash
     heroku config:get GOOGLE_APP_CREDENTIALS --shell > credentials.json
     ```

   - The **`credentials.json`** file should look similar to the **`example_credentials.json`** file, but you should have the values for the missing credentials: private_key_id, private_key, client_email, and client_id. The credentials file is required for accessing the GCloud API in the **`extract.py`** script.

3. Copy and paste the **`example.env`** file and rename it to **`.env`**. You will need to add a token for the **`OPENAI_API_KEY`** to run the `generate.py` script.

4. Set up a virtual environment:

    ```bash
    make venv
    ```

    This command creates a virtual environment, installs the required packages listed in **`requirements.txt`**, and activates the virtual environment.

## Running the Script

1. To extract and transform data from resume PDFs, .doc, and .docx files into JSON and CSV formats, run:

    ```bash
    make extract
    ```

    This command activates the virtual environment and runs the `extract.py` script in the `src/` directory. The resumes will be downloaded from Google Drive to the `resumes/` folder, and the extracted data will be saved to the `data/` folder.

2. To generate responses using the OpenAI GPT-4 model, run:

    ```bash
    make generate
    ```

    This command activates the virtual environment and executes the **`generate.py`** script. The script reads input files from the **`input`** directory, generates responses based on system and user prompts, and stores the output in the **`output`** directory.

## ChatGPT Customization

### System and User Prompts

Modify the **`system_prompt`** and **`user_prompt`** variables in the **`generate.py`** script to customize the prompts used for generating responses.

### OpenAI API Key

- Review and update the configurations in the **`.env`** file as needed.
- The project assumes the availability of the OpenAI GPT-4 model and requires a valid OpenAI API key.


License
----------
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
