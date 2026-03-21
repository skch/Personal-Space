# Personal-Space
Local website to manage personal information

## Usage

STEP 1. Create file `config.json` in the root directory.

```json
{
  "logo": "My logo",
  "wiki": "{path-to-wiki-root}",
  "calendar": "{path-to-calendar-root}",
  "contacts": "{path-to-contacts-root}"
}
```

STEP 2. Install dependencies

Use the following command to install dependencies:

```shell
pip install -r requirements.txt
```

STEP 3. Start the server


```shell
python app.py
```