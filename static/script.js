$(document).ready(function () {
    $(window).scroll(function () {
        if ($(this).scrollTop() > 50) {
            $('.nav__container').addClass('scrolled');
        } else {
            $('.nav__container').removeClass('scrolled');
        }
    });

    $('#contact-form').on('submit', function (e) {
        e.preventDefault();
        alert('Thank you for your message!');
        $(this).trigger('reset');
    });





});
