function throttle(func, ms) {

	let isThrottled = false,
	  savedArgs,
	  savedThis;
  
	function wrapper() {
  
	  if (isThrottled) {
		savedArgs = arguments;
		savedThis = this;
		return;
	  }
  
	  func.apply(this, arguments);
  
	  isThrottled = true;
  
	  setTimeout(function() {
		isThrottled = false;
		if (savedArgs) {
		  wrapper.apply(savedThis, savedArgs);
		  savedArgs = savedThis = null;
		}
	  }, ms);
	}
  
	return wrapper;
  }


$(document).ready(function() {
	
	$(window).resize(function() {
		if(+$("#ifr").width() < 580 && lg == true) {
			$("#newFile span").text("NEW");
		}
		else {
			$("#newFile span").text("UPLOAD NEW");
		}

		updateTerminalHeight();
	});

	function updateTerminalHeight() {
		let img = $("#ifr");
		let tim;
		tim = setInterval(function() {
			let im_height = img.css("height");
			if (im_height != "0px") {
				if(xs == true) {
					$("#term-body").css("height", "30vh");
				}
				else {
					$("#term-body").css("height", ($("#ifr").height()-10)+"px");
				}
				clearInterval(tim);
				return false;
			}
		}, 1000);
		return false;
	};
	
	updateTerminalHeight();

	$("#prevfiles").change(function() {
        var im = $("#ifr");
        userid = im.attr("src").split('/')[3];
        var fname = $("#prevfiles :selected").text();
        if (fname != "Demo Files") {
			$("#prevfiles").val("demo");
            im.attr("src", "");
            im.attr("src", "/upload/" + fname + "/" + userid);
            vid_name = "upload/" + fname;
			$("#videoname").text(fname.slice(0, -4).replace(/-/g, " "));
			console.log('Getting terminal text for user ' + userid);

			xhr_m.open('GET', "/player/terminal/" + userid);
    		xhr_m.send();
			console.log('Got terminal text for user ' + userid);

			resetPageState();
			updateTerminalHeight();
        }
        return false;
	}).change();
	
	$("#hiddenInput").change(function() {
		$("#mainForm").submit();
	});

    var output = $("#term-body");
    var userid = $("#ifr").attr("src").split('/')[3];
    var vid_name = "upload/" + $("#ifr").attr("src").split('/')[2];
	var latestVal_m = "";
	var pos_main = 0;
	var new_result_str = ' <div class="image"><img /></div><div class="info-wrapper"><span class="type"></span><div class="time"><span class="count"></span><i class="fas fa-angle-down"></i></div></div><ul class="colled"></ul>';
	var new_timestamp_str = '<li><span></span><i class="fas fa-play-circle"></i></li>';
	var playbtn = $(".playbtn");
	var slider = document.getElementById("myRange");
	var cur_time_disp = document.getElementById("currenttime");
	var max_time_disp = document.getElementById("maxtime");
	var slider_tim;
	var videoEnded = false;
	
	var xhr_m = new XMLHttpRequest();
	console.log('Getting terminal text for user' + userid);
    xhr_m.open('GET', "/player/terminal/" + userid);
    xhr_m.send();
	console.log('Got terminal text for user' + userid);

	var xhr_vidpos =  new XMLHttpRequest();
	xhr_vidpos.open('GET', "/player/getpos/" + userid);
	xhr_vidpos.send();

	$("#detectLogos").prop("checked", true);
	$("#detectText").prop("checked", true);

    function handleNewData_main() {
        // the response text include the entire response so far
        // split the messages, then take the messages that haven't been handled yet
        // pos_main tracks how many messages have been handled
        // messages end with a newline, so split will always show one extra empty message at the end
        var messages = xhr_m.responseText.split("\n=======\n");
        messages.slice(pos_main, -1).forEach(function(value) {
			var json_val = JSON.parse(value);
            if (latestVal_m != value && json_val["video"] == vid_name) {
				latestVal_m = value; // update the latest value in place
				
				let msg_src = json_val["source"];

				var res_div = $('.result[data-id="'+json_val["counter"]+'"]');

				$("#stats span").text((parseInt($("#stats span").text()) + 1).toString());
				$("#stats span").css("padding", ($("#stats span").text().length-1)*4+2+"px 8px");

				
				if(res_div.length) {
					//update existing item
					res_div.addClass("active");
					let cnt = res_div.find(".count");
					let new_qty = parseInt(cnt.text()) + 1;
					if (new_qty > 1) {
						cnt.text(new_qty.toString()+" "+msg_src+"s");
					}
					else {
						cnt.text(new_qty.toString()+" "+msg_src);
					}

					let new_stamp = $.parseHTML(new_timestamp_str);
					
					$(new_stamp).find("span").attr("data-time", json_val["time"]);
					$(new_stamp).find("span").text(fmtMSS(json_val["time"]/1000)+"."+parseInt(json_val["time"]%1000));
					$(new_stamp).find("span").click(function() {
						if (!videoEnded) {
							clearInterval(slider_tim);
							var millis = parseInt($(this).attr("data-time"));
							slider.value = millis/1000;
							cur_time_disp.innerHTML = fmtMSS(slider.value);
							$.get("/player/seek/"+userid+"/"+millis, function(resp) {
								slider_tim = setInterval(incrementSliderPos, 1000);
							});
							playbtn.addClass("paused");
						}
					});

					$(new_stamp).find(".fa-play-circle").click(function() {
						$(this).prev().click();
					});

					let stamp_list = res_div.find(".colled");
					stamp_list.append(new_stamp);
					if (res_div.find(".time").hasClass("flipped")) { //if expanded
						stamp_list.css("maxHeight", stamp_list.get(0).scrollHeight + "px");
					} 

					setTimeout( function(){
						res_div.removeClass("active");
					},300);

					switch(isVisible(res_div, $("#term-body"))) {
						//up
						case 1: {
							$("#hiddenResultsup span").text((parseInt($("#hiddenResultsup span").text()) + 1).toString());
							$("#hiddenResultsup").css("opacity", 1);
							res_div.addClass("hidden-up");
							res_div.data("hiddencount") ?
							res_div.data().hiddencount++ :
							res_div.data("hiddencount", 1);
							break;
						}
						//down
						case -1: {
							$("#hiddenResultsdown span").text((parseInt($("#hiddenResultsdown span").text()) + 1).toString());
							$("#hiddenResultsdown").css("opacity", 1);
							res_div.addClass("hidden-down");
							res_div.data("hiddencount") ?
							res_div.data().hiddencount++ :
							res_div.data("hiddencount", 1);
							break;
						}
					}
				}
				else {
					if(msg_src == "Meta") {
						playbtn.removeClass("paused");
						clearInterval(slider_tim);
						videoEnded = true;
						return;
					}
					// build and append a new item to the result list
					let item = $(document.createElement("div"));
					item.append($.parseHTML(new_result_str));
					item.addClass(" result active result-"+msg_src.toLowerCase());
					item.attr("data-id", json_val["counter"]); //ordinary id has character limits
					item.find(".image img").attr("src", "../static/images/logos/"+json_val["image"]);
					item.find(".type").html(json_val["info"]);

					let link = item.find(".type a").attr("href");
					if(link) {
						item.find(".image img").wrap(`<a target="_blank" href="${link}"></a>`)
					}

					item.find(".time").click(function() {
						$(this).toggleClass("flipped");
						var coll = this.parentNode.nextElementSibling;
						if (coll.style.maxHeight){
							coll.style.maxHeight = null;
						  } else {
							coll.style.maxHeight = coll.scrollHeight + "px";
						  } 
					});
					item.find(".count").text("1 "+msg_src);

					let new_stamp = $.parseHTML(new_timestamp_str);
					
					$(new_stamp).find("span").attr("data-time", json_val["time"]);
					$(new_stamp).find("span").text(fmtMSS(json_val["time"]/1000)+"."+parseInt(json_val["time"]%1000));
					$(new_stamp).find("span").click(function() {
						if (!videoEnded) {
							clearInterval(slider_tim);
							var millis = parseInt($(this).attr("data-time"));
							slider.value = millis/1000;
							cur_time_disp.innerHTML = fmtMSS(slider.value);
							$.get("/player/seek/"+userid+"/"+millis, function(resp) {
								slider_tim = setInterval(incrementSliderPos, 1000);
							});
							playbtn.addClass("paused");
						}
					});

					$(new_stamp).find(".fa-play-circle").click(function() {
						$(this).prev().click();
					});

					item.find(".colled").append(new_stamp);

					item.css("opacity", "0");
					output.append(item);
					setTimeout( function(){
						item.css("opacity", "1");
					},100);
					
					setTimeout( function(){
						item.removeClass("active");
					},300);
					//scroll to new item
					output.animate({
						scrollTop:output[0].scrollHeight
					}, 800);
				}
            }
        });
        pos_main = messages.length - 1;
	};

	function incrementSliderPos() {
		var messages = xhr_vidpos.responseText.split("!!!");
		var latest_val = messages[messages.length-1];
		if (latest_val == "") {
			slider.value = parseFloat(slider.value)+1;
		}
		else {
			slider.value = parseInt(latest_val)/1000;
		}
		
		cur_time_disp.textContent = fmtMSS(slider.value);
		
		if(parseInt(slider.value) + 1 >slider.max) {
			console.log("stopped incremming");
			clearInterval(slider_tim);
			videoEnded = true;	
		}
		
		if (xhr_vidpos.readyState == XMLHttpRequest.DONE) {
            console.log("STOPPED position request! Resending...");
			xhr_vidpos.open('GET', "/player/getpos/" + userid);
            xhr_vidpos.send();
        }	
	}

	function isVisible( element, container ){
		///returns -1 if element is below, 1 if it is above visible area
		var elementTop = $(element).offset().top,
			elementHeight = $(element).height(),
			containerTop = $(container).offset().top,
			containerHeight = $(container).height();
		
		if(((elementTop - containerTop) > containerHeight)) {
			return -1;
		}
		else if((((elementTop - containerTop) + elementHeight) < 0)) {
			return 1;
		}
		
		return 0;
	  }

	function resetPageState() {
		let im = $("#ifr");
		output.empty();
		$("#stats span").text("0");
		$("#stats span").css("padding", "2px 8px");
		$("#hiddenResultsup span").text("0");
		$("#hiddenResultsup").css("opacity", 0);
		$("#hiddenResultsdown span").text("0");
		$("#hiddenResultsdown").css("opacity", 0);
		videoEnded = false;
		let vidready_tim;
		clearInterval(slider_tim);
		vidready_tim = setInterval(function() {
			if(im.css("height") != "0px") {
				$.get("/player/getduration/"+userid, function(resp) {
					slider.max = resp;
					max_time_disp.innerHTML = fmtMSS(resp);
				});

				slider.value = 0;
				slider_tim = setInterval(incrementSliderPos, 1000);
				playbtn.addClass("paused");
				clearInterval(vidready_tim);
			}
		}, 500)
	}

	$(".playbtn-cont").click(function() {

		playbtn.toggleClass("paused");
		if (videoEnded && playbtn.hasClass("paused")) {
			var im = $("#ifr");
			var src_str = im.attr("src");
			im.attr("src", "");
			let vidempty_tim;
			vidempty_tim = setInterval(function() {
				if(im.css("height") == "0px") {
					im.attr("src", src_str);
					clearInterval(vidempty_tim);
				}
			}, 500);

			resetPageState();
		}
		else {
			$.get("/player/playpause/"+userid, function(resp) {
				if(playbtn.hasClass("paused")) {
					slider_tim = setInterval(incrementSliderPos, 1000);
				}
				else {
					clearInterval(slider_tim);
				}
			});
		}
		
		return false;
	  });

	$("#detectLogos").click(function() {

		$.get("/player/choption/"+userid+"/detectlogos/"+this.checked);
	});

	$("#detectText").click(function() {
		$.get("/player/choption/"+userid+"/detecttext/"+this.checked);
	});

	var updateHiddenCounters = throttle(function(){
		let target =  this.oldScroll > this.scrollTop ? "up" : "down";

		$(".hidden-"+target).each(function() {
			let state = isVisible(this, "#term-body");
			if(state == 0 || (state == 1  && target== "down") || 
			   (state == -1  && target== "up")) {
				   $(this).removeClass("hidden-"+target);
				   $("#hiddenResults"+target+" span").text((parseInt($("#hiddenResults"+target+" span").text()) - $(this).data("hiddencount")).toString());
				   $(this).removeData("hiddencount");

				   if(parseInt($("#hiddenResults"+target+" span").text())<=0) {
					$("#hiddenResults"+target).css("opacity", 0);
					$("#hiddenResults"+target+" span").text("0");
				   }
				   
			   }
		});
		this.oldScroll = this.scrollTop;
  }, 200);

	$("#term-body").on("scroll", updateHiddenCounters);
	
	slider.value = 0;
	slider_tim = setInterval(incrementSliderPos, 1000);
	
	function fmtMSS(s){s=Math.floor(s); return(s-(s%=60))/60+(9<s?':':':0')+s}
	
	slider.oninput = function() {
		cur_time_disp.innerHTML = fmtMSS(this.value);
	}
	
	slider.onmousedown = function(e) {
		if (e.button == 0) {
			clearInterval(slider_tim);
		}
	}
	
	slider.onmouseup = function(e) {
		if (e.button == 0 && !videoEnded) {
			var millis = slider.value * 1000;
			$.get("/player/seek/"+userid+"/"+millis, function(resp) {
				slider_tim = setInterval(incrementSliderPos, 1000);
			});
			playbtn.addClass("paused");
		}
	}
	
	$.get("/player/getduration/"+userid, function(resp) {
		slider.max = resp;
		max_time_disp.innerHTML = fmtMSS(resp);
	});

    var timer;
    timer = setInterval(function() {
        // check the response for new data
        handleNewData_main();
        if (xhr_m.readyState == XMLHttpRequest.DONE) {
            console.log("STOPPED terminal! Resending...");
			xhr_m.open('GET', "player/terminal/" + userid);
            xhr_m.send();
			console.log('Got terminal text for user' + userid);

			pos_main = 0;
        }
	}, 1000);
});