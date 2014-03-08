// Static_pages browser testing

casper.test.begin('Static pages tests', 17, function suite(test) {
  casper.start(casper.cli.get("url"), function() {
    this.echo("Test homepage has loaded.", "INFO_BAR");
    test.assertHttpStatus(200);
    test.assertTitle("rocket", "homepage title is the one expected");
    test.assertSelectorHasText('h1', 'A better way to sell on ', "homepage call out is present");
    test.assertSelectorHasText('#register-menu-item', 'Sign Up', "sign up button is present");
    test.assertSelectorHasText('#login-menu-item', 'Login', "login button is present");
  });
  casper.then(function(){
    this.echo("Test manage tab works.", "INFO_BAR");
    test.assertVisible('#manage-partial', "manage-partial is visible");
    test.assertResourceExists(function(resource) {
            return resource.url.match('http://static.rocketlistings.com/static_pages/img/dashboard.6b2f2a043e59.png');
    }, "manage image has loaded");
  });
  casper.then(function(){
    this.echo("Test post tab works.", "INFO_BAR");
    this.click("#post-menu-item");
    test.assertUrlMatch(casper.cli.get("url") + "post/", "url has /post/ appended to it");
    test.assertVisible('#post-partial', "post-partial is visible");
    test.assertResourceExists(function(resource) {
            return resource.url.match('http://static.rocketlistings.com/static_pages/img/full-listing.3bf583e31922.png');
    }, "create image has loaded");
  });
  casper.then(function(){
    this.echo("Test trust tab works.", "INFO_BAR");
    this.click("#profile-menu-item");
    test.assertUrlMatch(casper.cli.get("url") + "profile/", "url has /profile/ appended to it");
    test.assertVisible('#profile-partial', "profile-partial is visible");
    test.assertResourceExists(function(resource) {
            return resource.url.match('http://static.rocketlistings.com/static_pages/img/profile-card.6461a043a459.png');
    }, "profile image has loaded");
  });
  casper.then(function(){
    this.echo("Test about page works.", "INFO_BAR");
    this.click("#about-menu-item");
    test.assertUrlMatch(casper.cli.get("url") + "about/", "url has /about/ appended to it");
    test.assertTextExists('Craigslist has the best network.', 'about copy exists');
  });
  casper.then(function(){
    this.echo("Test pricing page works.", "INFO_BAR");
    this.click("#pricing-menu-item");
    test.assertUrlMatch(casper.cli.get("url") + "pricing/", "url has /pricing/ appended to it");
    test.assertTextExists("While we're in beta, Rocket is totally free.", 'pricing copy exists.');
  });
  casper.run(function() {
    test.done();
  });

})
