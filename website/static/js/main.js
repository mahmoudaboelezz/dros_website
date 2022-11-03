(function () {
	"use strict";

	var treeviewMenu = $('.app-menu');

	// Toggle Sidebar
	$('[data-toggle="sidebar"]').click(function(event) {
		event.preventDefault();
		$('.app').toggleClass('sidenav-toggled');
	});

	// Activate sidebar treeview toggle
	$("[data-toggle='treeview']").click(function(event) {
		event.preventDefault();
		if(!$(this).parent().hasClass('is-expanded')) {
			treeviewMenu.find("[data-toggle='treeview']").parent().removeClass('is-expanded');
		}
		$(this).parent().toggleClass('is-expanded');
	});

	// Set initial active toggle
	$("[data-toggle='treeview.'].is-expanded").parent().toggleClass('is-expanded');

	//Activate bootstrip tooltips
	$("[data-toggle='tooltip']").tooltip();

})();


// when the page is ready
$(document).ready(function() {
	// add active class to element with href equal to current page
	$('a[href="' + this.location.pathname + '"]').addClass('active');
	// override the javascript alert function
	
	
});

// when the page is ready
$(document).ready(function() {
	// get button with id delete
	var deleteButton = $('#delete');
	// when the button is clicked
	deleteButton.click(function() {
		event.preventDefault();
		Swal.fire({
			title: 'Are you sure?',
			text: "You won't be able to revert this!",
			icon: 'warning',
			showCancelButton: true,
			confirmButtonColor: '#d33',
			cancelButtonColor: '#009688',
			confirmButtonText: 'Yes, delete it!'
		}).then((result) => {
			if (result.value) {
				// if the user confirms, submit the form
				console.log('submitting form');
				$('#delete-form').submit();
				console.log($('#delete-form'));
			}
		})
		
	})
});
