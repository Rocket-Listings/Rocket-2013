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

	// Toggle the checkboxes
	$(".check-all").click(function () {
		if (this.checked) {
			$(".check-one").prop('checked', true);
		}
		else {
			$(".check-one").prop('checked', false);
		}
	});

	// Scroll messages to bottom
	$.fn.scrollBottom = function() {
		$(this).scrollTop($(this)[0].scrollHeight);
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
		$(".messages-body").html("").append(Mustache.render($("#new-message").html(), {'messages': data.messages}));
		$(".buyers-body").html("").prepend(Mustache.render($("#new-buyer").html(), {'buyers': data.buyers}));
		$(".listings-body ul.list").html("").prepend(Mustache.render($("#new-listing").html(), {'listings': data.listings}));
		// Reset the filter button
		$("a.dropdown-btn").text("All");
	}

	// Bind clicks and list init to the current items
	function bindEvents() {
		$('.listings-body li').click(function () {
			var listingRow = $(this),
				id = listingRow.data('listing-id'),
				buyers = $(".listing-" + id);
			$('.listings-body li').removeClass('highlight');
			listingRow.addClass('highlight');
			$(".message").addClass("hide");
			$(".buyer-card").addClass("hide");
			if(buyers.length) {
				buyers.removeClass("hide");
				buyers.first().click();
				$('.message-form-wrapper').removeClass("hide");
				$('.messages-body').scrollBottom();
			} else {
				$('.message-form-wrapper').addClass("hide");
			}
		});

		$('.buyer-card').click(function(event){
			var buyerCard = $(this),
				buyer_id = buyerCard.data('buyer-id'),
				listing_id = buyerCard.data('listing-id');
			$('.buyer-card').removeClass('highlight');
			buyerCard.addClass('highlight');
			$(".message").addClass("hide");
			$('.buyer-' + buyer_id).removeClass("hide");
			$(".message-form input[name='listing']").val(listing_id);
			$(".message-form input[name='buyer']").val(buyer_id);
			$('.messages-body').scrollBottom();
			//$(".message-form textarea").focus();
		});

		var options = {
			valueNames: ['title', 'price', 'category', 'date', 'status']
		};

		window.listings = new List('dashboard-content', options);
	}

	// Unbind click events from current items
	function unbindEvents() {
		$('.listings-body li, .buyer-card').unbind('click');
	}

	// Keyboard controls
	$(document).keydown(function(e) {
		var listings = $('.listings-body'),
			buyers = $('.buyers-body'),
			currentSelectedListing = listings.find("li.highlight"),
			currentSelectedBuyer = buyers.find('ul.highlight'),
			key = e.which || e.keyCode;
		if (!$('.message-form textarea').is(":focus")) {
			if (key == "66") window.context = "b"; // B
			if (key == "76") window.context = "l"; // L
			if ((key == '74') || (key == '40')) {
				// J || DOWN
				if (context == "l") {
					currentSelectedListing.next('li').click();
					listings.scrollTo(currentSelectedListing.next('li'));
				}
				if (context == "b") {
					currentSelectedBuyer.next('ul').click();
					buyers.scrollTo(currentSelectedBuyer.next('ul'));
				}
			}
			if ((key == '75') || (key == '38')) {
				// K || UP
				if (context == "l") {
					currentSelectedListing.prev('li').click();
					listings.scrollTo(currentSelectedListing.prev('li'));
				}
				if (context == "b") {
					currentSelectedBuyer.prev('ul').click();
					buyers.scrollTo(currentSelectedBuyer.prev('ul'));
				}
			}
			if ((key == '77') && (!$('.message-form-wrapper').hasClass('hide'))) {
				// M
				$(".message-form textarea").focus();
				return false;
			}
		}
		if (($('.message-form textarea').is(":focus")) && (key == "27")) {
			// ESC
			$(".message-form textarea").blur();
		}
	});

	$('.close').click(function(event){
		$('.dashboard-panel').removeClass("first-visit");
	});

	// Autopost from dashboard (Deprecated)
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

	$(".dashboard-refresh").click(function (e) {
		e.preventDefault();
		var currentSelectedListing = $(".listings-body").find("li.highlight").data('listing-id');
		$.ajax({
			type: 'GET',
			url: '/listings/dashboard/data/',
			// data: {'listing': $(".last-listing").text(),
			// 	   'buyer': $(".last-buyer").text(),
			// 	   'message': $(".last-message").text()},
			success: function (response) {
				insertNewData(response);
				unbindEvents(); // To prevent overlap
				bindEvents(); // Bind all items (including new)
				if (currentSelectedListing != null) {
					$(".listings-body").find("li[data-listing-id='" + currentSelectedListing + "']").click();
				}
				else { $(".listings-body li").first().click(); }
			}
		});
	});

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

	// Check the status of a listing (Deprecated)
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

	$(".message-content").each(function() {
		$(this).html(linkToClickable($(this).text()));
	});

	bindEvents();

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
        $(".buyer-card, message").addClass("hide");
        $(".listings-body li").first().click();
        return false;
    });

    $('#filter-none').click(function() {
        window.listings.filter();
        return false;
    });

    $('.dashboard-dropdown .dropdown-menu a').click(function() {
    	$(this).parent().parent().prev('a.dropdown-btn').text($(this).text());
    	$('.dropdown-menu').dropdown('toggle');
    	$(".listings-body li").first().click();
    	$(".listings-body").scrollTop(0);

    });

    $('.listings-body li').first().click();
});

// Context for keyboard controls
var context = "l";

// Globally declare List listings for access outside bindEvents() scope
var listings;