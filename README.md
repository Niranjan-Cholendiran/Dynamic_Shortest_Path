# Dynamic Shortest Path

# Project Description

This project involves building a web application that calculates the shortest route between two cities using **Dijkstra’s Algorithm**. The application is designed for three U.S. states (Colorado, New York, and California) with a selection of 6-10 cities per state. We use the **Google Maps API** to provide real-time traffic data, and the algorithm computes the optimal route based on that data.

### Workflow

The user enters the source city, destination city, and traffic type (current or rush hour). After processing the input, the system:

- Retrieves real-time traffic information from the Google Maps API.
- Computes the shortest route using Dijkstra’s Algorithm.
- Visualizes the route on an interactive map.

### Features

The features of the system include:

- **Real-time traffic updates**.
- **Display of the shortest driving path**.
- **Dynamic interaction with Google Maps** to plot cities and compute travel times.
- **Coverage for 3 states** and **30 cities**.


# Setup Instructions

To get started with this project, follow the steps below:

### 1. Create a `config.json` File

In the root directory of the project, you need to create a `config.json` file. This file should contain your Google API key. Follow the steps below to create and configure the file:

1. Create a file named `config.json` in the root directory of the project.
2. Add the following content to the file, replacing `[YOUR API KEY]` with your actual Google API key:

    ```json
    {
        "googleApiKey": "[YOUR API KEY]"
    }
    ```

#### How to Get a Google API Key:
To obtain a Google API key, follow these steps:

- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project or use an existing one.
- Navigate to the **APIs & Services** > **Credentials** section.
- Click **Create credentials** and select **API key**.
- Copy the generated API key and paste it in the `config.json` file.

### 2. Replace the API Key in the Template

Next, replace the placeholder `[Google API Key]` in the `templates/distance_computation.html` file with the API key you generated. Simply open the file and search for `[Google API Key]`:

```html
<script src="https://maps.googleapis.com/maps/api/js?key=[Google API Key]&callback=initMap" async defer></script>
```

### 3. Run the Application

To run the application, make sure you're in the root directory of the project and run the following command:

```bash
python app.py
```
This will start the application. Open your browser and navigate to the URL provided in the terminal to view the application in action.
