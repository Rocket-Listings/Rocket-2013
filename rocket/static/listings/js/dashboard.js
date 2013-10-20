$(function() {
	// Helpers

	// Plugin to scroll div to certain location
	/**
	 * Copyright (c) 2007-2013 Ariel Flesler - aflesler<a>gmail<d>com | http://flesler.blogspot.com
	 * Dual licensed under MIT and GPL.
	 * @author Ariel Flesler
	 * @version 1.4.6
	 */
	;(function($){var h=$.scrollTo=function(a,b,c){$(window).scrollTo(a,b,c)};h.defaults={axis:'xy',duration:parseFloat($.fn.jquery)>=1.3?0:1,limit:true};h.window=function(a){return $(window)._scrollable()};$.fn._scrollable=function(){return this.map(function(){var a=this,isWin=!a.nodeName||$.inArray(a.nodeName.toLowerCase(),['iframe','#document','html','body'])!=-1;if(!isWin)return a;var b=(a.contentWindow||a).document||a.ownerDocument||a;return/webkit/i.test(navigator.userAgent)||b.compatMode=='BackCompat'?b.body:b.documentElement})};$.fn.scrollTo=function(e,f,g){if(typeof f=='object'){g=f;f=0}if(typeof g=='function')g={onAfter:g};if(e=='max')e=9e9;g=$.extend({},h.defaults,g);f=f||g.duration;g.queue=g.queue&&g.axis.length>1;if(g.queue)f/=2;g.offset=both(g.offset);g.over=both(g.over);return this._scrollable().each(function(){if(e==null)return;var d=this,$elem=$(d),targ=e,toff,attr={},win=$elem.is('html,body');switch(typeof targ){case'number':case'string':if(/^([+-]=?)?\d+(\.\d+)?(px|%)?$/.test(targ)){targ=both(targ);break}targ=$(targ,this);if(!targ.length)return;case'object':if(targ.is||targ.style)toff=(targ=$(targ)).offset()}$.each(g.axis.split(''),function(i,a){var b=a=='x'?'Left':'Top',pos=b.toLowerCase(),key='scroll'+b,old=d[key],max=h.max(d,a);if(toff){attr[key]=toff[pos]+(win?0:old-$elem.offset()[pos]);if(g.margin){attr[key]-=parseInt(targ.css('margin'+b))||0;attr[key]-=parseInt(targ.css('border'+b+'Width'))||0}attr[key]+=g.offset[pos]||0;if(g.over[pos])attr[key]+=targ[a=='x'?'width':'height']()*g.over[pos]}else{var c=targ[pos];attr[key]=c.slice&&c.slice(-1)=='%'?parseFloat(c)/100*max:c}if(g.limit&&/^\d+$/.test(attr[key]))attr[key]=attr[key]<=0?0:Math.min(attr[key],max);if(!i&&g.queue){if(old!=attr[key])animate(g.onAfterFirst);delete attr[key]}});animate(g.onAfter);function animate(a){$elem.animate(attr,f,g.easing,a&&function(){a.call(this,targ,g)})}}).end()};h.max=function(a,b){var c=b=='x'?'Width':'Height',scroll='scroll'+c;if(!$(a).is('html,body'))return a[scroll]-$(a)[c.toLowerCase()]();var d='client'+c,html=a.ownerDocument.documentElement,body=a.ownerDocument.body;return Math.max(html[scroll],body[scroll])-Math.min(html[d],body[d])};function both(a){return typeof a=='object'?a:{top:a,left:a}}})(jQuery);

	// Scroll messages to bottom
	$.fn.scrollBottom = function() {
		$(this).scrollTop($(this)[0].scrollHeight);
	}

	$.fn.exists = function () {
		return this.length !== 0;
	}

	// Mark a message as seen on the server
	// Must have attr 'data-message-id'
	$.fn.markSeen = function(callback) {
		var message_id = $(this).data('message-id');
		$.ajax({
			method: 'GET',
			url: '/listings/dashboard/message/seen',
			data: {'message_id': message_id},
			success: function (response) {
				if (response.status == 'success') {
					callback(response.message_data);
				}
				else {
					console.log("The server experienced an error.");
				}
			}
		});
	}

	// Convert links in messages to anchors
	function linkToClickable(text) {
	    var exp = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)/gi;
	    return text.replace(exp, "<a href='$1'>$1</a>"); 
	}

	// Insert new items into dashboard
	function insertNewData(data) {
		// Update latest ids
		$(".last-listing").text(data.latest[0]);
		$(".last-buyer").text(data.latest[1]);
		$(".last-message").text(data.latest[2]);
		// Mustache the new items
		$(".messages-body").append(Mustache.render($("#new-message").html(), {'messages': data.messages}));
		$(".buyers-body").prepend(Mustache.render($("#new-buyer").html(), {'buyers': data.buyers}));
		$(".listings-body ul.list").prepend(Mustache.render($("#new-listing").html(), {'listings': data.listings}));
	}

	// Bind clicks and list init to the current items
	function bindEvents() {
		$('.listing').click(function () {
			var listingRow = $(this),
				id = listingRow.data('listing-id'),
				buyers = $(".buyer[data-listing-id='" + id + "']");
			$('.listing').removeClass('highlight');
			$('.d-arrow').addClass('hide');
			listingRow.addClass('highlight');
			$(".message, .buyer").addClass("hide");
			$(".dashboard-delete-btn").attr('data-listing-id', id).removeClass("disabled");
			if (listingRow.hasClass("deleted")) {
				$(".dashboard-delete-permanent-btn").attr('data-listing-id', id).removeClass("disabled");
			}
			if (buyers.length) {
				$('.d-arrow', this).removeClass('hide');
				$(".buyers-body").addClass("border-right").removeClass("hide");
				$(".no-messages").addClass("hide");
				buyers.removeClass("hide");
				buyers.first().click();
				$('.message-form-wrapper').removeClass("hide");
				$('.messages-body').removeClass("hide").scrollBottom();
			} else {
				$('.message-form-wrapper').addClass("hide");
				$(".buyers-body").removeClass("border-right").addClass("hide");
				$(".messages-body").addClass("hide");
				$(".no-messages").removeClass("hide");
			}
		});

		$('.buyer').click(function (event){
			var buyerCard = $(this),
				buyer_id = buyerCard.data('buyer-id'),
				listing_id = buyerCard.data('listing-id'),
				unreadMessages = $(".message.unread[data-buyer-id='" + buyer_id + "']");
			$('.buyer').removeClass('highlight');
			buyerCard.addClass('highlight');
			$(".message").addClass("hide");
			$('.message[data-buyer-id="' + buyer_id + '"]').removeClass("hide");
			$(".message-form input[name='listing']").val(listing_id);
			$(".message-form input[name='buyer']").val(buyer_id);
			$('.messages-body').scrollBottom();
			unreadMessages.each(function () { 
				$(this).markSeen(function (data) {
					$(".message[data-message-id='" + data.message_id +"'], .buyer[data-buyer-id='" + data.buyer_id + "']").removeClass("unread");
					if (data.listing_all_read) {
						$(".listing[data-listing-id='" + data.listing_id + "']").removeClass("unread");
						$('span.label-info').hide();
					}
				});
			});
		});

		// Initialize the listings globally for List.js
		var options = {
			valueNames: ['id', 'title', 'price', 'category', 'date', 'status']
		};

		if (window.listings) {
			window.listings.filter();
		}

		window.listings = new List('dashboard-content', options);
		window.currentFilterButton.click();
	}

	// Unbind click events from current items
	function unbindEvents() {
		$('.listing, .buyer').unbind('click');
	}

	function propogateUnreadMessages() {
		$(".message.unread").each(function () {
			var buyer 	= $(this).data('buyer-id'),
				listing = $(this).data('listing-id');
			$('.buyer[data-buyer-id="' + buyer + '"]').addClass("unread");
			$('.listing[data-listing-id="' + listing + '"]').addClass("unread");
		});
	}

	// Toggle up/down chevrons on sort click
	$('.sort').click(function () {
		var icon = $(this).next('span'),
			icons = $("span.glyphicon.sort-toggle"),
			iconsNotClicked = $("span.glyphicon.sort-toggle:not('span.glyphicon.active')"),
			down = 'glyphicon-chevron-down',
			up = 'glyphicon-chevron-up';
		icons.addClass("hide").removeClass("active");
		icon.removeClass("hide").addClass('active');
		iconsNotClicked.removeClass(down + " " + up).addClass(down);
		if (icon.hasClass(down)) {
			icon.removeClass(down).addClass(up);
		}
		else {
			icon.removeClass(up).addClass(down);
		}
		return false;
	});
	
	// Remove the 'first-visit' class from the dashboard panel
	// This will move the dashboard back up on the page when
	// the first visit info box is closed
	$('.close').click(function(event){
		$('.dashboard-panel').removeClass("first-visit");
	});

	// Autopost from dashboard (not used here)
	$(".share_optn").click(function (e) {
		e.preventDefault();
		if (!$(this).hasClass("disabled")) {
			$.ajax({
				type: 'GET',
				url: $(this).attr('href'),
				success: function (response) {
				}
			});
		}
		$(this).addClass("disabled");
		checkStatus($(this).attr("id"));
		return false;
	});

	// Retrieve any new listings, buyers, messages from the database
	$(".dashboard-refresh").click(function (e) {
		e.preventDefault();
		var currentSelectedListing = $(".listings-body").find("li.highlight").data('listing-id');
		$.ajax({
			type: 'GET',
			url: '/listings/dashboard/data/',
			data: {'listing': $(".last-listing").text(),
				   'buyer': $(".last-buyer").text(),
				   'message': $(".last-message").text()},
			success: function (response) {
				insertNewData(response);
				unbindEvents(); // To prevent overlap
				bindEvents(); // Bind all items (including new)
				propogateUnreadMessages();
				if (currentSelectedListing != null) {
					// Maintain the clicked listing
					$(".listings-body").find("li[data-listing-id='" + currentSelectedListing + "']").click();
				}
				else { $(".listings-body li").first().click(); }
			}
		});
	});

	// Submit and handle a new message
	$("form.message-form").submit(function() {
		var csrftoken = getCookie('csrftoken');
		$.ajax({
			url: '/listings/dashboard/message/',
			method: 'POST',
			data: $(this).serialize(),
			beforeSend: function(xhr) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			},
			success: function (response) {
				switch (response.status) {
					case 'success':
						console.log(response);
						$(".messages-body").append(Mustache.render($("#new-message").html(), response));
						$('.buyer-' + response.messages.buyer_id).removeClass("hide");
						$('.messages-body').scrollBottom();
						$('.last-message').text(response.messages.message_id);
						$('.message-form textarea').val("").focus();
						break;
					case 'err_validation':
						console.log("There was an error sending the message.");
						break;
					case 'err_empty':
						break;
				}
			},
			error: function (response) {
				console.log("There was an error sending the message.");
			}
		});
		return false;
	});

	// Change the status of the selected listing to "Deleted"
	$(".dashboard-delete-btn").click(function (e) {
		var id = $(this).attr('data-listing-id');
		e.preventDefault();
		if (!$(this).hasClass("disabled")) {
			$.ajax({
				url: '/listings/' + id + '/status/update',
				method: 'GET',
				data: {'status': 'Deleted'},
				success: function (response) {
					var item = window.listings.get('id', response.listing.id);
					item.values({'status': response.listing.status});
					$('.listing[data-listing-id="' + response.listing.id + '"]').addClass('deleted').removeClass('active draft pending sold');
					window.currentFilterButton.click();
				}
			});
		}
	});

	// Delete the currently selected listing
	$(".dashboard-delete-permanent-btn").click(function (e) {
		var id = $(this).attr('data-listing-id');
		e.preventDefault();
		if (!$(this).hasClass("disabled")) {
			$.ajax({
				url: '/listings/' + id + '/delete',
				method: 'GET',
				success: function () {
					$(".buyer[data-listing-id='" + id + "'], .message[data-listing-id='" + id + "']").remove();
					window.listings.remove('id', id);
					window.currentFilterButton.click();
					$(".listings-body").scrollTop(0);
				}
			});
		}
		return false;
	});

	// Check the status of a listing (not used here)
	function checkStatus(listingid) {
		var timer = setInterval(function () {
			$.ajax({
				type: 'GET',
				url: '/listings/' + listingid + '/status',
				success: function (response) {
					if (response === "Active") {
						clearInterval(timer);
						$("tr[data-listing-id='" + listingid + "'] td.listing-status").html(response);
						$("a#" + listingid).removeClass("disabled");
					}
				}
			});
		}, 3000);
	}

	// Remove focus from the listings and hide buyers/messages during search
	$("input.search").keydown(function() {
		$(".buyers-body, .messages-body, .message-form-wrapper").addClass("hide");
		$(".listings-body li").removeClass("highlight");
		$(".no-messages").removeClass("hide");
		$(".dashboard-delete-btn, .dashboard-delete-permanent-btn").addClass("disabled");
	});

	$("input.search").focus(function() {
		window.searchHasFocus = true;
	});

	$(".dashboard-search-btn").click(function(e) {
		if (window.searchHasFocus == true) {
			$("input.search").blur();
			$(".listing").first().click();
			window.searchHasFocus = false;
		}
		else {
			$("input.search").focus();
		}
	});

	// Listings filters
	$('#filter-draft').click(function() {
    window.listings.filter(function(item) {
        if (item.values().status == "Draft") {
            return true;
        } else {
            return false;
        }
    });
    return false;
  });

  $('#filter-active').click(function() {
    window.listings.filter(function(item) {
        if (item.values().status == "Active") {
            return true;
        } else {
            return false;
        }
    });
    return false;
  });

  $('#filter-deleted').click(function() {
    window.listings.filter(function(item) {
        if (item.values().status == "Deleted") {
            return true;
        } else {
            return false;
        }
    });
    return false;
  });

  $('#filter-pending').click(function() {
    window.listings.filter(function(item) {
        if (item.values().status == "Pending") {
            return true;
        } else {
            return false;
        }
    });
    return false;
  });

  $('#filter-sold').click(function() {
    window.listings.filter(function(item) {
        if (item.values().status == "Sold") {
            return true;
        } else {
            return false;
        }
    });
    return false;
  });

  // All
  $('#filter-not-deleted').click(function() {
    window.listings.filter(function(item) {
        if (item.values().status != "Deleted") {
            return true;
        } else {
            return false;
        }
    });
    return false;
  });

  // Make the filter dropdown more intuitive:
  // - Change button text to filter type
  // - Close (toggle) dropdown on click
  // - Scroll to top of listings on filter
  $('.sidebar-text').click(function() {
  	window.currentFilterButton = $(this);
  	$(".sidebar-button-wrapper").removeClass('selected');
  	window.currentFilterButton.parent().addClass('selected');
  	$(".listing").first().click();
  	$(".listings-body").scrollTop(0);
  	if (window.currentFilterButton.attr('id') != "filter-deleted") {
  		$(".dashboard-delete-btn").removeClass("hide");
  		$(".dashboard-delete-permanent-btn").addClass("hide");
  	}
  	else {
  		$(".dashboard-delete-btn").addClass("hide");
  		$(".dashboard-delete-permanent-btn").removeClass("hide");
  	}
  });

  $(".keyboard-shortcuts-text a").click(function () {
  	$("#keyboard-shortcuts-modal").modal();
  });

  var Keys = {
		b: 66, l: 76,
		j: 74, k: 75,
		m: 77, r: 82, n: 78,
		esc: 27, enter: 13, slash: 191,
		shift: 16, qmark: 191,
		rarr: 39, larr: 37,
		up: 38, down: 40,
		context: "l",
		keys: [],
		init: function () {
			this.cacheElements();
			this.bindEvents();
		},
		cacheElements: function () {
			this.$body = $("body");
			this.$listings = $(".listings-body");
			this.$buyers = $(".buyers-body");
			this.$search = $("input.search");
			this.$refresh = $(".dashboard-refresh");
			this.$messageFormWrapper = $(".message-form-wrapper");
			this.$message = this.$messageFormWrapper.find("textarea");
		},
		bindEvents: function () {
			var $doc = $(document);
			$doc.on('keydown', this.addKey);
			$doc.on('keydown', this.executeEvents);
			$doc.on('keyup', this.removeKey);
		},
		addKey: function (e) {
			var key = e.which || e.keyCode;
			if (Keys.keys.indexOf(key) == -1) {
				Keys.keys.push(key);
			}
		},
		removeKey: function (e) {
			var key = e.which || e.keyCode;
			var keyIndex = Keys.keys.indexOf(key);
			Keys.keys.splice(keyIndex, 1);
		},
		executeEvents: function (e) {
			var keys = Keys.keys;
			var context = Keys.context;
			if (keys.length > 1) {
				if ((keys.length == 2) 
					&& (keys.indexOf(Keys.shift) != -1) 
					&& (keys.indexOf(Keys.qmark) != -1)
					&& (!Keys.$search.is(":focus")) 
					&& (!Keys.$message.is(":focus"))) {
					$("#keyboard-shortcuts-modal").modal('toggle');
				}
			}
			if (!Keys.$body.hasClass("modal-open")) {
				if ((!Keys.$search.is(":focus")) && (!Keys.$message.is(":focus"))) {
					switch (keys[0]) {
						case Keys.l:
						case Keys.larr:
							if (Keys.$listings.find("li:not(.hide)").length != 0) {
								Keys.context = "l";
							}
							break;
						case Keys.b:
						case Keys.rarr:
							if (Keys.$buyers.find("ul:not(.hide)").length != 0) {
								Keys.context = "b";
							}
							break;
						case Keys.j:
						case Keys.down:
							switch (context) {
								case "l":
									var currentSelectedListing = Keys.$listings.find("li.highlight");
									var nextListing = currentSelectedListing.next("li:not(.hide)");
									if (nextListing.exists()) {
										nextListing.click();
										Keys.$listings.scrollTo(nextListing)
									}
									break;
								case "b":
									var currentSelectedBuyer = Keys.$buyers.find("ul.highlight");
									var nextBuyer = currentSelectedBuyer.next("ul:not(.hide)");
									if (nextBuyer.exists()) {
										nextBuyer.click();
										Keys.$buyers.scrollTo(nextBuyer);
									}
									break;
							}
							break;
						case Keys.k:
						case Keys.up:
							switch (context) {
								case "l":
									var currentSelectedListing = Keys.$listings.find("li.highlight");
									var prevListing = currentSelectedListing.prev("li:not(.hide)");
									if (prevListing.exists()) {
										prevListing.click();
										Keys.$listings.scrollTo(prevListing)
									}
									break;
								case "b":
									var currentSelectedBuyer = Keys.$buyers.find("ul.highlight");
									var prevBuyer = currentSelectedBuyer.prev("ul:not(.hide)");
									if (prevBuyer.exists()) {
										prevBuyer.click();
										Keys.$buyers.scrollTo(prevBuyer);
									}
									break;
							}
							break;
						case Keys.m:
							if (!Keys.$messageFormWrapper.hasClass("hide")) {
								Keys.$message.focus();
								return false;
							}
							break;
						case Keys.slash:
							Keys.$search.focus();
							return false;
							break;
						case Keys.r:
							Keys.$refresh.click();
							break;
						case Keys.n:
							window.location.href = "/listings/new";
							break;
					}
				}
				if (((Keys.$search.is(":focus")) || (Keys.$message.is(":focus"))) 
					&& (keys[0] == Keys.esc)) {
					Keys.$search.blur();
					Keys.$message.blur();
					return false;
				}
				if (Keys.$search.is(":focus") && (keys[0] == Keys.enter)) {
					Keys.$search.blur();
					$(".listing").first().click();
					window.searchHasFocus = false;
					return false;
				}
			}
		}
	}
	Keys.init();

  // Init
  bindEvents();
  propogateUnreadMessages();
  // Convert links in the message text
  $(".message-content").each(function() {
		$(this).html(linkToClickable($(this).text()));
	});
});

// Context for keyboard controls
var context = "l";

// Globally declare List listings for access outside bindEvents() scope
var listings;
var searchHasFocus;
var currentFilterButton = $("#filter-not-deleted");
