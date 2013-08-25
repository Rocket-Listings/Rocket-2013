// $(function() {
//     $("div[data-toggle='buttons-radio']").each(function() {
//         var btnGroup = $(this),
//             buttons = btnGroup.children('button');
//         buttons.click(function() {
//             buttons.removeClass("active");
//             $(this).addClass("active");
//         });
//     });
// });

// Get cookie for csrf token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}