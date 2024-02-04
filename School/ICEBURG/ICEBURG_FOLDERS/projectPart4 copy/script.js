'use strict';

// burger menu


const burgerBtn = document.querySelector('.hamburger-btn');
const burgerUl = document.querySelector('ul');
const body = document.querySelector('body');



burgerBtn.addEventListener('click', e=>{
    burgerUl.classList.toggle('active');
    body.classList.toggle('active');

    
});

const darkSwitch = document.getElementById('darkSwitch');
const main = document.querySelector('main');
const aside1 = document.getElementById('aside1');
const aside2 = document.getElementById('aside2');
const header = document.querySelector('header');
const footer = document.querySelector('footer');



darkSwitch.addEventListener('change', ()=> {
    console.log(darkSwitch);
    console.log(main);
    console.log(aside2);
    console.log(header);
    console.log(footer);

    main.classList.toggle('active');
    aside1.classList.toggle('active');
    aside2.classList.toggle('active');
    header.classList.toggle('active');
    footer.classList.toggle('active');
    

});

// burger menu end


const searchBtn = document.getElementById('searchBtn');
const artistInput = document.getElementById('artistName');
const resultsDiv = document.getElementById('results');
console.log(searchBtn);

if(searchBtn != null){

    searchBtn.addEventListener('click', () => {
    const artistName = artistInput.value.trim();
    console.log("searchBtn clicked")
    
    if (artistName !== '') {
        const apiUrl = `https://www.theaudiodb.com/api/v1/json/523532/searchalbum.php?s=${encodeURIComponent(artistName)}`;

        fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                console.log("error at response");
            throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(".then data");
            displayResults(data);
        })
        .catch(error => {
            console.error('There was a problem fetching the data:', error);
            resultsDiv.innerHTML = 'There was a problem fetching the data. Please try again.';
        });
    } else {
        resultsDiv.innerHTML = 'Please enter an artist name.';
    }
    });
}

function displayResults(data) {
  resultsDiv.innerHTML = '';

  if (data.album && data.album.length > 0) {
    data.album.forEach(album => {
      const albumName = album.strAlbum;
      const albumYear = album.intYearReleased;
      console.log(albumName);
      
      const albumInfo = document.createElement('div');
      albumInfo.innerHTML = `<strong>${albumName}</strong> - Released Year: ${albumYear}`;
      
      resultsDiv.appendChild(albumInfo);
    });
  } else {
    console.log(" no results")
    resultsDiv.innerHTML = 'No albums found for the specified artist.';
  }
}


const searchAllOtherPages = document.getElementById('submitBtn');
console.log(searchAllOtherPages);

if(searchAllOtherPages != null){
    searchAllOtherPages.addEventListener('click', () => {
        const artistName = artistInput.value.trim();
        window.location.href = `searchResults.html?query=${encodeURIComponent(artistName)}`;
    });
}

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const searchQuery = urlParams.get('query');

console.log('Search query:', searchQuery);

if (searchQuery != null){
       
    if (searchQuery !== '') {
        const apiUrl = `https://www.theaudiodb.com/api/v1/json/523532/searchalbum.php?s=${encodeURIComponent(searchQuery)}`;

        fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                console.log("error at response");
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(".then data");
            displayResults(data);
        })
        .catch(error => {
            console.error('There was a problem fetching the data:', error);
            resultsDiv.innerHTML = 'There was a problem fetching the data. Please try again.';
        });
    } else {
        resultsDiv.innerHTML = 'Please enter an artist name.';
    }
}
