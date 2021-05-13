$(() => {
    //Set css class on error fields
    $('.help.is-danger').siblings('.control').children('input').addClass('is-danger')

    //Activate hamburger menu on click
    $('.navbar-burger').click(() => {
        $('.navbar-burger').toggleClass('is-active')
        $('.navbar-menu').toggleClass('is-active')
    })

    //Delete notifications when button pressed
    $('button.delete').click((event) => {
        $(event.target).parent().parent().remove()
    })

    
})

function generateMapImageUrl(route){
    JSONFormat = JSON.stringify({ "type": "Feature",
                      "geometry": {
                        "type": "LineString",
                        "coordinates": route,
                      },
                      "properties": {}
                    });
    
    return  "https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/static/geojson(" + JSONFormat + ")/-0.5662,51.2309,10.81,0/600x400?access_token=pk.eyJ1IjoianNvbmJvdXJuZSIsImEiOiJja2xzMXpuODYxYmNvMm9ud2JxdHRuZzE0In0.8R6NEIohdETFfkjo5U5GdQ"
}

//Functions for encoding polylines for mapbox (taken from https://github.com/mapbox/polyline)
function py2_round(value) {
    // Google's polyline algorithm uses the same rounding strategy as Python 2, which is different from JS for negative values
    return Math.floor(Math.abs(value) + 0.5) * (value >= 0 ? 1 : -1);
}

function encode(current, previous, factor) {
    current = py2_round(current * factor);
    previous = py2_round(previous * factor);
    var coordinate = current - previous;
    coordinate <<= 1;
    if (current - previous < 0) {
        coordinate = ~coordinate;
    }
    var output = '';
    while (coordinate >= 0x20) {
        output += String.fromCharCode((0x20 | (coordinate & 0x1f)) + 63);
        coordinate >>= 5;
    }
    output += String.fromCharCode(coordinate + 63);
    return output;
}

//Takes an array of coordinates and optionally a precision value (default 5)
function encode_polyline(coordinates, precision) {
    if (!coordinates.length) { return ''; }

    var factor = Math.pow(10, Number.isInteger(precision) ? precision : 5),
        output = encode(coordinates[0][0], 0, factor) + encode(coordinates[0][1], 0, factor);

    for (var i = 1; i < coordinates.length; i++) {
        var a = coordinates[i], b = coordinates[i - 1];
        output += encode(a[0], b[0], factor);
        output += encode(a[1], b[1], factor);
    }

    return output;
};
