function update_manga() {
  event.preventDefault();
  var name = $('#home-manga-name').val();
  var loc = $('#home-update-form').attr('action');
  loc = loc.substring(0, loc.length - 4);
  $.get(loc + name, function(data) {
    location.reload();
  });
};
$('#home-update-button').click(update_manga);
$('#home-manga-name').keydown(function(e) {
  if(e.which == 13) {
     update_manga();
  }
}); 
