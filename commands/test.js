
        $(function() {
	    
	    $('#gen-form').on('submit', function(e){
		e.preventDefault();
		var story_id = -1;
		while(parseInt(getCookie("last_story_id")) ===  parseInt(story_id) || parseInt(story_id) === -1){
		    story_id = get_random_story_id();
		}
		
		console.log(story_id);
		console.log(getCookie("last_story_id"));
		process_start(story_id);
	    });
	    
	    function get_random_story_id(){
		var story_ids = new Array(4,5,6,7,8,9,10,11,12);
		var story_id = story_ids[Math.floor(Math.random()*story_ids.length)];
		return story_id;
	    }
	    var game_id = 0;
	    
	    function getCookie(name) {
		const value = `; ${document.cookie}`;
		const parts = value.split(`; ${name}=`);
		if (parts.length === 2) return parts.pop().split(';').shift();
	    }
	    function process_start(story_id){
		$('#generate-text').addClass("is-loading");
		$('#generate-text').prop("disabled", true);
		$.ajax({
		    type: 'POST',
		    url: 'api_interactive_fiction.php',
		    data: {
			start: 1,
			story_id: story_id
		    },
		    success: function (response, textStatus, jqXHR) {
			$('#generate-text').removeClass("is-loading");
			$('#generate-text').prop("disabled", false);
			
			//var $html = response.html;
			game_id = response.game_id;
			$('#model-output').empty();
			var html = '<div class=\"gen-box\">' + response.html + '</div><div class="gen-border"></div>';
			$(html).appendTo('#model-output').hide().fadeIn("slow");

			$('#generate-text').hide();
			
			$('html, body').animate({
			    scrollTop: $(".spn_story_text").offset().top - 200
			}, 1000);
		    },
		    dataType: 'JSON'
		});
	    }

	    function process_response(choice){
		$.ajax({
		    type: 'POST',
		    url: 'api_interactive_fiction.php',
		    data: {
			start: 0,
			choice: choice,
			game_id: game_id
		    },
		    success: function (response, textStatus, jqXHR) {
			//var $html = response.html;
			
			$('#model-output').empty();
			var html = '<div class=\"gen-box\">' + response.html + '</div><div class="gen-border"></div>';
			$(html).appendTo('#model-output').hide().fadeIn("slow");
			
			//$('#model-output').html($html);

			if(parseInt(response.ended) === 1){
			    $('#generate-text').find('span').eq(1).text('Generate Another Story!');
			    $('#generate-text').fadeIn('slow');
			}
			$('html, body').animate({
			    scrollTop: $(".spn_story_text").offset().top - 200
			}, 1000);
		    },
		    dataType: 'JSON'
		});
	    }

	    $(document).on('click', '.btn_choice', function(){
		var choice = $(this).data('choice_key');
		process_response(choice);
	    });


//            $('#gen-form').submit(function(e) {
//                    e.preventDefault();
//                    $.ajax({
//                            type: "POST",
//                            url: "api_interactive_fiction.php",
//                            data: {
//                                'stories': true
//                            },
//                            //dataType: "json",
//                            //data: JSON.stringify(getInputValues()),
//                            beforeSend: function(data) {
//                                $('#generate-text').addClass("is-loading");
//                                $('#generate-text').prop("disabled", true);
//                                var html = '';
//                                title = '';
//                            },
//                            success: function(data) {
//                                // $('#generate-text').removeClass("is-loading");
//                                $('#generate-text').prop("disabled", false);
//                                $('#tutorial').remove();
//
//                                $('#generate-text').removeClass("is-loading");
//                                if (data) {
//                                    $('#model-output').html("");
//                                    // data = JSON.parse(data);
//                                    // gentext = data.lyrics;
//                                    var html = '<div class=\"gen-box\">' + data + '</div><div class="gen-border"></div>';
//                                    $(html).appendTo('#model-output').hide().fadeIn("slow");
//                                } else {
//                                    $('#generate-text').removeClass("is-loading");
//                                    $('#generate-text').prop("disabled", false);
//                                    $('#tutorial').remove();
//                                    var html = '<div class="gen-box warning">There was an error generating the story! Please try again!</div><div class="gen-border"></div>';
//                                    $(html).appendTo('#model-output').hide().fadeIn("slow");
//                                }
//                            if ($("#prefix").length & $("#prefix").val() != '') {
//                                var pattern = new RegExp('^' + $("#prefix").val(), 'g');
//                                var gentext = gentext.replace(pattern, '<strong>' + $("#prefix").val() + '</strong>');
//                            }
//                        },
//                        error: function(jqXHR, textStatus, errorThrown) {
//                            $('#generate-text').removeClass("is-loading");
//                            $('#generate-text').prop("disabled", false);
//                            $('#tutorial').remove();
//                            var html = '<div class="gen-box warning">There was an error generating the story! Please try again!</div><div class="gen-border"></div>';
//                            $(html).appendTo('#model-output').hide().fadeIn("slow");
//                        }
//                    });
//            }); 
	    $('#clear-text').click(function(e) {
		$('#model-output').text('')
	    });
        // https://stackoverflow.com/a/51478809
        $("#save-image").click(function() {
            html2canvas(document.querySelector('#model-output')).then(function(canvas) {
                saveAs(canvas.toDataURL(), 'gen_texts.png');
            });
        });
        });

        function getInputValues() {
            var inputs = {};
            $("textarea, input").each(function() {
                inputs[$(this).attr('id')] = $(this).val();
            });
            return inputs;
        }
        // https://stackoverflow.com/a/51478809
        function saveAs(uri, filename) {
            var link = document.createElement('a');
            if (typeof link.download === 'string') {
                link.href = uri;
                link.download = filename;
                //Firefox requires the link to be in the body
                document.body.appendChild(link);
                //simulate click
                link.click();
                //remove the link when done
                document.body.removeChild(link);
            } else {
                window.open(uri);
            }
        }
    