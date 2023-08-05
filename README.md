# MyChat - Video Calling Web App

![MyChat Login Page](https://github.com/Rohit-Singh-0/MyChat/blob/main/static/Web%20capture_5-8-2023_17197_127.0.0.1.jpeg)

Welcome to MyChat - a video calling web app built with Django and integrated with the Agora SDK. MyChat enables real-time audio and video communication between users, providing an interactive and engaging experience for your web application's users.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)


## Introduction

MyChat is a full-featured web application that allows users to engage in video calls with each other in real-time. It leverages the power of Django web framework and integrates the Agora SDK, a robust solution for seamless real-time communication features. With MyChat, you can easily implement voice and video calling, live streaming, and interactive broadcasting in your Django-based web application.

## Features

- User registration using Django's built-in features.
- Real-time audio and video communication with Agora SDK.
- Group calling support, enabling multiple users to participate in the same call.
- Responsive and user-friendly interface for seamless usage on various devices.

## Installation

To run MyChat locally on your machine, follow these steps:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/Rohit-Singh-0/MyChat.git
cd MyChat
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Apply the database migrations:

```bash
python manage.py migrate
```

5. Obtain your Agora SDK credentials by signing up at [Agora.io](https://www.agora.io) and replace the placeholders in the `settings.py` file with your Agora App ID.

6. Run the development server:

```bash
python manage.py runserver
```

The application will now be accessible at `http://localhost:8000/`.

## Usage

Once MyChat is up and running, users can register or log in to their accounts. After logging in, they can create or join rooms for video communication. The Agora SDK handles the real-time communication aspects, allowing users to interact seamlessly through video calls.

Thank you for using MyChat! If you have any questions or encounter any issues, please feel free to open an issue on this repository. Happy video calling!
