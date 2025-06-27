// Get references to our HTML elements
const movieInput = document.getElementById('movie-input');
const searchButton = document.getElementById('search-button');
const resultsContainer = document.getElementById('results-container');

// This function calls our API and updates the page
const getRecommendations = async () => {
    const movieTitle = movieInput.value.trim();

    // Don't search if the input is empty
    if (!movieTitle) {
        return;
    }

    // Clear previous results and show a loading message
    resultsContainer.innerHTML = '<p class="message">Fetching recommendations...</p>';

    try {
        // Use fetch to call our backend API
        // encodeURIComponent ensures special characters in titles work correctly
        const response = await fetch(`/recommend?title=${encodeURIComponent(movieTitle)}`);

        if (!response.ok) {
            // If we get an error response (like 404), handle it
            const errorData = await response.json();
            throw new Error(errorData.error || 'Something went wrong');
        }

        const data = await response.json();
        
        displayResults(data.recommendations);

    } catch (error) {
        displayError(error.message);
    }
};

// This function takes the list of movies and displays them
const displayResults = (movies) => {
    resultsContainer.innerHTML = ''; // Clear the loading message

    if (movies && movies.length > 0) {
        movies.forEach(movie => {
            const movieElement = document.createElement('div');
            movieElement.classList.add('result-item');
            movieElement.textContent = movie;
            resultsContainer.appendChild(movieElement);
        });
    } else {
        resultsContainer.innerHTML = '<p class="message">No recommendations found.</p>';
    }
};

// This function displays an error message
const displayError = (message) => {
    resultsContainer.innerHTML = `<p class="error">${message}</p>`;
};

// Add event listeners
searchButton.addEventListener('click', getRecommendations);

// Allow pressing Enter to trigger a search
movieInput.addEventListener('keyup', (event) => {
    if (event.key === 'Enter') {
        getRecommendations();
    }
});