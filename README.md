# LLM Web Server

## Overview

This Python web server utilizes a Large Language Model (LLM) to generate responses. It's an experiment and is not suited for production. It use Llama 3 70b as the preferred LLM as smaller ones didn't follow instructions as well. The server requires an API that is compatible with the OpenAI API.

## Why

Could we use LLMs for web development? Instead of having to develop a site using some frontend library, why can't we have the LLM do it for us? We give it the content of the site as pure text, and it will serve it as HTML for us.

## No, really why?
For fun!

## Features

- **Content Management**: Content is stored in the root directory as .txt files.
- **Basic Pages**: Supports basic pages such as `/about` and `/blog/why-so-serious`.
- **List Pages**: Supports list pages with pagination, e.g., `/blogs` and `/blogs?page=1&pageSize=1`.
- **Styling**: Supports custom styling for a better user experience.
- **Output Formats**: Supports multiple output formats including `text/html`, `text/text`, `application/json`, and `application/rss+xml` for RSS feeds.

## Getting Started

To get started with the LLM Web Server, follow these steps:

1. Clone the repository: `git clone https://github.com/tobias-varden/llm-webserver.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Install [Ollama](https://www.ollama.com) and download llama 3 70b model. Alternatively set the openapi_endpoint to an OpenAI compatible endpoint and change the auth_token to your authentication token
4. Put some `.txt` files in your root dir, for example: about.txt
5. Run the server: `python app.py`

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
