Certainly! Here's a README template tailored to the script we've been discussing:

---

# Email Notification Script

This Python script sends email notifications to users with details about matched files, attaching PDF files if they exist.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This script provides a simple way to send email notifications to users based on matched files found in a specified folder.

## Features

- Sends email notifications to users based on matched files containing their user ID.
- attaches PDF files if they exist and are accessible.
- Provides error handling for SMTP errors and file-related issues.

## Installation

1. Clone or download the script from the repository.
2. Make sure you have Python installed on your system.
3. Install the required dependencies using pip:

```
pip install smtplib
pip install email
pip install sqlalchemy
```

## Usage

1. Customize the script by setting up the SMTP server details, sender email, and password in the `config.ini` file.
2. Run the script and follow the prompts to enter the folder path and user ID.
3. The script will process the specified folder, search for files containing the user ID, and send email notifications accordingly.

```bash
python main.py
```

## Configuration

The script reads configuration details from the `config.ini` file. Make sure to set up the following parameters:

```ini
[Email]
smtp_server = smtp.example.com
smtp_port = 465
sender_email = your_email@example.com
sender_password = your_email_password
```

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](license.lic).

## Steps to Create an App Password

* Visit your Google Account Security Settings (https://myaccount.google.com/intro/security).
* Under "How you sign in to Google," select 2-Step Verification.
* At the bottom of the page, select App passwords.
* Choose "Select app" and pick "Other (Custom name)".
* Enter a descriptive name, like "Your Script Name".
* Click "Generate" and copy the 16-character App Password.

### if App Password not found on ur account
* In https://myaccount.google.com/security
- then visiting https://myaccount.google.com/apppasswords 
- should allow you to set up application specific passwords. 

---