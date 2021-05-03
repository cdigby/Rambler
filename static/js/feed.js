$(() => {
    

    //For all maps generate image once page loaded
})

function generateMapImage(id, route){

    JSONFormat = JSON.stringify({ "type": "Feature",
                      "geometry": {
                        "type": "LineString",
                        "coordinates": route,
                      },
                      "properties": {}
                    });
    
    url = "https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/static/geojson(" + JSONFormat + ")/-0.5662,51.2309,10.81,0/300x200?access_token=pk.eyJ1IjoianNvbmJvdXJuZSIsImEiOiJja2xzMXpuODYxYmNvMm9ud2JxdHRuZzE0In0.8R6NEIohdETFfkjo5U5GdQ"
    $("map-" + String(id)).attr("src", url)
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function like(route){
    var xhr = new XMLHttpRequest();

    console.log("Like")
    xhr.open("POST", "", false);
    xhr.withCredentials = true;

    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
    xhr.setRequestHeader("Accept", "application/json");

    console.log(route);
    xhr.send(JSON.stringify({
        function: "LIKE",
        route: route
    }));
}

function dislike(route){
    var xhr = new XMLHttpRequest();
    console.log("Dislike")
    xhr.open("POST", "", false);
    xhr.withCredentials = true;

    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
    xhr.setRequestHeader("Accept", "application/json");

    xhr.send(JSON.stringify({
        function: "DISLIKE",
        route: route
    }));
}