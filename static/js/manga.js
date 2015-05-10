$('#delete-manga').click(function() {
  if(!confirm("Remove this manga from the datastore?")) {
    event.preventDefault();
  }
});

