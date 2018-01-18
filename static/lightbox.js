
//var carousel = document.getElementById('carousel-b');
var lightbox = document.querySelector('.lightbox');

// Display lightbox
$('#carousel-b').on('dblclick', function(){
    console.log('double click');

    lightbox.style.display = 'block';
    
})

//var area = document.querySelector('.lightbox');

$('.lightbox').on('click', function(e) {
    // check if we click around picture
    if (e.target.className === 'lightbox'){
        lightbox.style.display = 'none';
    }
})

$(document).keydown(function(e) {
    if( e.keyCode === 27 ) {
        lightbox.style.display = 'none';
    }
});
// close pressing cross
$('.closex').click(function(e) {
    lightbox.style.display = 'none';
})
    

// Sync slider
$('#carousel-b').on('click','a',function(e){
    lazyLoad.displayOnly(nextPrev(e, 'b'))
    lazyLoad.linkAction(nextPrev(e, 'b'))
    var other = 'a';
    $('#carousel-' + other).carousel(this.getAttribute('data-slide'));
})


$('#carousel-a').on('click','a',function(e){
    lazyLoad.displayOnly(nextPrev(e, 'a'))
    lazyLoad.linkAction(nextPrev(e, 'a'))
    var other = 'b';
    $('#carousel-' + other).carousel(this.getAttribute('data-slide'));
})


// Sync controls

$('.controls').on('click','a',function(e){
    var link = parseInt(this.getAttribute('data-slide-to'));
    lazyLoad.displayOnly(link);
    lazyLoad.linkAction(link);

    // change active color
    if($(".chosen").length){
        $(".chosen")[0].classList.remove('chosen')
    };

    this.classList.add("chosen");


    $('#carousel-a').carousel(link);
    $('#carousel-b').carousel(link);
});
// add color to A after load

// $(document).ready(function() {
//     if ($('.controls').find("a").length) {
//         $('.controls').find("a")[0].classList.add("chosen");
//         $('.controls').parent().find("#chapter-link")[0].classList.add("chosen-main");
//     }
// });

// move carousel from comments link

$('#comments').on('click','a',function(e){
    var link = this.getAttribute('data-slide-to');
    console.log(this.getAttribute('data-slide-to'));
    $('#carousel-a').carousel(parseInt(link));
    $('#carousel-b').carousel(parseInt(link));
});

function activeSlide(){
    var activeSlide = $('#carousel-b .active').index();
    return activeSlide
};
// check if we go next of back
function nextPrev(e, carousel){
    var className = e.currentTarget.className;
    var active = activeSlide();
    console.log('active is ' +active);
    var numberOfSlides = $('#carousel-' + carousel).find('.item').length - 1;
    console.log('# of slides ' + numberOfSlides );
    if (className === 'carousel-control-next'){
        if (active === numberOfSlides){
            return 0;
        } else{
            return active + 1;
        };
    } else if (className === 'carousel-control-prev'){
        if (active === 0){
            return numberOfSlides;
        } else{
            return active - 1;
        };
    }
};

// check slides on load
window.onload = function() {
    lazyLoad.displayOnly(0);
    lazyLoad.linkAction(0);
}

// Load more 
var lazyLoad ={
    allowedNumber: 2,
    step: 2,
    currentNumber: 2,
    activeSlide: 0,
    link: $('#lazyLoadLink'),
    // hide or show link based on its status
    linkAction: function(slide){ 
        if(this.status(slide)){ 
            this.link.hide();
            this.reset();
        } else {
            this.link.show();
        };
    }, 
    status: function(slide){
        // return true if link is needed
        var result = (this.totalNumberOfCommentsX(slide) <= this.currentNumber) ?  true :  false;
        return result
    } ,
    reset: function(){
        this.currentNumber = 2;
    },
    increase: function(){
        this.currentNumber += this.step;
    },
    totalNumberOfComments: function(){
        return $( "#comments" ).find( "*.container" ).length;
    },
    totalNumberOfCommentsX: function(slide){
        return $(".container[data-slide='" + slide + "']").length;
    },
    displayOnly: function(slide) {
        var $allContainers = $( "#comments" ).find( "*.container" );
        var display = [];
        for (i = 0; i < $allContainers.length; i++){
            $allContainers[i].style.display = 'none';
            if (parseInt($allContainers[i].dataset.slide) == slide) {
                display.push($allContainers[i])
                //$allContainers[i].style.display = 'block';
            }; 
        };
        // display only withing range
        // check if the list long enough
        var number = (display.length <  this.currentNumber) ? display.length : this.currentNumber;
        for (i = 0; i < number; i++){
            display[i].style.display = 'block';
        
        };
    }
};

// Manage lazy load link
$('#lazyLoadLink').on('click', function(){
    lazyLoad.increase();
    lazyLoad.displayOnly(activeSlide());
    lazyLoad.linkAction(activeSlide());
});

// Normalize bootstrap carousel hight
// function carouselNormalization() {
//     var items = $('#carousel-b .item'), //grab all slides
//         heights = [], //create empty array to store height values
//         tallest; //create variable to make note of the tallest slide
    
//     if (items.length) {
//         function normalizeHeights() {
//             items.each(function() { //add heights to array
//                 heights.push($(this).height()); 
//             });
//             tallest = Math.max.apply(null, heights); //cache largest value
//             items.each(function() {
//                 $(this).css('min-height',tallest + 'px');
//             });
//         };
//         normalizeHeights();
    
//         $(window).on('resize orientationchange', function () {
//             tallest = 0, heights.length = 0; //reset vars
//             items.each(function() {
//                 $(this).css('min-height','0'); //reset min-height
//             }); 
//             normalizeHeights(); //run it again 
//         });
//     }
//     }
//     $(document).ready(carouselNormalization);

// double tap
(function($){

    $.event.special.doubletap = {
      bindType: 'touchend',
      delegateType: 'touchend',
  
      handle: function(event) {
        var handleObj   = event.handleObj,
            targetData  = jQuery.data(event.target),
            now         = new Date().getTime(),
            delta       = targetData.lastTouch ? now - targetData.lastTouch : 0,
            delay       = delay == null ? 300 : delay;
  
        if (delta < delay && delta > 30) {
          targetData.lastTouch = null;
          event.type = handleObj.origType;
          ['clientX', 'clientY', 'pageX', 'pageY'].forEach(function(property) {
            event[property] = event.originalEvent.changedTouches[0][property];
          })
  
          // let jQuery handle the triggering of "doubletap" event handlers
          handleObj.handler.apply(this, arguments);
        } else {
          targetData.lastTouch = now;
        }
      }
    };
  
  })(jQuery);

  // doubletouch
  $('#carousel-b').on('doubletap',function(e){
        lightbox.style.display = 'block';
    });