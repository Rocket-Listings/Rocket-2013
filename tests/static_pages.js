// Static_pages browser testing

casper.test.begin('Static pages render correctly', 1, function suite(test) {
  casper.start("http://rocket-listings-staging.herokuapp.com/", function() {
    test.assertTitle("rocket", "homepage title is the one expected");
  });

  casper.run(function() {
    test.done();
  });

})
