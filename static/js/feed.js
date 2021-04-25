$(() => {
    //FIX THIS

    //Load map images
    $('.map-img').each(() => {
        url = generateMapImageUrl($(this).attr('data-route')) 
        $(this).attr("src", url)
    })
})

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