//Constants:
const saveRouteUrl = "";
fullRoute="";
GEOJSONRoute = "";

var canvas
var points
var endMarker
var startMarker
var map

$(() => {
    

    mapboxgl.accessToken = 'pk.eyJ1IjoianNvbmJvdXJuZSIsImEiOiJja2xzMXpuODYxYmNvMm9ud2JxdHRuZzE0In0.8R6NEIohdETFfkjo5U5GdQ';
    map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/outdoors-v11',
        center: [-0.57048282701993, 51.23653894018821], // starting position
        zoom: 12
    });

    // initialize the map canvas to interact with later
    canvas = map.getCanvasContainer();

    points = [];

    endMarker = new mapboxgl.Marker({color: "red", draggable: true});
    startMarker = new mapboxgl.Marker({color: "green", draggable: true});

    map.on('click', function (e) {
        var coordsObj = e.lngLat;
        canvas.style.cursor = '';
        var coords = Object.keys(coordsObj).map(function (key) {
            return coordsObj[key];
        });
    
        points.push(coords);
        console.log("Coords: " + coords);
        console.log("Points: " + points);
    
        getRoute(points);
    });

    endMarker.on('dragend', repositionEndMarker);
    startMarker.on('dragend', repositionStartMarker);
})


// create a function to make a directions request
function getRoute(points) {
    console.log(points.length);
    if (points.length > 1) {
        steps = "";
        for (i = 0; i < points.length; i++) {
            if (steps == "") {
                steps = steps + points[i][0] + ',' + points[i][1];
            } else {
                steps = steps + ';' + points[i][0] + ',' + points[i][1];
            }

        }
        console.log("Steps: " + steps);

        var url = 'https://api.mapbox.com/directions/v5/mapbox/walking/' + steps + '?alternatives=true&geometries=geojson&steps=true&access_token=' + mapboxgl.accessToken;
        console.log(url);
        var req = new XMLHttpRequest();
        req.open('GET', url, true);
        req.onload = function () {
            var json = JSON.parse(req.response);
            var data = json.routes[0];
            var route = data.geometry.coordinates;
            console.log("Route: " + route);
            fullRoute=route;
            var geojson = {
                type: 'Feature',
                properties: {},
                geometry: {
                    type: 'LineString',
                    coordinates: route
                }
            };
            //GEOJSONRoute = geojson;
            //Get Instructions:
            var instructions = document.getElementById('instructions');
            var steps = data.legs[0].steps;

            var tripInstructions = [];
            for (var i = 0; i < steps.length; i++) {
                tripInstructions.push('<br><li>' + steps[i].maneuver.instruction.substring(0, (steps[i].maneuver.instruction.length-1))) + '</li>';
                fullInstructions = '<br><h2>Instructions:</h2><br><span class="duration">Trip duration: ' + Math.floor(data.duration / 60) + ' min </span>' + tripInstructions;
            }
            // if the route already exists on the map, reset it using setData
            if (map.getSource('route')) {
                GEOJSONRoute = req.response;
                map.getSource('route').setData(geojson);
                //update the position of the end marker to new end of route
                endMarker.setLngLat(points[points.length - 1]);
                console.log("Set Data");
                //GEOJSONRoute = geojson;
            } else { // otherwise, make a new request
                console.log("New Layer");
                map.addLayer({
                    id: 'route',
                    type: 'line',
                    source: {
                        type: 'geojson',
                        data: {
                            type: 'Feature',
                            properties: {},
                            geometry: {
                                type: 'LineString',
                                coordinates: geojson
                            }
                        }
                    },
                    layout: {
                        'line-join': 'round',
                        'line-cap': 'round'
                    },
                    paint: {
                        'line-color': '#3887be',
                        'line-width': 5,
                        'line-opacity': 0.75
                    }
                });
                map.getSource('route').setData(geojson);
                //GEOJSONRoute = geojson;
                console.log(geojson);
                console.log("Set Data after New Layer");
                //Add the end marker to the map for the first time
                endMarker
                    .setLngLat(points[points.length - 1])
                    .setPopup(new mapboxgl.Popup().setHTML("End"))
                    .addTo(map);
            }
        };
        req.send();
    } else if (points.length == 1) {
        console.log("Initial point triggered");
        if (!map.getSource('start')) {
            console.log("No start layer detected");
            startMarker
                .setLngLat(points[0])
                .setPopup(new mapboxgl.Popup().setHTML("Start"))
                .addTo(map);
        }
    }

}



function undo() {
    points.splice(points.length - 1, 1);
    console.log(points);
    if (map.getLayer('route')) {
        map.removeLayer('route');
    }
    if (map.getSource('route')) {
        map.removeSource('route');
    }
    endMarker.remove();
    if (points.length == 0) {
        startMarker.remove();
    }
    getRoute(points);
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

function validateInputs(){
    console.log(document.getElementById("titleBox").value);
    document.getElementById("errors").innerHTML = "";
    console.log(points.length);
    if (points.length < 2){
        document.getElementById("errors").innerHTML = document.getElementById("errors").textContent + "You must plot a route<br>";
        return false;
    }
    if (document.getElementById("titleBox").value == ""){

        document.getElementById("errors").innerHTML = document.getElementById("errors").textContent + "You must enter a title<br>";
        return false;
    }else{
        if (document.getElementById("descriptionBox").value == ""){
            document.getElementById("errors").innerHTML = document.getElementById("errors").textContent + "You must enter a description";
            return false;
        }else{
            return true;
        }
    }
}

function saveRoute() {

    if(validateInputs()){
        var xhr = new XMLHttpRequest();

        xhr.open("POST", "", false);
        xhr.withCredentials = true;

        xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
        xhr.setRequestHeader("Accept", "application/json");

        console.log(generateMapImage(fullRoute));

        xhr.send(JSON.stringify({
            points: fullRoute,
            title: document.getElementById("titleBox").value,
            description: document.getElementById("descriptionBox").value,
            length: calculateLength(),
            image: generateMapImage(fullRoute),
            tags: document.getElementById("tagsBox").value
        }));
    }


}

function repositionEndMarker() {
    console.log("End marker moved");
    console.log("New end: " + endMarker.getLngLat().lng + ", " + endMarker.getLngLat().lat);
    points[points.length - 1][0] = endMarker.getLngLat().lng;
    points[points.length - 1][1] = endMarker.getLngLat().lat;
    getRoute(points);

}

function repositionStartMarker() {
    console.log("End marker moved");
    console.log("New end: " + startMarker.getLngLat().lng + ", " + startMarker.getLngLat().lat);
    points[0][0] = startMarker.getLngLat().lng;
    points[0][1] = startMarker.getLngLat().lat;
    getRoute(points);
}

function displayInstructions(){
    document.getElementById("instructions").innerHTML = fullInstructions;
}

function calculateLength(){
    line = turf.lineString(points);
    length = turf.length(line, {units: 'kilometers'});
    console.log("Length: " + length);
    return length;
}

function generateMapImage(route){

    JSONFormat = { "type": "Feature",
                        "geometry": {
                        "type": "LineString",
                        "coordinates": route,
                        },
                        "properties": {
                        //"stroke": "#555555"
                        }
                    };
    
    document.getElementById("mapimg").setAttribute("src", "https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/static/geojson(" + JSON.stringify(JSONFormat) + ")/-0.5662,51.2309,10.81,0/300x200?access_token=pk.eyJ1IjoianNvbmJvdXJuZSIsImEiOiJja2xzMXpuODYxYmNvMm9ud2JxdHRuZzE0In0.8R6NEIohdETFfkjo5U5GdQ");
    return(("https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/static/geojson(" + JSON.stringify(JSONFormat) + ")/-0.5662,51.2309,10.81,0/300x200?access_token=pk.eyJ1IjoianNvbmJvdXJuZSIsImEiOiJja2xzMXpuODYxYmNvMm9ud2JxdHRuZzE0In0.8R6NEIohdETFfkjo5U5GdQ").toString());
   
}



