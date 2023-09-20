//  async POST requests with async (including CSRF tokens)
// were based on the following post :
//https://realpython.com/django-and-ajax-form-submissions/
//  the csrft token setup was pasted from here as referenced in this blog post:
// https://github.com/realpython/django-form-fun/tree/3a8e98e6c9060effba8df9222d22a337f95b48eb

$(function () {
  // This function gets cookie with a given name
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie("csrftoken");

  /*
    The functions below will create a header with csrftoken
    */

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }
  function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = "//" + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (
      url == origin ||
      url.slice(0, origin.length + 1) == origin + "/" ||
      url == sr_origin ||
      url.slice(0, sr_origin.length + 1) == sr_origin + "/" ||
      // or any other URL that isn't scheme relative or absolute i.e relative.
      !/^(\/\/|http:|https:).*/.test(url)
    );
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });
});

$(".edit-button").click((e) => {
  console.log("Edit button clicked!  ");
  const button = $(e.target);
  const garmin_id = button.attr("data-id");
  console.log(garmin_id);
});

$(".delete-button").click((e) => {
  console.log("Delete button clicked!  ");
  const button = $(e.target);
  const garmin_id = button.attr("data-id");
  console.log(garmin_id);

  // $('#delete-id')[0].innerText = garmin_id
  // $('#deleteModal').modal('show')
});
