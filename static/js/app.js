$(() => {
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