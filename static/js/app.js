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

