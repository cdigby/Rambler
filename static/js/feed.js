$(() => {
    //Highlight links for sorting all routes after selection
    let sp = new URLSearchParams(window.location.search)
    if (sp.has('showall')) {
        param = sp.get('showall')
        if (param === 'new') {$('#allnew').addClass('has-text-weight-bold')}
        if (param === 'old') {$('#allold').addClass('has-text-weight-bold')}
        if (param === 'top') {$('#alltop').addClass('has-text-weight-bold')}
    }
    if (Array.from(sp).length === 0) {$('#allnew').addClass('has-text-weight-bold')}

    //Load map images (Do last so nothing else is waiting)
    $('.map-img').each(function() {
        $(this).attr("src", generateMapImageUrl($(this).data('points')))
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
    $.ajax({
        type: 'POST',
        url: '/feed/',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        data: {"function": "LIKE", "route": route},
        success: function (response) {
            el = $('#rating-' + route)
            el.text(parseInt(response["rating"]))
        },
    })
}

function dislike(route){
    $.ajax({
        type: 'POST',
        url: '/feed/',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        data: {"function": "DISLIKE", "route": route},
        success: function (response) {
            el = $('#rating-' + route)
            el.text(parseInt(response["rating"]))
        },
    })
}