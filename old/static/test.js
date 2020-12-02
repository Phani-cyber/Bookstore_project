$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				name : $('#emailInput').val(),
				email : $('#passwordInput').val()
			},
			type : 'POST',
			url : '/login_submit'
		})
		.done(function(data) {

			if (data.login) {
                window.location.href = '/books';
                
			}
			else {
				$('#errorAlert').text(data.invalid).show();
				$('#successAlert').hide();
			}

		});

		event.preventDefault();

	});

});