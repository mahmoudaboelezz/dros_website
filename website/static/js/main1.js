// when document is ready, run this function
$(document).ready(function() {
    // when collapse button is clicked, hide all other collapse buttons and show the one that was clicked
    // buttun with class of 'collapse'
    $('[data-toggle="collapse"]').on('click', function() {
        // add class 'collapsed' to other collapse buttons except the one that was clicked
        $('[data-toggle="collapse"]').not(this).addClass('collapsed');
        $('[data-toggle="collapse"]').not(this).removeClass('active');
        // add class active to the button that was clicked
        $(this).toggleClass('active');
        // set aria-expanded to false for all collapse buttons except the one that was clicked
        $('[data-toggle="collapse"]').not(this).attr('aria-expanded', 'false');
        
        // get the data-target attribute of other collapse buttons except the one that was clicked
        var target = $('[data-toggle="collapse"]').not(this)
            .attr('data-target');
        // hide the other collapse buttons except the one that was clicked
        $(target).collapse('hide');
        
        
    });


    // when user click on button with class 'complete-lesson', run this function
    $('.complete-lesson').on('click', function() {
        // get the id of the lesson that was clicked
        var lesson_id = $(this).attr('id');
        // add class 'completed' to the button that was clicked and store in local storage with key of lesson_id
        $(this).addClass('completed');
        localStorage.setItem(lesson_id, 'completed');
        // get [data-toggle="collapse"] that has class 'active' and and add class 'completed' to it
        $('[data-toggle="collapse"].active').addClass('completed');
    });
    // if local storage has key of lesson_id, add class 'completed' to the button that was clicked
    $('.complete-lesson').each(function() {
        var lesson_id = $(this).attr('id');
        if (localStorage.getItem(lesson_id) == 'completed') {
            $(this).addClass('completed');
            // get data-complete attribute of the button that was clicked and add class 'completed' to it
            data_target = $(this).attr('data-complete');
            console.log(data_target);
            // get [data-toggle="collapse"] that has data-target attribute of data_target and add class 'completed' to it
            $('[data-toggle="collapse"][data-target="' + data_target + '"]').addClass('completed');
            
        }
    });


});