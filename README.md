# RecipChat

RecipChat is a chatbot application designed to provide users with detailed recipes for various meals. The chatbot is powered by OpenAI's GPT-3 model and is specifically trained to generate detailed recipes for Cameroonian meals.

## Features

- A list and detail view for recipes, implemented using Django's generic views.
- A chatbot view that accepts user messages, processes them using the GPT-3 model, and returns the generated response.
- A history of chat messages is maintained in the database.
- The frontend includes a chatbox where users can interact with the chatbot. It also includes features to clear the chatbox and copy messages to the clipboard.

## Installation

1. Clone the repository
```bash
git clone https://github.com/BertinAm/recip_chat.git
```
2. Change the working directory
```bash
cd recip_chat
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Apply migrations
```bash
python manage.py migrate
```
5. Create a superuser
```bash
python manage.py createsuperuser
```
6. Run the server
```bash
python manage.py runserver
```

## Usage

Open your web browser and navigate to `http://127.0.0.1:8000/` to start interacting with the chatbot.

## File Structure

- `recip_chat/`: The main Django project directory.
  - `recipes/`: The Django app containing the main functionality of the project.
    - `templates/`: Contains the HTML templates.
      - `src/chatbot_test.html`: The main chatbot interface.
    - `services.py`: Contains the `ChatGPTService` class which interacts with the OpenAI API.
    - `views.py`: Contains the views for the recipes and chatbot.
    - `models.py`: Contains the models for the recipes and chat messages.
    - `urls.py`: Contains the URL routes for the app.
  - `settings.py`: Contains the settings for the Django project.
  - `urls.py`: Contains the main URL routes for the project.
- `requirements.txt`: Contains the Python dependencies for the project.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
```

This README file provides a brief description of the project, its features, installation instructions, usage instructions, a description of the file structure, and information on how to contribute and the project's license.
