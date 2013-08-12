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
		// Reset the filter button
		$("a.dropdown-btn").text("Filter");
	}

	// Bind clicks and list init to the current items
	function bindEvents() {
		$('.listing').click(function () {
			var listingRow = $(this),
				id = listingRow.data('listing-id'),
				buyers = $(".buyer[data-listing-id='" + id + "']");
			$('.listing').removeClass('highlight');
			listingRow.addClass('highlight');
			$(".message, .buyer").addClass("hide");
			$(".dashboard-delete a").attr('data-listing-id', id).removeClass("disabled");
			if (buyers.length) {
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
					}
				});
			});
		});

		// Initialize the listings globally for List.js
		var options = {
			valueNames: ['title', 'price', 'category', 'date', 'status']
		};

		window.listings = new List('dashboard-content', options);
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

	// Keyboard controls
	$(document).keydown(function(e) {
		console.log(e);
		var listings = $('.listings-body'),
			buyers = $('.buyers-body'),
			currentSelectedListing = listings.find("li.highlight"),
			currentSelectedBuyer = buyers.find('ul.highlight'),
			key = e.which || e.keyCode;
		if (!$('input.search, textarea').is(":focus"))  {
			if ((key == "66") || (key == "39")) window.context = "b"; // B || RIGHT
			if ((key == "76") || (key == "37")) window.context = "l"; // L || LEFT
			if ((key == '74') || (key == '40')) {
				// J || DOWN
				if (context == "l") {
					var nextListing = currentSelectedListing.next('li:not(.hide)');
					if (nextListing.exists()) {
						nextListing.click();
						listings.scrollTo(nextListing);
					}
				}
				if (context == "b") {
					var nextBuyer = currentSelectedBuyer.next('ul:not(.hide)');
					if (nextBuyer.exists()) {
						nextBuyer.click();
						buyers.scrollTo(nextBuyer);
					}
				}
			}
			if ((key == '75') || (key == '38')) {
				// K || UP
				if (context == "l") {
					var prevListing = currentSelectedListing.prev('li:not(.hide)');
					if (prevListing.exists()) {
						prevListing.click();
						listings.scrollTo(prevListing);
					}
				}
				if (context == "b") {
					var prevBuyer = currentSelectedBuyer.prev('ul:not(.hide)');
					if (prevBuyer.exists()) {
						prevBuyer.click();
						buyers.scrollTo(prevBuyer);
					}
				}
			}
			if ((key == '77') && (!$('.message-form-wrapper').hasClass('hide'))) {
				// M
				$(".message-form textarea").focus();
				return false;
			}
			if (key == "191") {
				// \/
				$("input.search").focus();
				return false;
			}
			if (key == "82") {
				// R
				$(".dashboard-refresh").click();
			}
			if (key == "78") {
				// N
				window.location.href = "/listings/create"
			}
		}
		if (($('input.search, textarea').is(":focus")) && (key == "27")) {
			// ESC
			$("input.search, textarea").blur();
		}
		if ($("input.search").is(":focus") && key == "13") {
			// ENTER
			$("input.search").blur();
			$(".listing").first().click();
			return false;
		}
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

	// Delete the currently selected listing
	$(".dashboard-delete a").click(function (e) {
		var id = $(this).attr('data-listing-id');
		e.preventDefault();
		if (!$(this).hasClass("disabled")) {
			$.ajax({
				url: '/listings/' + id + '/delete',
				method: 'GET',
				success: function () {
					$("li[data-listing-id='" + id +"']").remove();
					$(".listing-" + id).remove();
					unbindEvents(); // To prevent overlap
					bindEvents(); // Bind all items (including new)
					$(".listings-body li").first().click();
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
		$(".buyer, .message, .message-form-wrapper").addClass("hide");
		$(".listings-body li").removeClass("highlight");
		$(".buyers-body").removeClass("border-right");
		$(".no-messages").removeClass("hide");
		$(".dashboard-delete a").addClass("disabled");
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
    	$(".sidebar-button-wrapper").removeClass('selected');
    	$(this).parent().addClass('selected');
    	$(".listing").first().click();
    	$(".listings-body").scrollTop(0);

    });

    // Convert links in the message text
    $(".message-content").each(function() {
		$(this).html(linkToClickable($(this).text()));
	});

    // Init
    bindEvents();
    propogateUnreadMessages();
    $("#filter-not-deleted").click();
});

// Context for keyboard controls
var context = "l";

// Globally declare List listings for access outside bindEvents() scope
var listings;
