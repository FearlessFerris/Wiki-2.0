$(document).ready(function(){
    
    // Turn the 'text response' into an real html response 
    const html = document.getElementById('wiki-page')
    html.innerHTML = html.innerText

    
    
    // Ensure that the nav url's are set to local http://127.0.0.1:5000/, for some reason when creating an html response for a page the default will change to en.wikipedia.org
    const base = document.getElementsByTagName('base')
    for ( let i of base ) {
        i.setAttribute('href', 'http://127.0.0.1:5000/')
    }
})








