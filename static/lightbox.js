
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
    $('#carousel-a').carousel(link);
    $('#carousel-b').carousel(link);
});

// move carousel from comments link

$('#comments').on('click','a',function(e){
    var link = this.getAttribute('data-slide-to');
    console.log(this.getAttribute('data-slide-to'));
    $('#carousel-a').carousel(parseInt(link));
    $('#carousel-b').carousel(parseInt(link));
});

// Display only related comments
// function changeComments(active){
//     var $allContainers = $( "#comments" ).find( "*.container" );
//     var $allA = $( "#comments" ).find( "*a" );
//     //console.log('Length container ' + $allContainers.length);
//     //console.log('Length all ' + $allA.length);

    
//     for (i = 0; i < $allA.length; i++){
//         if (parseInt($allA[i].dataset.slideTo)  != active) {
//             //console.log('Wrong comment = ' + $allA[i].dataset.slideTo);
//             $allContainers[i].style.display = 'none';
            
//         } else{
//             $allContainers[i].style.display = 'block';
//         };
//     };
// };

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
        var result = (this.totalNumberOfCommentsX(slide) < this.currentNumber) ?  true :  false;
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
