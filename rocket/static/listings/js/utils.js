if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined' ? args[number] : match;
    });
  };
}

if (!String.prototype.trim) {
  String.prototype.trim=function(){return this.replace(/^\s+|\s+$/g, '');};
}
// // serialize for backbone
// $.fn.serializeObject = function() {
//     var o = {};
//     var a = this.serializeArray();
//     $.each(a, function() {
//         if (o[this.name] !== undefined) {
//             if (!o[this.name].push) {
//                 o[this.name] = [o[this.name]];
//             }
//             o[this.name].push(this.value || '');
//         } else {
//             o[this.name] = this.value || '';
//         }
//     });
//     return o;
// };

// too hardcore for me
// function setupAjaxCSRF() {
//   function csrfSafeMethod(method) {
//     // these HTTP methods do not require CSRF protection
//     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
//   }
//   function sameOrigin(url) {
//     // test that a given url is a same-origin URL
//     // url could be relative or scheme relative or absolute
//     var host = document.location.host; // host + port
//     var protocol = document.location.protocol;
//     var sr_origin = '//' + host;
//     var origin = protocol + sr_origin;
//     // Allow absolute or scheme relative URLs to same origin
//     return  (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
//             (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
//             // or any other URL that isn't scheme relative or absolute i.e relative.
//             !(/^(\/\/|http:|https:).*/.test(url));
//   }
//   $.ajaxSetup({
//     beforeSend: function(xhr, settings) {
//       if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
//         // Send the token to same-origin, relative URLs only.
//         // Send the token only if the method warrants CSRF protection
//         // Using the CSRFToken value acquired earlier
//         xhr.setRequestHeader("X-CSRFToken", csrftoken);
//       }
//     }
//   });
// }