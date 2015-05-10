function base_search() {
  event.preventDefault();
  var name = $('#base-search-name').val();
  var loc = $('#base-search-form').attr('action');
  loc = loc.substring(0, loc.length - 4);
  window.location.href = loc + name;
};
$('#base-search-button').click(base_search);
$('#base-search-name').keydown(function(e) {
  if(e.which == 13) {
     base_search();
  }
});
