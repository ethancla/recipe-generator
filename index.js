function getRecipes() {
  const ingredients = document.getElementById('ingredients').value;

  fetch("https://recipegeneratorg.onrender.com/recipes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ingredients })
  })
  .then(response => response.json())
  .then(data => {
      if (data.error) {
          document.getElementById("recipeResult").innerHTML = `<p class="error-message">Error: ${data.error}</p>`;
          return;
      }

      const recipes = data.foods || [];
      let recipeHTML = "<h3>Suggested Recipes:</h3><ul class='recipe-list'>";

      recipes.forEach(recipe => {
          recipeHTML += `<li class="recipe-item">${recipe}</li>`;
      });

      recipeHTML += "</ul>";
      document.getElementById("recipeResult").innerHTML = recipeHTML;
  })
  .catch(error => {
      document.getElementById("recipeResult").innerHTML = `<p class="error-message">Fetch Error: ${error.message}</p>`;
  });
}

function getYoutube() {
  const subject = document.getElementById("youtubeSubject").value;

  fetch(`https://recipegeneratorg.onrender.com/youtube?subject=${encodeURIComponent(subject)}`)
  .then(response => response.json())
  .then(data => {
      if (data.error) {
          document.getElementById("youtubeResult").innerHTML = `<p class="error-message">Error: ${data.error}</p>`;
          return;
      }

      let youtubeHTML = "<h3>Recipe Videos:</h3>";
      data.forEach(video => {
          youtubeHTML += `
              <div class="youtube-video">
                  <a href="${video.url}" target="_blank" class="youtube-link">
                      <img src="${video.thumbnail}" alt="${video.title}" />
                      <p class="youtube-title">${video.title}</p>
                  </a>
              </div>
          `;
      });

      document.getElementById("youtubeResult").innerHTML = youtubeHTML;
  })
  .catch(error => {
      document.getElementById("youtubeResult").innerHTML = `<p class="error-message">Fetch Error: ${error.message}</p>`;
  });
}