
$(document).ready(function(){

	setInterval(score_refresh, 5000);

	function score_refresh(){

		var pk = {{match.id}};

		$.get({
			url: '{% url 'scorecard' %}',
			data: {
			  'pk': pk
			},
			dataType: 'json',
			success: function (data) {
				if (data) {
					$('#TeamA').html(data[0]);
					$('#TeamAScore').html(data[1]);
					$('#OddsTA').html(data[2]);
					$('#TeamB').html(data[3]);
					$('#TeamBScore').html(data[4]);
					$('#OddsTB').html(data[5]);

					var notes = data[6];
					if (notes == 'Not updated') {
						$('#MatchNotes').addClass('is-hidden');
						$('#Board').addClass('is-marginless');
					} else {
						$('#Board').removeClass('is-marginless');
						$('#MatchNotes').removeClass('is-hidden');
						$('#MatchNotes').html(notes);
					}
					

					var prediction = data[7];
					if (prediction) {
						$('#Prediction').html(prediction);
						$('#Prediction').removeClass('is-hidden');
					} else {
						
						$('#Prediction').addClass('is-hidden');
					}

					
					$('#OddsTeamA').html(data[8]);
					$('#OddsTeamB').html(data[9]);

					var status = data[10];
					if (status == 'completed') {
						$('#ODDS').hide();
					} else {
						$('#ODDS').show();
					}

					var OddsTA = data[2];
					var OddsTB = data[5];
					var OddsTeamA = data[8];
					var OddsTeamB = data[9];
					if (OddsTA == '0' && OddsTB == '0' && OddsTeamA == '0' && OddsTeamB == '0') {
						$('#ODDS').addClass('is-hidden');
					} else {
						$('#ODDS').removeClass('is-hidden');
					}

				}
			}
		});
	}

});