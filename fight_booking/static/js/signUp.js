$(function(){
	$('#btnSignUp').click(function(){
		window.alert("Signup");
		$.ajax({
			url: '/signup',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
				window.alert(response);
			},
			error: function(error){
				console.log(error);
				window.alert(response);
			}
		});
	});
});